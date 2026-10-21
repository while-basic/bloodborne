import importlib.util
from pathlib import Path
import struct
import unittest

spec = importlib.util.spec_from_file_location("brand_loading", Path(__file__).parents[1] / "mods/csr/brand_loading.py")
brand = importlib.util.module_from_spec(spec)
spec.loader.exec_module(brand)


class LoadingTagsTests(unittest.TestCase):
    def movie(self, body):
        data = bytearray(b"GFX\x0b\0\0\0\0\x08\x00\0\x1e\x01\0" + body)
        struct.pack_into("<I", data, 4, len(data))
        return data

    def test_short_and_long_tags_preserve_exact_boundaries(self):
        body = struct.pack("<HI", (37 << 6) | 63, 3) + b"abc" + struct.pack("<HH", 1 << 6, 0)
        data = self.movie(body)
        parsed = brand.tags(data)
        self.assertEqual([t[0] for t in parsed], [37, 1, 0])
        self.assertEqual(b"".join(data[start:end] for _, start, _, end in parsed), body)

    def test_refuses_truncated_headers_payload_and_missing_end(self):
        for body in (b"\x01", struct.pack("<H", (37 << 6) | 63),
                     struct.pack("<HI", (37 << 6) | 63, 100), struct.pack("<H", 1 << 6)):
            with self.subTest(body=body), self.assertRaises(ValueError):
                brand.tags(self.movie(body))

    def test_refuses_wrong_format_and_size(self):
        for offset in (0, 3, 4):
            data = self.movie(b"\0\0")
            data[offset] ^= 1
            with self.subTest(offset=offset), self.assertRaises(ValueError):
                brand.tags(data)
