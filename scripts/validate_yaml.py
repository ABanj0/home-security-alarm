"""Offline syntax checks only; native HA check and live acceptance remain required."""
from pathlib import Path
import sys

try:
    import yaml
    from jinja2 import Environment
except ImportError:
    sys.exit("BLOCKED: install requirements-dev.txt in a local venv; YAML/Jinja checks did not run.")

ROOT = Path(__file__).resolve().parents[1]


class Loader(yaml.SafeLoader):
    pass


for tag in ("!input", "!secret", "!include", "!include_dir_named"):
    Loader.add_constructor(tag, lambda loader, node: loader.construct_scalar(node))


def walk(value):
    if isinstance(value, dict):
        for child in value.values():
            walk(child)
    elif isinstance(value, list):
        for child in value:
            walk(child)
    elif isinstance(value, str) and ("{{" in value or "{%" in value):
        Environment().parse(value)


count = 0
for folder in ("config", "examples"):
    for path in (ROOT / folder).rglob("*.yaml"):
        parsed = yaml.load(path.read_text(encoding="utf-8"), Loader=Loader)
        walk(parsed)
        if "blueprints" in path.parts:
            assert parsed["blueprint"]["domain"] == "automation", path
            assert parsed["triggers"] and parsed["actions"], path
            # Every !input must be declared by the blueprint.
            import re
            inputs = re.findall(r"!input\s+(\w+)", path.read_text(encoding="utf-8"))
            assert set(inputs) <= set(parsed["blueprint"]["input"]), path
        count += 1
print(f"PASS: {count} YAML files and embedded Jinja syntax; NOT HA runtime/schema validation.")
