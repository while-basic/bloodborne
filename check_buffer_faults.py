#!/usr/bin/env python3
# Document:    Bloodborne Buffer Fault Boundary Check
# Version:     v1.0.0
# Author:      Christopher Celaya
# Contact:     https://github.com/while-basic
# Date:        2026-10-13
# SHA256:      3d44b120d16ef9c3507204cbc07646ea381c149e2aaac7233a466a5136873279
# Chain:       solana-mainnet
# Tx:          DLUihcTLgNn3zpEuYe2Kh8w85C87EWPJ889j6bgy4tMtutRgteoZ4j781hveD8kgnK8VfFCEinmcd6Qyxgu6ZZa
# License:     The Unlicense (public domain dedication)
"""Check the optional buffer patch against real source methods, without a game."""
import argparse
from pathlib import Path
import subprocess
import tempfile


SOURCE = "src/video_core/renderer_vulkan/vk_rasterizer.cpp"


def method(source, name):
    start = source.index("bool Rasterizer::" + name + "(")
    opening = source.index("{", start)
    depth, end = 1, opening + 1
    while depth:
        depth += (source[end] == "{") - (source[end] == "}")
        end += 1
    return source[start:end]


PREAMBLE = r'''
#include <boost/icl/interval_set.hpp>
#include <cstdint>
#include <limits>
#include <shared_mutex>
#include <stdexcept>
#include <tuple>
#include <vector>
#include <iostream>
using u64 = std::uint64_t;
using VAddr = u64;
namespace Common { using RecursiveSharedLock = std::shared_lock<std::shared_mutex>; }
struct BufferCache {
    std::vector<std::tuple<u64,u64,bool>> calls;
    void InvalidateMemory(u64 addr,u64 size,bool locks) { calls.emplace_back(addr,size,locks); }
};
struct TextureCache {
    std::vector<std::pair<u64,u64>> calls;
    void InvalidateMemory(u64 addr,u64 size) { calls.emplace_back(addr,size); }
};
struct Rasterizer {
    BufferCache buffer_cache;
    TextureCache texture_cache;
    boost::icl::interval_set<VAddr> mapped_ranges;
    std::shared_mutex mapped_ranges_mutex;
    bool InvalidateMemory(VAddr,u64,bool=false,bool=false);
    bool IsMapped(VAddr,u64);
    void map(u64 start,u64 end) {
        mapped_ranges += decltype(mapped_ranges)::interval_type::right_open(start,end);
    }
};
void require(bool value) { if (!value) throw std::runtime_error("boundary check failed"); }
void expect(Rasterizer& r,u64 addr,u64 size,bool enabled,u64 buffer_addr,u64 buffer_size,bool locks=false) {
    require(r.InvalidateMemory(addr,size,locks,enabled));
    require(r.buffer_cache.calls == std::vector<std::tuple<u64,u64,bool>>{{buffer_addr,buffer_size,locks}});
    require(r.texture_cache.calls == std::vector<std::pair<u64,u64>>{{addr,size}});
}
'''

CASES = r'''
int main() {
    try {
        { Rasterizer r; r.map(0x10000,0x20000); expect(r,0x12345,8,false,0x12345,8); }
        { Rasterizer r; r.map(0x10000,0x20000); expect(r,0x12345,8,true,0x10000,0x4000,true); }
        { Rasterizer r; r.map(0x12000,0x14000); expect(r,0x12345,8,true,0x12345,8); }
        { Rasterizer r; require(!r.InvalidateMemory(0x12345,8,false,true));
          require(r.buffer_cache.calls.empty() && r.texture_cache.calls.empty()); }
        { Rasterizer r; r.map(0x10000,0x20000); expect(r,0x14000,8,true,0x14000,0x4000); }
        { Rasterizer r; r.map(0x10000,0x20000); expect(r,0x13fff,1,true,0x10000,0x4000); }
        { Rasterizer r; require(!r.InvalidateMemory(UINT64_MAX-3,8,false,true));
          require(r.buffer_cache.calls.empty() && r.texture_cache.calls.empty()); }
        { Rasterizer r; r.map(0x10000,0x11000); r.map(0x12000,0x14000);
          expect(r,0x12345,8,true,0x12345,8); }
        { Rasterizer r; r.map(UINT64_MAX-0x3fff,UINT64_MAX);
          expect(r,UINT64_MAX-7,7,true,UINT64_MAX-7,7); }
        { Rasterizer r; r.map(0x10000,0x20000); require(!r.InvalidateMemory(0x12345,0,false,true));
          require(r.buffer_cache.calls.empty() && r.texture_cache.calls.empty()); }
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
    std::cout << "10 boundary cases pass. This is not a concurrency or FPS test.\n";
}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="trusted shadPS4 checkout with the buffer patch")
    parser.add_argument("--compiler", default="clang++", help="C++20 compiler executable")
    args = parser.parse_args()
    try:
        source = (args.source / SOURCE).read_text()
        code = PREAMBLE + method(source, "InvalidateMemory") + method(source, "IsMapped") + CASES
        with tempfile.TemporaryDirectory(prefix="bloodborne-buffer-check-") as directory:
            path = Path(directory)
            cpp, binary = path / "check.cpp", path / "check"
            cpp.write_text(code)
            subprocess.run([args.compiler, "-std=c++20", "-O1", "-I",
                            str((args.source / "externals/ext-boost").resolve()),
                            str(cpp), "-o", str(binary)], capture_output=True, text=True, check=True)
            result = subprocess.run([str(binary)], capture_output=True, text=True, check=True)
            print(result.stdout, end="")
    except (OSError, ValueError, IndexError, subprocess.CalledProcessError) as error:
        detail = error.stderr if isinstance(error, subprocess.CalledProcessError) else str(error)
        parser.error(f"Could not check the patched source: {detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
