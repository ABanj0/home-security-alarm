"""Run in the user's PowerShell: validate and start a disconnected HA bootstrap."""
from pathlib import Path
import os
import subprocess
import sys
from contextlib import contextmanager

ROOT = Path(__file__).resolve().parents[1]
COMPOSE = ["docker", "compose", "--file", "compose.yaml", "--project-name", "home-alarm"]


@contextmanager
def bootstrap_lock(root):
    path = root / ".bootstrap.lock"
    try:
        handle = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as error:
        raise RuntimeError("Bootstrap lock exists. Inspect its PID and Docker state; do not start a second deployment.") from error
    try:
        with os.fdopen(handle, "w") as lock:
            lock.write(str(os.getpid()))
        yield
    finally:
        path.unlink()


def run(args, capture=False):
    return subprocess.run(args, cwd=ROOT, check=True, text=True,
                          stdout=subprocess.PIPE if capture else None).stdout


def verify_bootstrap(root):
    """Refuse to start changed/private/live configs or an already-onboarded installation."""
    source = root / "config"
    target = root / "runtime/config"
    if not target.is_dir():
        raise RuntimeError("Run python scripts/prepare.py first.")
    expected = {p.relative_to(source) for p in source.rglob("*") if p.is_file()}
    actual = {p.relative_to(target) for p in target.rglob("*") if p.is_file()}
    if actual != expected:
        raise RuntimeError("Runtime is not the clean bootstrap. Review it manually; nothing overwritten.")
    for relative in expected:
        if (source / relative).read_bytes() != (target / relative).read_bytes():
            raise RuntimeError("Runtime differs from bootstrap templates. Review manually; nothing overwritten.")
    if not (target / "packages").is_dir() or any((target / "packages").iterdir()):
        raise RuntimeError("Bootstrap requires an empty packages directory.")
    if (target / ".storage").exists():
        raise RuntimeError("Existing HA onboarding detected; this helper is only for initial startup.")


def main():
    import json
    verify_bootstrap(ROOT)
    # The user must run this with their normal local Docker access, never a public API.
    endpoint = os.environ.get("DOCKER_HOST") or run(
        ["docker", "context", "inspect", "--format", "{{.Endpoints.docker.Host}}"], True).strip()
    if not endpoint.startswith("npipe://"):
        raise RuntimeError("Expected a local Windows Docker named pipe; review the Docker context.")
    if run(["docker", "info", "--format", "{{.OSType}}"], True).strip() != "linux":
        raise RuntimeError("Select Linux containers in Docker Desktop.")
    resolved = json.loads(run(COMPOSE + ["config", "--format", "json"], True))
    service = resolved["services"]["homeassistant"]
    ports = service.get("ports", [])
    if len(ports) != 1 or ports[0].get("host_ip") != "127.0.0.1" or str(ports[0].get("published")) != "8123":
        raise RuntimeError("Bootstrap must bind only 127.0.0.1:8123. Review HA_BIND_IP and .env.")
    if run(COMPOSE + ["ps", "--all", "--quiet"], True).strip():
        raise RuntimeError("An existing project container was found. Inspect it before proceeding.")
    image = service["image"]
    run(COMPOSE + ["pull", "homeassistant"])
    # Validate tracked YAML and Jinja with the dependencies inside the HA image.
    checker = ["docker", "run", "--rm", "--network", "none", "--entrypoint", "python"]
    for folder in ("config", "examples", "scripts"):
        checker += ["--mount", f"type=bind,source={ROOT / folder},target=/work/{folder},readonly"]
    run(checker + [image, "/work/scripts/validate_yaml.py"])
    run(["docker", "run", "--rm", "--network", "none", "--entrypoint", "python",
         "--mount", f"type=bind,source={ROOT / 'runtime/config'},target=/config",
         image, "-m", "homeassistant", "--script", "check_config", "--config", "/config"])
    # Only reached when every previous command succeeded. No EVL package is installed.
    run(COMPOSE + ["up", "-d", "homeassistant"])
    run(COMPOSE + ["ps"])
    print("Startup requested after syntax/config checks. Open http://127.0.0.1:8123")
    print("Complete owner onboarding privately. Hardware and notification tests remain pending.")


if __name__ == "__main__":
    try:
        with bootstrap_lock(ROOT):
            main()
    except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
        print(f"STOPPED: {error}", file=sys.stderr)
        sys.exit(1)
