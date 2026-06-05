---
name: arsenal-pipeline-starter
description: Entry point for the Arsenal automated attack pipeline. Cron-triggered daily scan of lab targets. Chains through recon → skill-match → execute → report → notify.
---

# Arsenal Pipeline Starter

This is the scheduled entry point for the automated Arsenal attack pipeline.
Invoked by cron daily at 3am UTC, or manually when the user says "scan the lab."

## Instructions

1. First, list available lab targets:
   - `arsenal_lab_targets()` to see all Docker and Proxmox targets

2. For Docker targets that might be running, check their status:
   - Run `docker ps --format "{{.Names}}" 2>/dev/null || echo "no docker"` in terminal
   - If dvwa, juiceshop, or other targets are running, note their ports

3. If no targets are running, select one Docker target to deploy and scan:
   - Deploy with `arsenal lab start dvwa` via terminal (node dist/index.js lab start dvwa --detach)
   - Wait for it to come up (check with curl to the target)

4. For any Proxmox LXC targets, note that they must be already deployed and running

5. Produce a summary of targets ready for scanning:
   - List each target with IP:port
   - Note any that failed to start

## Pipeline Output

When finished, pass a target summary to the next phase. Output must contain:

```
TARGETS_READY: target1|IP:port|type, target2|IP:port|type
```

Example:
```
TARGETS_READY: dvwa|172.17.0.2:80|docker, proxmox-sqli|192.168.8.60:80|lxc
```

## Chaining Configuration

on_complete:
  - trigger: arsenal-phase-recon
    condition: "output contains TARGETS_READY"
    pass_output: true
  - trigger: arsenal-phase-notify
    condition: "output contains FAILED"
    pass_output: true
