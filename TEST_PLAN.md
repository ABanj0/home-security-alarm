# Validation and acceptance

This matrix is a template; deployment results belong in an ignored private copy.
Full acceptance requires actual evidence. Do not mark a test passed from
expected behavior, configuration presence or a successful test message alone.

## Software checks (non-disruptive)

Run `python -m unittest discover -s tests -v`, then `python scripts/validate_yaml.py`
after installing requirements-dev.txt in a local virtual environment. The first checks
staging and forbidden control actions; the second parses YAML and Jinja, references and
blueprint structure. Neither validates HA's full runtime schema. Run the network-isolated
native HA configuration check in SETUP.md before startup and after each package change.
Compose parsing does not need a running engine. Record actual results in VALIDATION.md.

`python scripts/check_prepared.py` additionally checks the public integration example and
four sample blueprint instances with HA's native checker in a separate container using
`--network none` and dummy credentials. It leaves ignored schema fixtures under private/.
Passing this check does not prove live communication or notification delivery.

## Live acceptance matrix

Record timestamp/timezone, operator, expected/actual result, private evidence location,
latency and pass/fail/not-run per row. Use a copy under `private/`; redact shared reports.

| ID | Procedure | Required evidence / acceptance | Status |
|---|---|---|---|
| AT-001 | Operator tests existing keypad arm/disarm before and after integration | States, entry/exit behavior unchanged | NOT RUN |
| AT-002 | After verifying zone types, open/close every mapped contact with appropriate safe state | Per-zone keypad, HA and EyezOn values match; no invented mapping | NOT RUN |
| AT-003 | With explicit supervised test agreement, trigger controlled intrusion | Local siren works; alarm event reaches EyezOn and HA iPhone alerts; latency recorded | NOT RUN |
| AT-004 | Operator performs planned arm/disarm | Both independent notification paths deliver each event on locked iPhone | NOT RUN |
| AT-005 | Planned WAN interruption with onsite operator | Keypad, sensor and siren behavior remain operational; note cloud loss and supervision delay | NOT RUN |
| AT-006 | Planned HA stop; keep EVL/router online | Keypad and local alarm work; EyezOn events still reach phone | NOT RUN |
| AT-007 | Check local EVL and HA authentication without brute force | Unauthenticated access cannot view/control protected data; MFA verified where available | NOT RUN |
| AT-008 | Review router IPv4/IPv6, UPnP/DMZ, Windows listener/firewall settings | No public EVL ports, no public direct HA listener; only intended LAN/cloud/VPN access | NOT RUN |
| AT-009 | Restore WAN/HA after AT-005/006 | Fresh events and correct current states resume; no assumed replay of missed events | NOT RUN |
| AT-010 | Technician checks panel/battery and trouble indicators | Adequate power and no unresolved trouble; existing problems documented | NOT RUN |
| AT-011 | Inspect physical installation and module status | Correct wiring, supported firmware, Keybus status and keypad agreement | NOT RUN |
| AT-012 | Complete HA bootstrap, restart and check dashboard | Healthy UI, live entities, every installed contact visible, no missing entity errors | NOT RUN |
| AT-013 | Authorized user tests HA and EyezOn arm/disarm with onsite operator | Intended partition obeys commands; unauthorized access denied; no panel programming changes | NOT RUN |
| AT-014 | User tests remote access over cellular | Authenticated HA and EyezOn status/control over chosen secure path; no direct EVL exposure | NOT RUN |
| AT-015 | Technician-approved trouble test (do not invent a fault by pulling wiring) | Keypad trouble and verified HA attribute agree; EyezOn/HA trouble notifications arrive | NOT RUN |
| AT-016 | Planned EVL network loss and separate TPI session failure while host remains reachable | Detect each failure via verified channel within recorded acceptable delay; cached state not mistaken for live | NOT RUN |
| AT-017 | Benign notify action, then actual event tests, phone locked/Wi-Fi and cellular | Permission/Focus settings and each real event delivery verified separately | NOT RUN |
| AT-018 | Windows reboot / Docker restart with operator present | HA resumes as intended; fresh zone events, secrets, notifications and dashboard preserved | NOT RUN |
| AT-019 | Restore encrypted backup into isolated configuration location | Native configuration check passes; correct files/version restored; no concurrent EVL client | NOT RUN |
| AT-020 | Optional contact activity | Selected contact opens generate only intended notifications; omit if not requested | NOT RUN |

AT-016 is deliberately broader than ICMP. If Ping succeeds while TPI is stalled and no
verified health signal notices, record **FAIL / unresolved** and resolve with supported
integration/vendor diagnostics before signing off. Health sensors must not map missing
or unknown data to healthy. Validate behavior both at startup and after disconnection.

Stop any live test if there is unexpected siren behavior, trouble, a wrong zone/partition,
loss of keypad control, or any unknown monitoring/dialer involvement. Restore normal
connectivity, use the existing keypad procedure and contact the installer if needed.
Warn occupants before siren tests; agree who disarms and how restoration is verified.
No automated test in this repository sends alarm control commands.

Completion requires AT-001 through AT-019 passing, with explicit resolutions for any
unsupported notification/health behavior. AT-020 is optional. A deliberate omission of
an original requirement needs user agreement, not a silent N/A.
