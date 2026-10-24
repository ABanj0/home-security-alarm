# home-security-alarm

Home security with EyezOn Envisalink EVL-4EZR

## High-Level Design (HLD)

### 1) Objective
Provide a reliable and secure home alarm monitoring setup using the EyezOn Envisalink EVL-4EZR as the integration bridge between a traditional alarm panel and smart automation/notification systems.

### 2) Scope
- Integrate an existing alarm panel with Envisalink EVL-4EZR
- Enable remote status monitoring and event notifications
- Support optional local automation integrations (e.g., Home Assistant)
- Preserve alarm panel core behavior (arming/disarming/zones)

### 3) System Context
```text
[Sensors/Zones] -> [Alarm Panel] <-> [EVL-4EZR] <-> [Home LAN]
                                             |            |
                                             |            +--> [Local Automation Platform]
                                             |
                                             +--> [EyezOn Cloud Service] --> [User App/Web]
```

### 4) Core Components
1. **Alarm Panel**  
   Existing wired/wireless panel handling zones, arming states, and siren logic.
2. **EyezOn Envisalink EVL-4EZR**  
   Network module connected to the alarm panel keybus and home LAN; publishes panel state/events.
3. **Home Router / LAN**  
   Provides IP connectivity to EVL-4EZR; enforces network segmentation and firewall policy.
4. **EyezOn Cloud Service**  
   Receives panel events (via EVL) and provides remote access/notifications.
5. **Client Interfaces**  
   Mobile app/web for status, event history, and notifications.
6. **Local Automation (Optional)**  
   Consumes EVL events for home automations (lights, cameras, voice alerts).

### 5) Key Data Flows
1. **Zone Event Flow**
   - Sensor changes state (open/close, alarm, tamper)
   - Alarm panel updates zone state
   - EVL-4EZR captures event and forwards to cloud/local clients
   - Users receive push/email/SMS (based on service configuration)

2. **Arm/Disarm Command Flow**
   - User command originates from app/web or local automation
   - Command passes through EyezOn cloud (or local integration path)
   - EVL-4EZR sends keypad-equivalent command to panel
   - Panel confirms new state; event propagated back to clients

3. **Health/Heartbeat Flow**
   - EVL periodic connectivity checks with cloud
   - Alerting on communication failure, AC loss, battery/zone faults (if available from panel)

### 6) Non-Functional Requirements
- **Security**
  - Strong unique credentials for EyezOn account and local integrations
  - Isolate EVL device on trusted VLAN/segment where possible
  - Disable unnecessary inbound internet exposure; prefer outbound/cloud-initiated communications
- **Availability**
  - UPS for panel, EVL, and network gear
  - Internet outage should not affect local alarm triggering
- **Performance**
  - Near-real-time event propagation (typically seconds)
- **Maintainability**
  - Document panel zone mappings and automation rules
  - Maintain firmware/software update process for EVL, router, and automation platform

### 7) Deployment View
- EVL-4EZR physically mounted near alarm panel and wired to panel keybus
- EVL connected via Ethernet to home router/switch
- EyezOn account linked to EVL MAC/registration details
- Optional local automation integration configured using EVL local API/TPI credentials

### 8) Operational Considerations
- Keep a documented fallback for manual keypad operation
- Test alarm, arm/disarm, and notification paths monthly
- Audit user access to cloud and automation platforms
- Rotate integration credentials when household access changes
