# Hermes Arsenal Plugin

> Agent-driven offensive security lab — 764 cybersecurity skills, 22 vulnerable lab targets, 5-phase attack workflow with automated pipeline chaining.

## Overview

The Arsenal plugin integrates the [Arsenal CLI](https://github.com/dazeb/arsenal-cli) into Hermes agents. When you ask an agent to "attack this target," "pentest this server," or "run recon against this domain," it follows a structured 5-phase methodology backed by 764 curated skills.

**v0.3.0** adds automated pipeline chaining — skills trigger each other via `on_complete` conditions, ending with a Telegram notification. One cron job runs the full chain unattended.

## Quick Install

```bash
# Requires Arsenal CLI installed and ARSENAL_HOME set
git clone https://github.com/dazeb/hermes-arsenal-plugin ~/projects/hermes-arsenal-plugin
hermes plugins install ~/projects/hermes-arsenal-plugin

# Start with arsenal tools enabled
hermes --toolsets arsenal
```

## Tools Provided (arsenal toolset)

| Tool | Purpose |
|------|---------|
| `arsenal_skill_list` | Browse 764 skills across 11 groups |
| `arsenal_skill_show` | Read a skill's full playbook |
| `arsenal_skill_stats` | Group → category breakdown |
| `arsenal_recon` | Run nmap, dig, curl, openssl recon |
| `arsenal_attack` | Full 5-phase attack pipeline |
| `arsenal_lab_targets` | Browse 22 lab targets |
| `arsenal_lab_info` | Target details + flags |

## Skills

| Skill | Purpose | Chains To |
|-------|---------|-----------|
| `arsenal-agent` | 5-phase manual attack workflow | report, notify |
| `arsenal-pipeline-starter` | Cron entry — check/start lab targets | recon, notify (fail) |
| `arsenal-phase-recon` | Deploy labs + nmap/dig/curl/openssl recon | skill-match, notify (no targets) |
| `arsenal-phase-skill-match` | Map findings to 764-skills via SQLite matcher | execute, notify (no skills) |
| `arsenal-phase-execute` | Run exploit playbooks (non-destructive first) | report, notify (critical find) |
| `arsenal-phase-report` | Compile markdown report | notify |
| `arsenal-phase-notify` | Telegram delivery (terminal node) | — |

## Pipeline

```
arsenal-pipeline-starter (cron: daily 3am)
  → arsenal-phase-recon (deploy + recon targets)
    → arsenal-phase-skill-match (map findings to skills)
      → arsenal-phase-execute (run exploit playbooks)
        → arsenal-phase-report (compile markdown report)
          → arsenal-phase-notify (Telegram delivery)
```

Each skill has dual exit paths: success chains forward, failure routes directly to notify.

### Setup the Cron Pipeline

```bash
# In a Hermes session:
# 1. Load the starter skill
/hermes skill load arsenal-pipeline-starter

# 2. Create the cron job (daily at 3am UTC)
/hermes cron create \
  --name "Arsenal daily lab scan" \
  --schedule "0 3 * * *" \
  --skill arsenal-pipeline-starter \
  --deliver telegram \
  "Run the Arsenal automated lab scan pipeline."
```

### Manual Trigger

From any Hermes session: mention "scan my lab targets" or "run the arsenal pipeline" and the agent loads `arsenal-pipeline-starter`.

## Edge Cases Handled

| Scenario | Behavior |
|----------|----------|
| No Docker available | Starter emits FAILED → notify |
| No targets reachable | Recon emits NO_TARGETS → notify |
| No skills match services | Skill-matcher emits NO_SKILLS → notify |
| Critical finding mid-execute | Execute chains to notify immediately |
| All tools missing | Each phase skips with reason, chains to report |
| Partial success | Report includes succeeded + failed + skipped |

## Skill Groups (764 Total)

| Group | Count | Focus |
|-------|-------|-------|
| recon | 149 | Subdomain enum, port scanning, DNS recon |
| defense | 132 | SOC, IR, endpoint security, phishing |
| cloud | 109 | AWS/Azure/GCP, containers, Kubernetes |
| web | 74 | SQLi, XSS, CSRF, API security |
| network | 74 | Network security, OT/ICS, wireless |
| exploit | 50 | Pen testing, red team, privesc |
| identity | 54 | IAM, zero trust, Active Directory |
| specialized | 51 | Crypto, mobile, firmware, supply chain |
| malware | 39 | Malware analysis, reverse engineering |
| vuln-mgmt | 25 | Vulnerability management, SSVC triage |
| compliance | 7 | GRC, privacy |

## Requirements

- Node.js (for Arsenal CLI)
- nmap, dig, curl, openssl
- ARSENAL_HOME environment variable pointing to Arsenal CLI installation
- Docker (for lab targets)
- Proxmox host at 192.168.8.111 (for LXC targets)

## Repository

- **Plugin:** https://github.com/dazeb/hermes-arsenal-plugin
- **Arsenal CLI:** https://github.com/dazeb/arsenal-cli
- **Skills source:** OpenHack redteam collection (764 SKILL.md files)

## License

MIT
