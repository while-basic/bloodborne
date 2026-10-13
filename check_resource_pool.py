#!/usr/bin/env python3
# Document:    Bloodborne Resource Pool Regression Check
# Version:     v1.0.0
# Author:      Christopher Celaya
# Contact:     https://github.com/while-basic
# Date:        2026-10-13
# SHA256:      7bc70e4834f336a1b8fd10f628b655d91be9d0f811c27537ab6ba20646a06969
# Chain:       solana-mainnet
# Tx:          5FQF4Y8MVKJsEKNAXGVf37Prcyk1dRVH2MAKF3MZegbQuabm5TttbZ7RMuSyhqEdFiwzH8xsacP3DM7AfP1fiGae
# License:     The Unlicense (public domain dedication)
"""Check shadPS4's real pool methods with simulated GPU progress, without a game."""
import argparse
from pathlib import Path
import subprocess
import tempfile


BASE = "e0a466753a1aacbc8db8253be685bf7ab4d9daae"
SOURCE = "src/video_core/renderer_vulkan/vk_resource_pool.cpp"
HEADER = "src/video_core/renderer_vulkan/vk_resource_pool.h"

PREAMBLE = r"""
#include <cstddef>
#include <cstdint>
#include <optional>
#include <utility>
#include <vector>
#include <iostream>
using u64 = std::uint64_t;
namespace Vulkan {
struct Semaphore {
    u64 known=4, refreshed=5, current=9;
    u64 KnownGpuTick() const { return known; }
    u64 CurrentTick() const { return current; }
    void Refresh() { known=refreshed; }
};
"""

CASES = r"""
class ProbePool final : public ResourcePool {
public:
    unsigned allocations=0;
    ProbePool(Semaphore* sem, std::vector<u64> initial, std::size_t hint)
        : ResourcePool(sem,4) { ticks=std::move(initial); hint_iterator=hint; }
    void Allocate(std::size_t, std::size_t) override { ++allocations; }
    using ResourcePool::CommitResource;
    std::size_t Size() const { return ticks.size(); }
    u64 Tick(std::size_t index) const { return ticks.at(index); }
};
}
int main() {
    using namespace Vulkan;
    unsigned failures=0;
    auto check=[&](const char* name, std::vector<u64> initial, std::size_t hint,
                   std::size_t expected_index, std::size_t expected_size, unsigned allocations) {
        Semaphore sem;
        ProbePool pool(&sem, std::move(initial),hint);
        const auto index=pool.CommitResource();
        bool ok=index==expected_index && pool.Size()==expected_size &&
                pool.allocations==allocations && pool.Tick(index)==sem.current;
        std::cout << name << ": " << (ok?"PASS":"FAIL") << "\n";
        failures+=!ok;
    };
    check("cached completed resource",{4,8,8,8},0,0,4,0);
    check("resource completes on refresh",{5,8,8,8},0,0,4,0);
    check("wrap after refreshed progress",{5,8,8,8},2,0,4,0);
    check("all resources still busy",{8,8,8,8},0,4,8,1);
    check("empty pool grows",{},0,0,4,1);
    return failures?1:0;
}
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="trusted local shadPS4 checkout with the fix applied")
    parser.add_argument("--compiler", default="clang++", help="C++20 compiler executable")
    args = parser.parse_args()
    try:
        header = (args.source / HEADER).read_text()
        # Use the production class and methods, not a second copy of their logic.
        pool_class = header[header.index("class ResourcePool {"):header.index("\nclass CommandPool")]
        before = subprocess.run(
            ["git", "-C", str(args.source), "show", f"{BASE}:{SOURCE}"],
            capture_output=True, text=True, check=True).stdout
        after = (args.source / SOURCE).read_text()
        results = {}
        with tempfile.TemporaryDirectory(prefix="bloodborne-pool-check-") as directory:
            for label, source in (("before", before), ("after", after)):
                methods = source[source.index("ResourcePool::ResourcePool("):
                                 source.index("constexpr std::size_t COMMAND_BUFFER_POOL_SIZE")]
                cpp, binary = Path(directory) / f"{label}.cpp", Path(directory) / label
                cpp.write_text(PREAMBLE + pool_class + methods + CASES)
                subprocess.run([args.compiler, "-std=c++20", "-O2", str(cpp), "-o", str(binary)],
                               capture_output=True, text=True, check=True)
                result = subprocess.run([str(binary)], capture_output=True, text=True)
                print(f"{label}:\n{result.stdout}", end="")
                if result.stderr:
                    print(result.stderr, end="")
                results[label] = result.returncode
        if results != {"before": 1, "after": 0}:
            parser.exit(1, "Expected the old code to fail and all patched cases to pass.\n")
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        detail = error.stderr if isinstance(error, subprocess.CalledProcessError) else str(error)
        parser.error(f"Could not check the pinned source: {detail}")
    print("Reproduced the old bug; all five patched cases pass. This is not an FPS test.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
