# home-security-alarm

DSC PC1616 + EnvisaLink 4 + independent EyezOn alerts + Home Assistant for iPhone.
This repository provides a disconnected Home Assistant bootstrap, notification
blueprints, and disabled integration examples. Software checks do not establish
live alarm acceptance. Keep deployment observations and acceptance evidence private.

Start with [ROADMAP.md](ROADMAP.md) and [SETUP.md](SETUP.md).

- [HLD.md](HLD.md): architecture and requirements
- [SECURITY.md](SECURITY.md): credentials and remote access
- [TEST_PLAN.md](TEST_PLAN.md): acceptance gates
- [VALIDATION.md](VALIDATION.md): software checks and validation limits
- [RECOVERY.md](RECOVERY.md): backup, restore and troubleshooting
- `config/`: bootstrap and notification blueprints
- `examples/`: disabled integration, secrets, trouble and control-card examples

Run `python scripts/prepare.py` once to stage the bootstrap under ignored `runtime/`.
It refuses to overwrite an existing installation. Follow SETUP before starting Docker
or enabling hardware integration. Never commit private runtime files or alarm codes.
