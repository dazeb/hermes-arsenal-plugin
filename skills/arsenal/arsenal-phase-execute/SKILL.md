---
name: arsenal-phase-execute
description: Phase 3 — Execution. Run matched exploit playbooks against lab targets. Triggered by arsenal-phase-skill-match when SKILLS_MATCHED is found.
---

# Arsenal Phase 3 — Execution

Execute the matched skill playbooks against each target. This phase runs the actual
exploitation: tool commands, payload delivery, and verification steps from each skill's SKILL.md.

## Instructions

1. Parse the incoming SKILLS_MATCHED blocks — each target with its prioritized skill list

2. For each target, work through the matched skills in priority order (highest score first)

3. For each skill:
   - Read the full playbook: `arsenal_skill_show(skill_id="<skill_id>")`
   - Note the exact commands, tools, and expected output
   - If the skill requires tools not installed, skip with note
   - If prerequisites aren't met, skip with note
   - Execute the playbook steps via terminal

4. Execution guidelines:
   - Recon-based skills (scanning, enumeration): safe to run automated
   - Exploit skills (sqli, xss, injection): run carefully, prefer non-destructive tests
   - Brute force: ONLY if the lab is specifically for brute force practice — otherwise skip
   - Metasploit: only for lab targets, never against production

5. Record results per skill:
   - What succeeded — capture output snippets, flags found
   - What failed — error messages, tool missing, target not vulnerable
   - What was skipped — and why (missing tool, prerequisite not met, destructive)

6. For web targets, prefer these non-destructive tests first:
   - SQLi: test with sleep-based payloads, boolean blind, error-based
   - XSS: test with alert or console log probes
   - CSRF: check for missing tokens on state-changing requests
   - File inclusion: test read-only endpoint access first
   - File upload: test extension bypass, not actual shell upload

7. For each flag or vulnerability found, capture:
   - The finding (what was vulnerable)
   - The proof (output/flag)
   - The skill that found it
   - Severity estimate (critical/high/medium/low)

8. Output execution results:

```
EXECUTION_COMPLETE: <target_name>
  SUCCESS: exploiting-sql-injection-vulnerabilities
    Finding: Error-based SQLi in /search.php?id= parameter
    Proof: ExtractValue returned database version: 8.0.35
    Flag: CTF{sqli_error_based_extraction}
    Severity: HIGH
  FAILED: testing-for-xss-vulnerabilities
    Reason: No reflected input fields found on target
  SKIPPED: implementing-ssh-hardening-assessment
    Reason: ssh-audit not installed

EXECUTION_COMPLETE: <next_target>
  ...
```

## Chaining Configuration

on_complete:
  - trigger: arsenal-phase-report
    condition: "output contains EXECUTION_COMPLETE"
    pass_output: true
  - trigger: arsenal-phase-notify
    condition: "output contains CRITICAL"
    pass_output: true
