#!/usr/bin/env python3
# Document:    Bloodborne Buffer Fault Boundary Check
# Version:     v1.1.0
# Author:      Christopher Celaya
# Contact:     https://github.com/while-basic
# Date:        2026-10-13
# SHA256:      a3ed04ca1c125412e5c84e9163c717569408ce3648a32b9412aa774378b83baa
# Chain:       solana-mainnet
# Tx:          2dLFsKCeG3S7m6DMgsCp7yg58UBMMCSS6unpL5k8dHJPiuJyNY4vmgDHbkSJ1w1VcahGJYymTSQoZs14Ln8x4H8o
# License:     The Unlicense (public domain dedication)
"""Check the optional buffer patch against real source methods, without a game."""
import argparse
import os
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
    bool InvalidateMemory(VAddr,u64,bool=false,u64=0);
    bool IsMapped(VAddr,u64);
    void map(u64 start,u64 end) {
        mapped_ranges += decltype(mapped_ranges)::interval_type::right_open(start,end);
    }
};
void require(bool value) { if (!value) throw std::runtime_error("boundary check failed"); }
void expect(Rasterizer& r,u64 addr,u64 size,u64 enabled,u64 buffer_addr,u64 buffer_size,bool locks=false) {
    require(r.InvalidateMemory(addr,size,locks,enabled));
    require(r.buffer_cache.calls == std::vector<std::tuple<u64,u64,bool>>{{buffer_addr,buffer_size,locks}});
    require(r.texture_cache.calls == std::vector<std::pair<u64,u64>>{{addr,size}});
}
'''

CASES = r'''
int main() {
    unsigned cases = 0;
    for (u64 window : {16384ULL,65536ULL,262144ULL}) {
        const u64 base=0x100000, addr=base+0x2345;
        { Rasterizer r; r.map(base,base+window); expect(r,addr,8,0,addr,8); ++cases; }
        { Rasterizer r; r.map(base,base+window); expect(r,addr,8,window,base,window,true); ++cases; }
        { Rasterizer r; r.map(addr,addr+8); expect(r,addr,8,window,addr,8); ++cases; }
        { Rasterizer r; require(!r.InvalidateMemory(addr,8,false,window));
          require(r.buffer_cache.calls.empty() && r.texture_cache.calls.empty()); ++cases; }
        { Rasterizer r; r.map(base,base+2*window); expect(r,base+window,8,window,base+window,window); ++cases; }
        { Rasterizer r; r.map(base,base+window); expect(r,base+window-1,1,window,base,window); ++cases; }
        { Rasterizer r; require(!r.InvalidateMemory(UINT64_MAX-3,8,false,window));
          require(r.buffer_cache.calls.empty() && r.texture_cache.calls.empty()); ++cases; }
        { Rasterizer r; r.map(base,base+0x1000); r.map(base+0x2000,base+window);
          expect(r,addr,8,window,addr,8); ++cases; }
        { Rasterizer r; r.map(UINT64_MAX-window+1,UINT64_MAX);
          expect(r,UINT64_MAX-7,7,window,UINT64_MAX-7,7); ++cases; }
        { Rasterizer r; r.map(base,base+window); require(!r.InvalidateMemory(addr,0,false,window));
          require(r.buffer_cache.calls.empty() && r.texture_cache.calls.empty()); ++cases; }
        { Rasterizer r; r.map(base,base+2*window);
          expect(r,base+window-4,8,window,base+window-4,8); ++cases; }
        { Rasterizer r; r.map(base,base+2*window);
          expect(r,base,window+8,window,base,window+8); ++cases; }
    }
    for (u64 invalid : {1ULL,4096ULL,32768ULL,UINT64_MAX}) {
        Rasterizer r; r.map(0x100000,0x200000);
        expect(r,0x123456,8,invalid,0x123456,8); ++cases;
    }
    std::cout << cases << " actual-method window boundary checks passed\n";
}
'''


ENV_PREAMBLE = r"""
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <iostream>
using u64 = std::uint64_t;
int main() {
    u64 buffer_fault_window = 0;
"""
ENV_END = r"""
    std::cout << buffer_fault_window << "\n";
}
"""
ENV_CASES = [
    (None, None, 0), ("0", None, 0), ("1", None, 16384), ("10", None, 0),
    (None, "0", 0), (None, "16", 16384), (None, "64", 65536),
    (None, "256", 262144), ("1", "0", 0), ("1", "64", 65536),
    (None, "32", 0), (None, "64x", 0), ("1", "-1", 16384), (None, "", 0),
]


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
            page_manager = (args.source / "src/video_core/page_manager.cpp").read_text()
            start = page_manager.index('        const char* wide_faults = std::getenv(')
            end = page_manager.index('        // Should be called first.', start)
            cpp.write_text(ENV_PREAMBLE + page_manager[start:end] + ENV_END)
            subprocess.run([args.compiler, "-std=c++20", "-O1", str(cpp), "-o", str(binary)],
                           capture_output=True, text=True, check=True)
            for legacy, window, expected in ENV_CASES:
                env = os.environ.copy()
                for name, value in (("SHADPS4_WRITE_FAULT_WINDOW_16K", legacy),
                                    ("SHADPS4_BUFFER_WRITE_WINDOW_KIB", window)):
                    env.pop(name, None)
                    if value is not None:
                        env[name] = value
                result = subprocess.run([str(binary)], env=env, capture_output=True,
                                        text=True, check=True)
                if int(result.stdout.strip()) != expected:
                    raise ValueError(f"Wrong buffer window for {legacy!r}, {window!r}")
            print(f"{len(ENV_CASES)} actual-source environment checks passed")
    except (OSError, ValueError, IndexError, subprocess.CalledProcessError) as error:
        detail = error.stderr if isinstance(error, subprocess.CalledProcessError) else str(error)
        parser.error(f"Could not check the patched source: {detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
