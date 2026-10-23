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
        play.BBPORT_DATA.mkdir()
        (play.BBPORT_DATA / "bbport.ini").write_text("upscaler=taa\npreset=2\nunknown=keep\n")

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
        self.assertNotIn("BB_UPSCALER", result["runtime_env"])
        self.assertNotIn("BB_VBLANK_HZ", result["runtime_env"])
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

    def test_metal_profiles_check_and_launch_match_without_changing_saved_settings(self):
        for options in ([], ["--tuned"], ["--metalfx"], ["--tuned", "--metalfx"]):
            with self.subTest(options=options):
                before, output = self.snapshot(), io.StringIO()
                directories = {p for p in self.root.rglob("*") if p.is_dir()}
                with patch("sys.argv", ["play.py", *options, "--check"]), \
                        patch.object(play.subprocess, "run") as run, \
                        patch.object(play.subprocess, "call") as launch, contextlib.redirect_stdout(output):
                    self.assertEqual(play.main(), 0)
                run.assert_not_called()
                launch.assert_not_called()
                self.assertEqual(directories, {p for p in self.root.rglob("*") if p.is_dir()})
                self.assertEqual(before, self.snapshot())
                report = json.loads(output.getvalue())
                with patch("sys.argv", ["play.py", *options]), \
                        patch.object(play.subprocess, "run") as run, \
                        patch.object(play.subprocess, "call", return_value=0) as launch, \
                        contextlib.redirect_stdout(io.StringIO()):
                    run.return_value.returncode = 1
                    self.assertEqual(play.main(), 0)
                env = launch.call_args.kwargs["env"]
                self.assertEqual(report["runtime_env"], {key: env[key] for key in report["runtime_env"]})
                self.assertEqual(env.get("BB_UPSCALER"),
                                 "metalfx" if "--metalfx" in options else None)
                if "--metalfx" in options:
                    self.assertEqual((env["BB_UPSCALE_PRESET"], env["BB_FSR_SHARPNESS"]), ("0", "0"))
                if "--tuned" in options:
                    self.assertEqual((env["BB_VBLANK_HZ"], env["BB_STAGING_KEEP_MB"],
                                      env["BB_FAULT_WINDOW"], env["BB_RETINA"]), ("0", "2048", "1024", "0"))
                else:
                    self.assertFalse({"BB_VBLANK_HZ", "BB_STAGING_KEEP_MB", "BB_FAULT_WINDOW", "BB_RETINA"} & env.keys())
                self.assertEqual((env["BB_RENDER_RES"], env["BB_OUTPUT_RES"], env["BB_FPS"]),
                                 ("1920x1080", "1920x1080", "60"))
                self.assertEqual(env["MESA_SHADER_CACHE_DIR"], str(play.RUNTIME / "cache/mesa"))
                self.assertEqual(env["MESA_SHADER_CACHE_MAX_SIZE"], "4G")
                self.assertTrue(Path(env["MESA_SHADER_CACHE_DIR"]).is_dir())
                self.assertEqual(before, self.snapshot())

    def test_shell_experiments_cannot_redirect_or_change_the_launch(self):
        stale = {key: "stale" for key in (
            "BB_CONFIG", "BB_GAME_DIR", "BB_DATA_DIR", "BB_PATCHES", "BB_PROBE", "BB_DEPS",
            "BB_GUEST_IN_PLACE", "BB_METALFX_INTERPOLATE", "BB_GPU_COMMAND_WRITES", "BB_WRITE_TRACKING",
            "BB_UPSCALER", "BB_UPSCALE_PRESET", "BB_OBJECT_MOTION", "BB_FRAME_STATS", "BB_FRAME_LOG",
            "BB_VBLANK_HZ", "BB_STAGING_KEEP_MB", "BB_FAULT_WINDOW", "BB_RETINA",
            "MESA_SHADER_CACHE_DIR", "MESA_SHADER_CACHE_MAX_SIZE")}
        with patch.dict(os.environ, {**stale, "PATH": os.environ["PATH"]}, clear=True), \
                patch("sys.argv", ["play.py"]), patch.object(play.subprocess, "run") as run, \
                patch.object(play.subprocess, "call", return_value=0) as launch, \
                contextlib.redirect_stdout(io.StringIO()):
            run.return_value.returncode = 1
            self.assertEqual(play.main(), 0)
            env = launch.call_args.kwargs["env"]
            self.assertEqual(env["PATH"], os.environ["PATH"])
            self.assertEqual(os.environ["BB_GUEST_IN_PLACE"], "stale")
        self.assertEqual(env["BB_CONFIG"], str(play.BBPORT_DATA / "bbport.ini"))
        self.assertEqual(env["BB_PATCHES"], ";".join(play.bbport_patches(3)))
        self.assertFalse(set(stale) & {key for key, value in env.items() if value == "stale"})
        self.assertFalse({"BB_GUEST_IN_PLACE", "BB_METALFX_INTERPOLATE", "BB_PROBE", "BB_DEPS"} & env.keys())

    def test_source_engine_receives_metal_profile_through_real_child_process(self):
        source = self.root / "source engine"
        script = source / "tools/macos/run.sh"
        script.parent.mkdir(parents=True)
        (source / "out").mkdir()
        (source / "out/bb-probe").write_text("fixture")
        script.write_text('printf "%s\\n" "$BB_UPSCALER" "$BB_UPSCALE_PRESET" "$BB_VBLANK_HZ" '
                          '"$BB_CONFIG" > "$BB_DATA_DIR/received.txt"\nexit 7\n')
        before = (play.BBPORT_DATA / "bbport.ini").read_bytes()
        with patch("sys.argv", ["play.py", "--bbport-src", str(source), "--metalfx", "--tuned"]), \
                patch.object(play.subprocess, "run") as run, contextlib.redirect_stdout(io.StringIO()):
            run.return_value.returncode = 1
            self.assertEqual(play.main(), 7)
        self.assertEqual((play.BBPORT_DATA / "received.txt").read_text().splitlines(),
                         ["metalfx", "0", "0", str(play.BBPORT_DATA / "bbport.ini")])
        self.assertEqual((play.BBPORT_DATA / "bbport.ini").read_bytes(), before)

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
