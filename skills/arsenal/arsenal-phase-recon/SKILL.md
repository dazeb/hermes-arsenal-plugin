---
name: arsenal-phase-recon
description: Phase 1 — Reconnaissance. Run nmap, dig, curl, openssl against lab targets. Triggered by arsenal-pipeline-starter when TARGETS_READY is found.
---

# Arsenal Phase 1 — Reconnaissance

Run full reconnaissance against all ready targets. Use the Arsenal CLI recon tools
plus direct terminal commands for deeper scanning.

## Instructions

1. Parse the incoming output for TARGETS_READY line:
   - Format: `TARGETS_READY: name|IP:port|type, name|IP:port|type`
   - Extract each target's name, IP, port, and type

2. For each Docker target:
   - Run `arsenal_recon(target="<IP>", operation="all")` to gather: subdomain enum, DNS recon, port scan, tech detection, cert scan, HTTP probe
   - Record open ports and services detected
   - Capture HTTP response headers and body snippets for tech fingerprinting

3. For each Proxmox LXC target:
   - SSH to the Proxmox host (192.168.8.111) to run internal recon if needed
   - Run `arsenal_recon(target="<IP>", operation="all")`
   - Time-based attacks need to run from inside the LXC — note this for later

4. For each target found, compile recon findings:
   - List open ports and services
   - Identify web frameworks (Apache, Nginx, Tomcat, Node, PHP, Python)
   - Note database services (MySQL, PostgreSQL, MongoDB)
   - Note any auth portals, admin panels, login pages

5. Output findings in structured format:

```
RECON_COMPLETE: <target_name>
  ports: 80(http), 443(https), 22(ssh), 3306(mysql)
  web: Apache/2.4.41, PHP/7.4, WordPress
  db: MySQL/8.0 on :3306
  notes: Login page at /wp-admin, XML-RPC enabled

RECON_COMPLETE: <next_target>
  ...
```

## Chaining Configuration

on_complete:
  - trigger: arsenal-phase-skill-match
    condition: "output contains RECON_COMPLETE"
    pass_output: true
  - trigger: arsenal-phase-notify
    condition: "output contains NO_TARGETS"
    pass_output: true
