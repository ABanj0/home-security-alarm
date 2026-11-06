# Implementation roadmap

This roadmap describes deployment gates, not the state of a particular installation.
Keep host observations, account setup, zone maps and dated evidence under ignored `private/`.
See VALIDATION.md for software checks and TEST_PLAN.md for supervised acceptance.

## Milestones

| ID | Work and dependencies | Required evidence |
|---|---|---|
| M0 | Inspect inventory and agree architecture | Verified hardware inventory and architecture review |
| M1 | Bootstrap HA Container; needs Linux Docker engine | Compose validation, native configuration check, healthy UI and owner onboarding |
| M2 | Establish keypad baseline; technician verifies EVL and Ethernet | Safe installation, power budget, normal keypad, Keybus and LAN status |
| M3 | Reserve IP, change local credentials, activate EyezOn; needs M2 | Live status matches keypad; independent iPhone notification |
| M4 | Enable supported Envisalink integration; needs M1-M3 | Native check, verified partition/zone map and every sensor transition |
| M5 | Map dashboard, control and health signals; needs M4 | Correct entities, unknown health stays unknown, authorized control test |
| M6 | Configure HA and EyezOn event alerts; needs phone registration and M4-M5 | Triggered/armed/disarmed/trouble/loss delivery with timestamps |
| M7 | Secure remote access; needs HA user and cloud/VPN choice | Cellular access and router/IPv6 review showing no direct alarm exposure |
| M8 | Supervised acceptance, outages, restore and handover | All applicable TEST_PLAN rows have evidence and recovery passes |

M1 can proceed independently of physical installation. M2-M3 must precede enabling
integration. Notification blueprints can be prepared before M4; enabling them requires
verified entities. Files, TCP connectivity and container health do not establish alarm acceptance.

## Decisions and stop points

The provided deployment targets HA Container on Windows with Docker/WSL2. Validate
Docker networking, host sleep, reboot and startup behavior. Consider a dedicated supported
host if uptime requirements cannot be met; record deployment choices privately.
Use the built-in Envisalink integration rather than custom panel protocol code.

Prepare monitoring first; manually controlled arm/disarm remains an acceptance requirement.
No automatic arm/disarm/trigger/bypass/PGM actions are included. DSC programming requires
explicit approval. Wiring, siren and outage exercises are manual supervised tasks.

Complete bootstrap checks and owner onboarding before entering credentials privately.
Confirm partition assignment and every zone before enabling integration. Verify EyezOn
account setup and phone registration independently of Home Assistant.

Sources: [EyezOn compatibility](https://www.eyezon.com/evl4.php),
[Envisalink integration](https://www.home-assistant.io/integrations/envisalink/).
