"""Exercise the public dry run without game files or an emulator."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import play


class DryRunTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.runtime = self.root / "runtime"
        self.xml = self.runtime / "downloads/Bloodborne.xml"
        self.xml.parent.mkdir(parents=True)
        self.game = self.runtime / "games/CUSA00900/eboot.bin"
        self.game.parent.mkdir(parents=True)
        self.game.touch()
        self.engine = self.root / "shadps4"
        self.engine.touch()
        self.config = self.root / "config.json"
        self.config.write_text("{}\n")
        self.profile = self.root / "patches/bloodborne-profile"
        root = ET.Element("Patch")
        ET.SubElement(ET.SubElement(root, "TitleID"), "ID").text = "CUSA00900"
        for name in sorted(play.selected_patches("1080p", 60, 3)):
            ET.SubElement(root, "Metadata", Name=name, AppVer="01.09")
        ET.ElementTree(root).write(self.xml)
        for name, value in {
            "RUNTIME": self.runtime,
            "GAME": self.game,
            "CONFIG": self.config,
            "PATCH_DIR": self.profile,
            "ENGINES": {"nightly": self.engine, "release": self.engine},
        }.items():
            replacement = patch.object(play, name, value)
            replacement.start()
            self.addCleanup(replacement.stop)

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()}

    def test_check_is_read_only_and_does_not_claim_gameplay(self):
        before = self.snapshot()
        output = io.StringIO()
        with patch("sys.argv", ["play.py", "--check"]), \
                patch.object(play.subprocess, "run") as run, \
                patch.object(play.subprocess, "call") as launch, \
                contextlib.redirect_stdout(output):
            self.assertEqual(play.main(), 0)
        result = json.loads(output.getvalue())
        self.assertTrue(result["local_files_present"])
        self.assertFalse(result["gameplay_verified"])
        self.assertEqual(result["fps_target"], 60)
        self.assertEqual(result["vblank_hz"], 60)
        self.assertEqual(before, self.snapshot())
        self.assertFalse(self.profile.exists())
        run.assert_not_called()
        launch.assert_not_called()

    def test_check_reports_timing_request_without_applying_it(self):
        before = self.snapshot()
        output = io.StringIO()
        with patch("sys.argv", ["play.py", "--check", "--vblank", "120",
                                "--present-mode", "Fifo", "--windowed"]), \
                patch.object(play.subprocess, "run") as run, \
                patch.object(play.subprocess, "call") as launch, \
                contextlib.redirect_stdout(output):
            self.assertEqual(play.main(), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["fps_target"], 60)
        self.assertEqual(result["vblank_hz"], 120)
        self.assertEqual(result["present_mode_requested"], "Fifo")
        self.assertEqual(result["fullscreen_mode"], "windowed")
        self.assertFalse(result["gameplay_verified"])
        self.assertEqual(before, self.snapshot())
        run.assert_not_called()
        launch.assert_not_called()

    def test_invalid_vblank_fails_before_reading_or_writing_settings(self):
        for rate in ("-1", "0", "29", "1001", "4294967296"):
            with self.subTest(rate=rate):
                before = self.snapshot()
                errors = io.StringIO()
                with patch("sys.argv", ["play.py", "--vblank", rate]), \
                        patch.object(play, "make_profile") as profile, \
                        patch.object(play, "write_config") as config, \
                        patch.object(play.subprocess, "run") as run, \
                        contextlib.redirect_stderr(errors), \
                        self.assertRaises(SystemExit) as raised:
                    play.main()
                self.assertEqual(raised.exception.code, 2)
                self.assertIn("--vblank must be between 30 and 1000", errors.getvalue())
                self.assertEqual(before, self.snapshot())
                profile.assert_not_called()
                config.assert_not_called()
                run.assert_not_called()

    def test_missing_game_fails_without_claiming_success(self):
        self.game.unlink()
        output, errors = io.StringIO(), io.StringIO()
        with patch("sys.argv", ["play.py", "--check"]), \
                contextlib.redirect_stdout(output), \
                contextlib.redirect_stderr(errors), \
                self.assertRaises(SystemExit) as raised:
            play.main()
        self.assertEqual(raised.exception.code, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("Required local file missing", errors.getvalue())
        self.assertFalse(self.profile.exists())


if __name__ == "__main__":
    unittest.main()
