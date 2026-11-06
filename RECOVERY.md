# Troubleshooting and recovery

| Symptom | Check and next action |
|---|---|
| Docker client but no server | Start Docker Desktop/Linux engine in the user's session; verify WSL integration and `docker version`. Agent sandbox denial is not proof WSL is broken. |
| Bootstrap container-name conflict | Run `docker compose ps --all`; inspect the existing container's Compose labels, configuration mount, state and ports. If it is this project's healthy HA instance, keep it and continue onboarding. Do not delete it merely to rerun bootstrap. |
| Bootstrap lock exists | Inspect the PID recorded in `.bootstrap.lock` and current process/container state. A lock file alone does not prove work is running. Remove only the stale lock after verifying its process has ended; preserve runtime data and containers. |
| UI only works on Windows | Bootstrap binds loopback. Follow SETUP's explicit LAN binding/firewall step; verify Windows Private network profile and address. |
| EVL not online | Compare LEDs with vendor guide; check DHCP lease, Ethernet and EyezOn activation. Leave panel wiring to technician. |
| HA authentication failure | Confirm local EVL credentials, not cloud credentials; edit private secrets, validate, restart HA only. |
| Missing/wrong zones | Verify actual zone/partition numbers and entity IDs. No automatic zone discovery or inferred room labels. |
| Frozen status but Ping works | ICMP cannot prove TPI health. Inspect integration logs/session and compare fresh keypad/contact events. Keep AT-016 unresolved until detection is verified. |
| Duplicate or missing alerts | Check instantiated blueprints, notify action, app permissions/Focus and actual event selections in EyezOn; distinguish independent HA/EyezOn messages. |
| No trouble sensor | Inspect actual keypad attributes. Do not guess fields or coerce missing values to healthy. Escalate unsupported trouble reporting as an acceptance gap. |
| HA down after reboot/sleep | Check Windows uptime, Docker startup and container restart policy; test operator-approved startup/power policy. |

## Backup

Prefer the supported HA backup UI for routine backups: Settings > System > Backups >
Set up backups. Download the emergency kit privately and keep it separately from the
PC; its encryption key is needed for recovery. Configure encrypted backups and retain
an off-device copy. Confirm the first backup completes before treating backup setup as
done. On HA Container, local backup archives are under `runtime/config/backups`.
The container backup does not cover this repository's Compose files, private overrides,
Windows/Docker startup settings or Tailscale policy; protect those separately. Never
paste the emergency kit or encryption key into chat. A restore exercise must use an
isolated instance without EVL network access. See the
[official backup guide](https://www.home-assistant.io/common-tasks/general/backups/).

The cold-copy procedure below is an alternative for an agreed maintenance window:

With a planned HA-only maintenance window, stop HA using `docker compose stop` to obtain
a consistent database and `.storage` snapshot. Copy the entire private `runtime/config`
directory and `.env` to encrypted storage with restricted access, recording the image tag
and date. Resume with `docker compose start`. Test that it resumes and receives fresh
events. Back up before upgrades and after entity/account configuration changes.
Never commit the backup or run two HA instances against EVL during restore testing.

## Roll back HA configuration

Stop HA. Preserve the current private configuration for diagnosis; restore a known-good
backup to `runtime/config` without merging `.storage` files. Restore its recorded image
tag in Compose. Run the native network-isolated config check, start HA and verify fresh
states and notifications. If disabling EVL integration for diagnosis, move its package
outside the included `packages` directory and restart HA. Do not factory-reset DSC/EVL
or change panel programming as a software rollback. Existing keypad operation should
remain independent and must be verified during acceptance.

## Upgrade

Read HA release notes and Envisalink changes, back up, select a specific release tag,
pull it and run the native configuration check before deployment. After starting, repeat
zone/status, notification, communications-loss and recovery checks. Keep the prior image
available until acceptance passes. On failure, restore both previous configuration and
image; database/storage migrations may not support an image-only downgrade.

## Lost phone or exposed credential

Revoke affected HA/remote-service sessions, remove the lost phone from notification
recipients and rotate compromised credentials privately. If an alarm code is exposed,
have the user arrange an authorized code change at the panel; never automate programming.
Review logs locally, preserving privacy. A password change does not itself verify alert
delivery; rerun relevant tests.
