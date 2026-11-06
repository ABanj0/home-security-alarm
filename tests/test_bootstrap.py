from pathlib import Path
import importlib.util
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("bootstrap", ROOT / "scripts/bootstrap.py")
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "config", self.root / "config")
        shutil.copytree(ROOT / "config", self.root / "runtime/config")
        (self.root / "runtime/config/packages").mkdir()

    def test_clean_bootstrap_accepted(self):
        bootstrap.verify_bootstrap(self.root)

    def test_overlapping_deployment_rejected(self):
        with bootstrap.bootstrap_lock(self.root):
            with self.assertRaises(RuntimeError):
                with bootstrap.bootstrap_lock(self.root):
                    self.fail("Second bootstrap entered")
            self.assertTrue((self.root / ".bootstrap.lock").exists())
        self.assertFalse((self.root / ".bootstrap.lock").exists())

    def test_lock_released_on_failure(self):
        with self.assertRaises(ValueError):
            with bootstrap.bootstrap_lock(self.root):
                raise ValueError("Simulated deployment failure")
        self.assertFalse((self.root / ".bootstrap.lock").exists())

    def test_live_package_rejected(self):
        (self.root / "runtime/config/packages/envisalink.yaml").write_text("envisalink: {}")
        with self.assertRaises(RuntimeError):
            bootstrap.verify_bootstrap(self.root)

    def test_modified_runtime_rejected_without_overwrite(self):
        path = self.root / "runtime/config/configuration.yaml"
        path.write_text("private existing configuration")
        with self.assertRaises(RuntimeError):
            bootstrap.verify_bootstrap(self.root)
        self.assertEqual(path.read_text(), "private existing configuration")

    def test_failed_docker_check_never_reaches_start(self):
        with patch.object(bootstrap, "ROOT", self.root), patch.dict("os.environ", {"DOCKER_HOST": "npipe:////./pipe/docker_engine"}), patch.object(bootstrap, "run", side_effect=subprocess.CalledProcessError(1, "docker")) as runner:
            with self.assertRaises(subprocess.CalledProcessError):
                bootstrap.main()
        self.assertEqual(runner.call_count, 1)
        self.assertNotIn("up", runner.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
