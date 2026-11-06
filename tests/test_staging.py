from pathlib import Path
import importlib.util
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("prepare", ROOT / "scripts/prepare.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class StagingTests(unittest.TestCase):
    def test_staging_has_no_live_panel_package_or_secrets(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "config"
            files = module.prepare(ROOT / "config", target)
            self.assertIn("configuration.yaml", files)
            self.assertEqual(list((target / "packages").iterdir()), [])
            self.assertFalse((target / "secrets.yaml").exists())

    def test_existing_runtime_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "config"
            target.mkdir()
            marker = target / "configuration.yaml"
            marker.write_text("existing private data", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                module.prepare(ROOT / "config", target)
            self.assertEqual(marker.read_text(encoding="utf-8"), "existing private data")

    def test_development_configs_do_not_call_alarm_actions(self):
        forbidden = ["alarm_control_panel.alarm_", "envisalink.alarm_keypress",
                     "envisalink.invoke_custom_function", "shell_command.", "rest_command."]
        for path in (ROOT / "config").rglob("*.yaml"):
            content = path.read_text(encoding="utf-8")
            for action in forbidden:
                self.assertNotIn(action, content, str(path))

    def test_no_saved_code_in_integration_example(self):
        import re
        text = (ROOT / "examples/envisalink.yaml").read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"^\s*code\s*:", text, re.M))


if __name__ == "__main__":
    unittest.main()
