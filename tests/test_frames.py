"""Check that stutters and malformed captures cannot become inflated FPS claims."""
import math
from pathlib import Path
import tempfile
import unittest

from analyze_frames import read_frames, summarize


class FrameTests(unittest.TestCase):
    def read(self, body, **kwargs):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "frames.csv"
            path.write_text("elapsed_seconds,frame_ms\n" + body)
            return read_frames(path, **kwargs)

    def test_average_uses_total_time_including_stutter(self):
        frames = [(0.01, 10), (0.02, 10), (0.12, 100)]
        result = summarize(frames, "synthetic timing test")
        self.assertAlmostEqual(result["average_fps"], 25)
        self.assertEqual(result["one_percent_low_fps"], 10)
        self.assertEqual(result["worst_frame_ms"], 100)
        self.assertEqual(result["frames_over_50ms"], 1)
        self.assertAlmostEqual(result["fraction_within_90fps_budget"], 2 / 3)
        self.assertFalse(result["scene_verified_by_tool"])

    def test_window_excludes_frames_crossing_its_start(self):
        frames = self.read("0.1,100\n0.2,100\n0.3,100\n0.4,100\n", start=0.15, end=0.35)
        self.assertEqual(frames, [(0.3, 100)])

    def test_rejects_bad_records_even_outside_window(self):
        for body in ["0.1,0\n", "0.1,-1\n", "nan,10\n", "0.1,inf\n",
                     "0.1,10\n0.1,10\n", "0.2,10\n0.1,10\n", "0.1\n",
                     "0.1,10,extra\n", "-1,10\n", "0.1,10\n1.1,10\n"]:
            with self.subTest(body=body), self.assertRaises(ValueError):
                self.read(body, start=1)

    def test_rejects_empty_window_and_invalid_bounds(self):
        for bounds in [{"start": -1}, {"start": math.nan}, {"end": math.inf},
                       {"start": 1, "end": 1}, {"start": 100}]:
            with self.subTest(bounds=bounds), self.assertRaises(ValueError):
                self.read("0.1,10\n", **bounds)

    def test_percentiles_and_slow_tail(self):
        frames = [(i + 1, float(i + 1)) for i in range(100)]
        result = summarize(frames, "synthetic timing test")
        self.assertAlmostEqual(result["p99_frame_ms"], 99.01)
        self.assertEqual(result["one_percent_low_fps"], 10)
        self.assertAlmostEqual(result["average_fps"], 1000 / 50.5)


if __name__ == "__main__":
    unittest.main()
