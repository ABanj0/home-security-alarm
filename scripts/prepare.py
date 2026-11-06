"""Stage bootstrap configuration without replacing an existing installation."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def prepare(source: Path, target: Path) -> list[str]:
    if target.exists():
        raise FileExistsError("Runtime already exists; refusing to overwrite. Follow RECOVERY.md.")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)
    (target / "packages").mkdir(exist_ok=True)
    return sorted(str(p.relative_to(target)) for p in target.rglob("*") if p.is_file())


if __name__ == "__main__":
    files = prepare(ROOT / "config", ROOT / "runtime" / "config")
    print(f"Staged {len(files)} bootstrap files. No alarm integration enabled; no service started.")
