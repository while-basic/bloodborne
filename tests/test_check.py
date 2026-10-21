"""Check the bbport-only launch boundary without starting a game."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import play


class LauncherTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for name, path in {
            "ROOT": self.root, "RUNTIME": self.root / "runtime",
            "GAME": self.root / "base/eboot.bin", "GAME_PATCH": self.root / "update",
            "GAME_MERGED": self.root / "game", "BBPORT_RUN": self.root / "engine/run.sh",
            "BBPORT_DATA": self.root / "data",
        }.items():
            replacement = patch.object(play, name, path)
            replacement.start()
            self.addCleanup(replacement.stop)
        play.BBPORT_RUN.parent.mkdir()
        play.BBPORT_RUN.write_text("engine")
        play.GAME_MERGED.mkdir()
        (play.GAME_MERGED / "eboot.bin").write_text("game")
        (self.root / "original-save").write_bytes(b"keep me")

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()}

    def test_default_check_is_bbport_and_read_only(self):
        before = self.snapshot()
        output = io.StringIO()
        with patch("sys.argv", ["play.py", "--check"]), \
                patch.object(play.subprocess, "run") as run, \
                patch.object(play.subprocess, "call") as launch, contextlib.redirect_stdout(output):
            self.assertEqual(play.main(), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["engine"], str(play.BBPORT_RUN))
        self.assertTrue(result["game_ready"])
        self.assertFalse(result["merge_needed"])
        self.assertFalse(result["gameplay_verified"])
        self.assertEqual(result["fps_target"], 60)
        self.assertEqual(result["resolution"], "1080p")
        self.assertEqual(result["perf_level"], 3)
        self.assertEqual(before, self.snapshot())
        run.assert_not_called()
        launch.assert_not_called()

    def test_check_accepts_base_and_update_without_merging(self):
        (play.GAME_MERGED / "eboot.bin").unlink()
        play.GAME.parent.mkdir()
        play.GAME.write_text("base")
        play.GAME_PATCH.mkdir()
        (play.GAME_PATCH / "eboot.bin").write_text("update")
        before, output = self.snapshot(), io.StringIO()
        with patch("sys.argv", ["play.py", "--check"]), contextlib.redirect_stdout(output):
            self.assertEqual(play.main(), 0)
        self.assertTrue(json.loads(output.getvalue())["merge_needed"])
        self.assertEqual(before, self.snapshot())

    def test_missing_game_fails_without_launch_or_file_changes(self):
        (play.GAME_MERGED / "eboot.bin").unlink()
        before = self.snapshot()
        with patch("sys.argv", ["play.py", "--check"]), \
                contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            play.main()
        self.assertEqual(error.exception.code, 2)
        self.assertEqual(before, self.snapshot())

    def test_old_standalone_switches_and_conflicting_actions_are_rejected(self):
        for args in (["--engine", "nightly"], ["--engine", "release"], ["--fps", "120"],
                     ["--keep-facegen"], ["--vblank", "120"], ["--present-mode", "Fifo"],
                     ["--keep-vulkan-validation"], ["--check", "--install"], ["--stats", "--check"]):
            with self.subTest(args=args), patch("sys.argv", ["play.py", *args]), \
                    patch.object(play, "install_bbport") as install, \
                    patch.object(play.subprocess, "call") as launch, \
                    contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                play.main()
            self.assertEqual(error.exception.code, 2)
            install.assert_not_called()
            launch.assert_not_called()

    def test_old_bbport_command_remains_a_bbport_only_alias(self):
        output = io.StringIO()
        with patch("sys.argv", ["play.py", "--engine", "bbport", "--check"]), contextlib.redirect_stdout(output):
            self.assertEqual(play.main(), 0)
        self.assertEqual(json.loads(output.getvalue())["engine"], str(play.BBPORT_RUN))

    def test_launch_uses_bbport_and_explicit_logging_state(self):
        before = self.snapshot()
        with patch("sys.argv", ["play.py", "--no-log", "--windowed"]), \
                patch.dict(os.environ, {"BB_SAVE_LOG": "1", "BB_FPS_SCALE": "6"}), \
                patch.object(play.subprocess, "run") as run, \
                patch.object(play.subprocess, "call", return_value=0) as launch, \
                contextlib.redirect_stdout(io.StringIO()):
            run.return_value.returncode = 1
            self.assertEqual(play.main(), 0)
        self.assertEqual(launch.call_args.args[0], ["bash", str(play.BBPORT_RUN)])
        env = launch.call_args.kwargs["env"]
        self.assertEqual(env["BB_GAME_DIR"], str(play.GAME_MERGED))
        self.assertEqual(env["BB_DATA_DIR"], str(play.BBPORT_DATA))
        self.assertEqual(env["BB_FPS"], "60")
        self.assertEqual(env["BB_SAVE_LOG"], "0")
        self.assertEqual(env["BB_FPS_SCALE"], "1")
        self.assertEqual(env["BB_FULLSCREEN"], "0")
        self.assertEqual(before, self.snapshot())

    def test_running_game_is_left_alone(self):
        with patch("sys.argv", ["play.py"]), patch.object(play.subprocess, "run") as run, \
                patch.object(play.subprocess, "call") as launch, \
                contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            run.return_value.returncode = 0
            play.main()
        launch.assert_not_called()

    def test_install_needs_no_game_and_does_not_launch(self):
        with patch("sys.argv", ["play.py", "--install"]), \
                patch.object(play, "install_bbport") as install, \
                patch.object(play, "launch_bbport") as launch:
            self.assertEqual(play.main(), 0)
        install.assert_called_once_with()
        launch.assert_not_called()
