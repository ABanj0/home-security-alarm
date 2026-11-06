# Software validation and limits

The public repository records source checks only. Deployment history and original
observations are retained under ignored `private/`; this document does not supersede
or certify those records. Live alarm acceptance requires the evidence in TEST_PLAN.md.

## Publication checks

Verify an export of the exact staged Git tree with:

- `python -m unittest discover -s tests -v`
- `python scripts/validate_yaml.py`
- `docker compose --file compose.yaml config --quiet`

Publication results, checked tree IDs and explicit skips belong in the ignored local
publication ledger. Secret scanning and manual review cover candidate content; private
runtime files, credentials, overrides and deployment observations are excluded.

## Required deployment checks

Before deployment, run Docker Compose parsing and Home Assistant's native configuration
checker as described in SETUP.md. Repeat native validation after enabling or changing
packages and blueprint instances. Syntax checks alone do not validate HA's runtime schema.

The example checker uses network isolation and synthetic credentials. It does not
validate a private zone map, live communication, phone delivery or hardware behavior.

Keypad/siren operation, all sensor transitions, both notification paths, trouble and
communications loss, cellular access, host uptime, encrypted backup and isolated restore
remain installation-specific acceptance requirements. Ping does not establish TPI session
health, and a stopped host cannot report its own failure through Home Assistant.
Never trigger alarms, change panel programming or interrupt a live network as part of
software publication checks.
