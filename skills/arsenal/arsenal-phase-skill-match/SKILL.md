---
name: arsenal-phase-skill-match
description: Phase 2 — Skill Selection. Map recon findings to specific exploit skills from the 764-skill catalog. Triggered by arsenal-phase-recon when RECON_COMPLETE is found.
---

# Arsenal Phase 2 — Skill Matching

Take recon output and map every finding to specific exploit skills from the 764-skill catalog.
Use the Arsenal skill search and the skill-matcher engine to find the best matches.

## Instructions

1. Parse incoming RECON_COMPLETE blocks — each target's ports, services, web tech

2. For each finding, query matching skills:
   - **Web server found** → `arsenal_skill_list(group="web")`, then drill to `arsenal_skill_list(search="<tech>")`
   - **MySQL/PostgreSQL** → `arsenal_skill_list(search="sqli")` or `arsenal_skill_list(search="sql injection")`
   - **SSH open** → `arsenal_skill_list(search="ssh")`, `arsenal_skill_list(search="brute force")`
   - **Login page** → `arsenal_skill_list(search="authentication")`, `arsenal_skill_list(search="credential")`
   - **Apache/IIS/Nginx specific** → `arsenal_skill_list(search="<server>")` for version-specific CVEs
   - **WordPress** → `arsenal_skill_list(search="wordpress")`, `arsenal_skill_list(search="cms")`
   - **API endpoints** → `arsenal_skill_list(search="api")`, `arsenal_skill_list(search="injection")`

3. For each matched skill, read the playbook:
   - `arsenal_skill_show(skill_id="<id>")` to get the exact attack procedure
   - Note which tools each skill requires (sqlmap, hydra, metasploit, curl, etc.)
   - Check if the target's services match the skill's prerequisites

4. Also run terminal-based skill matching for broader coverage:
   - `node dist/index.js skill list --search "<keyword>"` from the arsenal-cli directory

5. Build a prioritized execution plan:
   - High priority: skills that match open high-value services (web, DB, SSH)
   - Medium: skills matching detected tech stack versions
   - Lower: generic recon/deep-enum skills

6. Output the match plan:

```
SKILLS_MATCHED: <target_name>
  - exploiting-sql-injection-vulnerabilities (score: 85, group: web)
    → Matches: MySQL/8.0 on port 3306
    → Tools: sqlmap, curl, burp
    → Prerequisites met: YES (database accessible)
  - testing-for-xss-vulnerabilities (score: 72, group: web)
    → Matches: Apache/PHP web app
    → Tools: burp, curl, browser
    → Prerequisites met: YES (web forms found)
  - implementing-ssh-hardening-assessment (score: 45, group: network)
    → Matches: SSH on port 22
    → Tools: hydra, nmap, ssh-audit
    → Prerequisites met: PARTIAL (need cred list)
```

## Chaining Configuration

on_complete:
  - trigger: arsenal-phase-execute
    condition: "output contains SKILLS_MATCHED"
    pass_output: true
  - trigger: arsenal-phase-notify
    condition: "output contains NO_SKILLS"
    pass_output: true
