# Security and remote access

The DSC remains responsible for local detection, keypad, timing and siren. HA and
EyezOn are separate convenience/notification paths; they share EVL, network and power
failure risks. No professional dispatch is configured. No automated alarm control,
panic, bypass, custom keypress or PGM output is part of this implementation.

## Network boundaries

| Path | Policy |
|---|---|
| HA to EVL TCP 4025 | Trusted LAN only; limit source to HA host where router supports it |
| Local EVL administration | Trusted administrator devices only; never public |
| EVL to EyezOn | Supported outbound service traffic; consult vendor for firewall requirements |
| Windows TCP 8123 | Loopback initially; explicitly selected trusted LAN binding for iPhone |
| iPhone remote to HA | Authenticated Home Assistant Cloud or restricted VPN |
| WAN to EVL / HA | No router port forwarding, DMZ placement or UPnP mappings |

Also inspect IPv6 inbound firewall policies; absence of IPv4 NAT forwards alone is not
proof of isolation. Do not expose Docker's management API. Treat local EVL/TPI traffic
as sensitive on the LAN; a cloud encryption claim does not prove local protocol TLS.

One remote-access option is Tailscale on Windows and iPhone.
First verify they belong to the intended tailnet and review its access policy; membership
alone is not proof of restricted access. Limit access to the HA host and its UI port.
Do not advertise the alarm subnet or expose EVL administration. Verify policy and
listener settings on each deployment. Home Assistant Cloud remains an alternative.
[Official HA remote-access options](https://www.home-assistant.io/docs/configuration/remote/),
[Tailscale access controls](https://tailscale.com/docs/features/access-control).

After local onboarding, a candidate is binding Docker's HA port to the Windows Tailscale
IPv4 address via private `HA_BIND_IP`, with tailnet policy and host firewall restricted
to approved clients. This requires testing Docker Desktop's interface binding and phone
access before deployment. The loopback URL then changes to the host's
Tailscale address. Do not substitute a wildcard bind if this fails. Traffic between
Tailscale peers is carried through the VPN; keep HA authentication and MFA enabled.
Test cellular access, denial to unauthorized clients, and absence of ordinary LAN/WAN
exposure before sign-off. No exit node, subnet router, Funnel or public router forward
is required by this design. HA Container cannot install Supervisor add-ons.

## Credentials and authorization

Use unique supported EVL local credentials, a unique EyezOn password, MFA wherever
available, and HA MFA. Use individual HA accounts; keep administrator access limited.
Hiding a control card does not restrict service/API access. Do not give untrusted users
HA access based on a supposedly read-only dashboard. Review actual account privileges.
Do not save the DSC code in YAML, automations or notification actions. Runtime code
prompts do not alter DSC quick-arm policy; only explicit approval permits programming.

`runtime/`, `private/`, `.env` and secrets are ignored by Git. This is accidental-commit
protection, not encryption or filesystem access control. Restrict NTFS access to the
operator and required service identity, use device encryption, and encrypt backups.
HA `.storage`, logs, database and backups contain private data and tokens. Keep the repo
private; never paste codes, MAC IDs, credentials, detailed zone maps or unredacted logs.
Rotate exposed credentials and revoke lost-device sessions promptly.

## Failure and maintenance

Windows sleep, updates, Docker termination and WSL restarts interrupt HA. Configure and
verify host uptime with the user; `restart: unless-stopped` does not start Docker after
Windows login or wake a sleeping PC. EyezOn remains independent of the HA host but
depends on working EVL, internet and phone delivery. Test backup power; do not silently
change Windows power policy or panel wiring. Review access and relevant acceptance
tests after upgrades; avoid unattended image updates for the alarm integration.
