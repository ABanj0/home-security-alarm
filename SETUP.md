# Installation and configuration

Run project commands from `home-security-alarm` in PowerShell. This guide stages a new
installation; do not merge it over an existing HA installation without a backup and review.
All real configuration and credentials go under ignored `runtime/` or `private/`.

## 1. Bootstrap without alarm connectivity

For a fresh installation, install requirements-dev.txt in a local virtual environment,
then run the following from the repository root in your normal Windows PowerShell session.
If an installation already exists, preserve it and follow RECOVERY.md instead.

```powershell
python scripts/prepare.py
python scripts/bootstrap.py
```

This helper refuses changed/live runtime configuration or an existing project container.
It checks for a local Linux Docker engine and loopback binding, pulls the pinned image,
runs YAML/Jinja checks and native HA configuration validation without networking, and
only then starts the bootstrap. It installs no EVL package and requests no alarm code.
If it stops, report the error; do not delete existing runtime data to bypass a check.
Once startup succeeds, open `http://127.0.0.1:8123` and create the HA owner account privately.
The equivalent manual steps follow.

1. Start Docker Desktop interactively and select Linux containers. Run `docker version`
   and `docker info`; both must return a server. Resolve WSL permissions in the user's
   session if needed. A restricted agent session may not have engine access.
2. Run `python scripts/prepare.py` once. It refuses an existing target and copies only
   bootstrap files to `runtime/config`; the EVL package is deliberately not included.
3. Validate before starting:

   ```powershell
   docker compose config --quiet
   docker compose pull
   docker run --rm --network none --entrypoint python --mount "type=bind,source=$((Resolve-Path runtime/config).Path),target=/config" ghcr.io/home-assistant/home-assistant:2026.10.4 -m homeassistant --script check_config --config /config
   ```

   A network-isolated check may lack integration dependencies in the image. Record
   that as blocked, never as a schema pass. Do not start an unvalidated live package.
4. After the native check passes, run `docker compose up -d`, open
   `http://127.0.0.1:8123`, create your private owner account and enable MFA.
   Verify `docker compose ps`. No panel commands are part of this procedure.

The image is pinned to the release used during preparation. Verify pull, native checks
and startup on the target host. Review release/security fixes before future upgrades.
The container uses a bridge network and explicit host binding, not host networking or
privileged mode. Direct EVL IP connectivity does not require discovery. HA Container
has no Supervisor/add-on installation flow. See the official
[Container installation](https://www.home-assistant.io/installation/linux/).

## 2. Confirm physical installation (manual gate)

Record the baseline keypad state, existing trouble, battery condition, partition use,
all wired contacts and any attached dialer. Have an appropriately qualified technician
verify available panel current and installation. Follow the panel and module manuals;
isolate AC and backup battery before wiring. Preserve existing keypad, zones and siren.
No panel programming changes are authorized.

EVL connects to the Keybus, never telephone Tip/Ring. Connect Ethernet to a DHCP LAN.
Record the module MAC privately for activation. The manufacturer's DSC procedure uses
automatic enrollment. Confirm OPER, KEYB, NET, LINK and ONLINE indications against the
[quick-start manual](https://www.eyezon.com/Envisalink4MQuickStartFull.pdf).
Report installation status before proceeding; LEDs alone are not a siren test.

## 3. Network and independent EyezOn alerts

Find EVL in router DHCP leases, reserve its address, and check its local interface on
the trusted LAN. Use credentials from the supplied guide for initial login; change
defaults to a unique supported password. Verify firmware and panel status. Do not
reset the module to work around an unknown password without a recovery plan.

Sign in to EyezOn yourself, add the EVL-4 with panel type DSC and its private module
identifier. Install the vendor-linked iPhone app; authorize notifications. In the actual
portal/app, configure recipient/event selections for alarm, arm, disarm, trouble and
network supervision where offered. Record available options and supervision latency;
do not assume identical labels or plan features. Confirm live status and use a vendor
test notification if available. Real alarm-event delivery still needs supervised tests.
EyezOn offers push alerts and network supervision, independently of HA:
[vendor features](https://www.eyezon.com/evl4.php).

## 4. Enable local integration after bootstrap validation

1. Confirm wiring, Keybus communication, stable LAN address and local login. Verify
   the partition and zone map at the keypad without triggering alarms; account for
   any 24-hour zones before opening contacts.
2. Copy `examples/secrets.example.yaml` to `runtime/config/secrets.yaml`; enter local
   EVL credentials privately. EyezOn credentials are different. Never store an alarm code.
3. Copy `examples/envisalink.yaml` to `runtime/config/packages/envisalink.yaml`.
   Confirm partition 1 or replace it. Add every verified zone number and a neutral name.
4. Run the native configuration check again, then restart only HA. Inspect its logs
   locally for login/setup errors. Do not paste unredacted logs or attributes into chat.
5. In Developer Tools > States, identify actual alarm, keypad and contact entity IDs.
   Update `runtime/config/dashboards/alarm.yaml`; add each contact to an entities card.
   Confirm changes match the keypad and each physical contact, including restore to closed.

The built-in integration uses local credentials and TCP 4025, with `evl_version: 4`.
It requires configured partitions/zones; IDs cannot be inferred safely from room names.
Omitting `code` requests user input for control. Do not assume this prevents code-free
arming permitted by the panel. See [integration configuration](https://www.home-assistant.io/integrations/envisalink/).

## 5. iPhone, health and notifications

After local onboarding, follow SECURITY.md's restricted remote-access design if using
Tailscale. Verify phone access and policy before relying on it. For ordinary LAN access,
set `HA_BIND_IP` in ignored `.env` to the Windows host's reserved trusted
LAN address, recreate the container, and permit TCP 8123 only from trusted clients on
the Private Windows network profile. Have the user review any administrator firewall
changes. Never use an unrestricted router forward. Validate the binding on the target host.
Private `compose.override.yaml` files load automatically with ordinary `docker compose`
commands; inspect the resolved configuration before applying any deployment change.
Register the iPhone using the official HA Companion App and grant notification permission.
Find its actual `notify.mobile_app_...` action in Developer Tools > Actions. A benign
test message to your own phone is manual setup, not an alarm test.

In Settings > Automations & scenes > Blueprints, create an automation from
`Alarm state notifications`, choosing the real partition and phone action. The three
provided blueprints send only notifications. The optional contact blueprint is opt-in.
They become active only after you instantiate them; copied blueprints alone do nothing.
Normal state alerts suppress startup unknown/unavailable transitions; triggered is not
suppressed. Configure iOS Focus, preview privacy and delivery preferences, and test
locked-screen reception. Critical alert behavior is not enabled or claimed by these files.
[Companion notify actions](https://companion.home-assistant.io/docs/notifications/notifications-basic/).

Add the built-in Ping integration via Settings > Devices & services for the EVL address.
Verify its binary connectivity entity with a planned outage, then instantiate the health
blueprint with fault state `off`. This detects host reachability only, not a stuck TPI
session. Review native Envisalink logs too. Live end-to-end communications-loss detection
remains an acceptance gate; do not declare it solved by Ping or cached alarm state.

For panel trouble, inspect the real keypad status attributes and confirm which boolean
reflects the keypad trouble indicator. `examples/trouble.yaml` is a disabled template:
replace the entity and attribute placeholders only after verifying semantics, then copy
to packages and validate. Instantiate the health blueprint for the resulting trouble
binary sensor with fault state `on`. If no trustworthy trouble signal is exposed, leave
this unconfigured and record the gap; verify EyezOn trouble delivery separately. Neither
HA nor mobile push can guarantee reporting its own host/internet failure.

## 6. Remote access and control

Follow SECURITY.md to choose Home Assistant Cloud or a restricted VPN. Account creation,
subscription selection and private credentials are user tasks. Verify cellular access
before relying on it. After supervised control approval, add `examples/control-card.yaml`
to the dashboard using the actual entity ID and test authorized arm/disarm with an
onsite operator. Never invoke alarm trigger or panel keypress tools during development.

Complete TEST_PLAN.md and keep evidence privately. See RECOVERY.md for rollback and
sleep/reboot recovery. Installation is incomplete until real-system acceptance passes.
