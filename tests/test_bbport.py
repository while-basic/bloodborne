"""Exercise the bbport engine helpers without game files or the engine."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import play


class BbportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.runtime = self.root / "runtime"
        names = {
            "RUNTIME": self.runtime,
            "GAME": self.runtime / "games/CUSA00900/eboot.bin",
            "GAME_PATCH": self.runtime / "games/CUSA00900-patch",
            "GAME_MERGED": self.runtime / "games/CUSA00900-109",
            "BBPORT_DIR": self.runtime / "engines/bbport",
            "BBPORT_RUN": self.runtime / "engines/bbport/run.sh",
            "BBPORT_DATA": self.runtime / "bbport",
            "SHADPS4_SAVE": self.root / "shadPS4/savedata/CUSA00900/SPRJ0005",
        }
        for name, value in names.items():
            patcher = patch.object(play, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_perf_ladder_skips_patches_bbport_lacks(self):
        self.assertEqual(play.bbport_patches(3), ["Disable Motion Blur (perf increase)",
                                                  "Disable Chromatic Aberration"])
        self.assertEqual(len(play.bbport_patches(7)), 5)
        self.assertEqual(play.bbport_patches(0, ["Disable AA"]), ["Disable AA"])

    def test_frame_summary_ignores_menus_and_reports_lows(self):
        rows = [{"frame_ms": "16.67", "draws": "1400"}] * 99 + [{"frame_ms": "50.0", "draws": "1400"},
                                                                 {"frame_ms": "100.0", "draws": "14"}]
        summary = play.frame_summary(rows)
        self.assertEqual(summary["frames"], 100)
        self.assertEqual(summary["median_fps"], 60.0)
        self.assertEqual(summary["one_percent_low_fps"], 20.0)
        self.assertEqual(summary["frames_under_58_fps_pct"], 1.0)
        self.assertIsNone(play.frame_summary([{"frame_ms": "16.67", "draws": "14"}]))

    def test_frame_summary_skips_a_row_cut_off_at_quit(self):
        rows = [{"frame_ms": "16.67", "draws": "1400"}] * 10 + [{"frame_ms": "16.67", "draws": None}]
        self.assertEqual(play.frame_summary(rows)["frames"], 10)

    def test_merge_game_overlays_update_and_keeps_originals(self):
        play.GAME.parent.mkdir(parents=True)
        play.GAME.write_text("base")
        (play.GAME.parent / "base-only").write_text("kept")
        play.GAME_PATCH.mkdir(parents=True)
        (play.GAME_PATCH / "eboot.bin").write_text("1.09")
        play.merge_game()
        self.assertEqual((play.GAME_MERGED / "eboot.bin").read_text(), "1.09")
        self.assertEqual((play.GAME_MERGED / "base-only").read_text(), "kept")
        self.assertEqual(play.GAME.read_text(), "base")

    def test_import_save_copies_once_without_shadps4_metadata(self):
        (play.SHADPS4_SAVE / "sce_sys").mkdir(parents=True)
        (play.SHADPS4_SAVE / "userdata0000").write_text("save")
        target = play.import_save()
        self.assertEqual((target / "userdata0000").read_text(), "save")
        self.assertFalse((target / "sce_sys").exists())
        self.assertTrue((play.SHADPS4_SAVE / "userdata0000").exists())
        (target / "userdata0000").write_text("newer")
        self.assertIsNone(play.import_save())
        self.assertEqual((target / "userdata0000").read_text(), "newer")

    def test_install_refuses_a_download_with_the_wrong_hash(self):
        archive = self.runtime / f"downloads/bbport-mac-{play.BBPORT_VERSION}.zip"
        archive.parent.mkdir(parents=True)
        archive.write_bytes(b"not the release")
        with self.assertRaises(RuntimeError):
            play.install_bbport()
        self.assertFalse(archive.exists())
        self.assertFalse(play.BBPORT_DIR.exists())

    def test_check_without_install_explains_the_next_step(self):
        stderr = io.StringIO()
        with patch("sys.argv", ["play.py", "--engine", "bbport", "--check"]), \
                contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            play.main()
        self.assertIn("--engine bbport --install", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
