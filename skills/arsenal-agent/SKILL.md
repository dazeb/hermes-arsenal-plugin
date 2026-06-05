---
name: arsenal-agent
description: Arsenal offensive security agent — 5-phase attack workflow. When a user asks to attack, hack, pentest, or assess a target, follow this skill. 764 cybersecurity skills, 22 lab targets, real recon tools (nmap, dig, curl, openssl).
---

# Arsenal Agent — Offensive Security Workflow

You have access to the Arsenal CLI through these tools:
- `arsenal_skill_list` — browse 764 skills across 11 groups
- `arsenal_skill_show` — read a skill's full attack playbook
- `arsenal_skill_stats` — group → category breakdown
- `arsenal_recon` — run nmap, dig, curl, openssl recon
- `arsenal_attack` — full orchestrated attack pipeline
- `arsenal_lab_targets` — browse 22 vulnerable lab targets
- `arsenal_lab_info` — get target details + flags

## When to Use

A user asks you to:
- "attack this target"
- "hack example.com"
- "pentest 192.168.1.100"
- "run recon against this server"
- "check this web app for vulnerabilities"
- "do a security assessment"

## The 5-Phase Attack Workflow

Follow this workflow exactly. Do NOT skip phases. Each phase produces intel the next phase needs.

### Phase 0: Target Triage

1. Run `arsenal_skill_stats` to see what groups are available
2. Classify the target:
   - Domain/URL → groups: recon, web, exploit
   - IP address → groups: recon, network, exploit
   - Cloud asset → groups: cloud, recon
   - Internal host → groups: network, recon, exploit
   - Blue team drill → groups: defense, vuln-mgmt

### Phase 1: Reconnaissance

1. Run `arsenal_recon(target="<target>", operation="all")` to gather intel
2. Analyze the output:
   - **Port 80/443 open** → web application attack surface
   - **Port 22 open** → SSH — check for default creds later
   - **Port 3306/5432** → database — SQL injection opportunity
   - **Port 8080** → Tomcat/Jenkins — default credential attacks
   - **Apache/IIS/Nginx** → fingerprint the version, check for known CVEs
   - **HTML title/body** → what app is running?

### Phase 2: Skill Selection

Based on what recon found, browse matching skills:

```
arsenal_skill_list(group="web")       # If web app detected
arsenal_skill_list(search="sqli")     # If database detected
arsenal_skill_list(group="exploit")   # For exploitation techniques
arsenal_skill_list(group="network")   # For network attacks
```

For each relevant group, skills are organized by category. Read the group view to understand what's available.

When you find promising skills, read them with `arsenal_skill_show(skill_id="...")` to get the full playbook — what tools to use, what commands to run, what to look for.

### Phase 3: Execution

Read the selected skill's playbook, then execute its instructions using your own terminal. Skills tell you:
- What tools to use (nmap, sqlmap, curl, metasploit, hydra)
- What commands to run
- What output to expect
- How to verify success

Run the commands yourself. The skill is the playbook — you are the operator.

### Phase 4: Report

After each skill execution, tell the user:
- ✓ What succeeded
- ✗ What failed
- 🏁 Any flags captured
- What the next step should be

### Phase 5: Lateral Movement

If you gained access:

1. Run `arsenal_skill_list(group="exploit", search="privesc")` for privilege escalation paths
2. Run `arsenal_skill_list(group="network", search="pivot")` for lateral movement
3. Check for:
   - Other hosts on the network (ip neigh, arp -a, nmap scan adjacent IPs)
   - Credentials (config files, .env, bash_history, SSH keys)
   - Internal services (netstat -tlnp — services on localhost only)
   - Sudo rights, SUID binaries, writable cron jobs

Repeat Phases 1-4 for any new targets discovered.

## Lab Targets

22 vulnerable targets available for practice:

```
arsenal_lab_targets              # Browse catalog
arsenal_lab_info(target="dvwa")  # Get target details + flags
```

Docker targets run locally. Proxmox LXC targets deploy via the lab-targets/proxmox/ scripts.

## Proxmox Host

If the target is a lab on the Proxmox host:
- **Host**: 192.168.8.111
- **SSH**: root@192.168.8.111 (key: ~/.ssh/id_ed25519)
- **Storage**: local-zfs
- **Template**: local:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst
- Deploy labs: `bash lab-targets/proxmox/deploy.sh <name>`

## Skill Groups Reference

| Group | Count | What's Inside |
|-------|-------|---------------|
| recon | 149 | subdomain enum, port scanning, DNS recon, threat hunting, forensics |
| defense | 132 | SOC, incident response, endpoint security, phishing, ransomware |
| cloud | 109 | AWS/Azure/GCP, containers, Kubernetes, DevSecOps |
| web | 74 | SQLi, XSS, CSRF, API security, WebSocket, file upload |
| network | 74 | network security, OT/ICS, wireless, firewall |
| exploit | 50 | pen testing, red team, privesc, social engineering |
| identity | 54 | IAM, zero trust, Active Directory, MFA |
| specialized | 51 | crypto, mobile, firmware, supply chain, blockchain |
| malware | 39 | malware analysis, reverse engineering |
| vuln-mgmt | 25 | vulnerability management, SSVC triage |
| compliance | 7 | governance, risk, compliance, privacy |

## Automated Pipeline (Cron-Driven)

The Arsenal pipeline can run autonomously via skill chaining. The full pipeline:

```
arsenal-pipeline-starter (cron: daily 3am)
  → arsenal-phase-recon (deploy + recon targets)
    → arsenal-phase-skill-match (map findings to skills)
      → arsenal-phase-execute (run exploit playbooks)
        → arsenal-phase-report (compile markdown report)
          → arsenal-phase-notify (Telegram delivery)
```

Each phase is a standalone skill with `on_complete` triggers. When running in
automated/manual mode and you complete a full attack, chain into the report:

## Chaining Configuration

on_complete:
  - trigger: arsenal-phase-report
    condition: "output contains attack complete"
    pass_output: true
  - trigger: arsenal-phase-notify
    condition: "output contains FLAG"
    pass_output: true

## Rules

1. **Always recon first** — never attempt exploitation without recon intel
2. **Match skills to findings** — Apache found → web skills, MySQL found → SQLi skills
3. **Read the playbook before executing** — `arsenal_skill_show` gives you the exact procedure
4. **Report every result** — success or failure, tell the user
5. **Check lateral after success** — a foothold is not the end
6. **Never skip phases** — each phase produces intel the next phase depends on
