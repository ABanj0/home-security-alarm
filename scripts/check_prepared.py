"""Validate the integration example and blueprint instances without hardware access."""
from pathlib import Path
import shutil
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[1]


def main():
    # Separate ignored fixture: never use or modify live credentials or .storage.
    target = ROOT / "private" / ("schema-check-" + uuid.uuid4().hex)
    shutil.copytree(ROOT / "config", target)
    (target / "packages").mkdir()
    shutil.copy2(ROOT / "examples/envisalink.yaml", target / "packages/envisalink.yaml")
    (target / "secrets.yaml").write_text(
        'envisalink_host: "127.0.0.1"\nenvisalink_user: "validation"\nenvisalink_password: "not-a-real-password"\n',
        encoding="utf-8")
    (target / "automations.yaml").write_text('''
- alias: Validate alarm notifications
  use_blueprint:
    path: home_alarm/alarm_notifications.yaml
    input:
      alarm: alarm_control_panel.validation
      notify_action: notify.mobile_app_validation
- alias: Validate trouble notifications
  use_blueprint:
    path: home_alarm/health_notifications.yaml
    input:
      health_sensor: binary_sensor.validation_trouble
      fault_state: "on"
      label: Validation trouble
      notify_action: notify.mobile_app_validation
- alias: Validate connectivity notifications
  use_blueprint:
    path: home_alarm/health_notifications.yaml
    input:
      health_sensor: binary_sensor.validation_connectivity
      fault_state: "off"
      label: Validation connectivity
      notify_action: notify.mobile_app_validation
- alias: Validate contact notifications
  use_blueprint:
    path: home_alarm/contact_notifications.yaml
    input:
      contacts:
        - binary_sensor.validation_contact
      notify_action: notify.mobile_app_validation
''', encoding="utf-8")
    subprocess.run([
        "docker", "run", "--rm", "--network", "none", "--entrypoint", "python",
        "--mount", f"type=bind,source={target},target=/config",
        "ghcr.io/home-assistant/home-assistant:2026.10.4", "-m", "homeassistant",
        "--script", "check_config", "--config", "/config"], check=True, cwd=ROOT)
    print("PASS: native HA configuration check for integration example and blueprint instances.")
    print("No network, real credentials, notifications or panel commands; not a live test.")


if __name__ == "__main__":
    main()
