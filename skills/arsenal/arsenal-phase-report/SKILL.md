---
name: arsenal-phase-report
description: Phase 4 — Report. Compile execution findings into a structured markdown report. Triggered by arsenal-phase-execute when EXECUTION_COMPLETE is found.
---

# Arsenal Phase 4 — Report Compilation

Take execution results from all targets and compile a comprehensive markdown report.
Save to disk and prepare for notification delivery.

## Instructions

1. Parse all EXECUTION_COMPLETE blocks from the input

2. For the report file, use this path:
   - `/home/dazeb/projects/arsenal-cli/reports/scan-{YYYY-MM-DD}.md`

3. Report structure:

```markdown
# Arsenal Lab Scan Report — {DATE}

**Pipeline:** recon → skill-match → execute → report
**Generated:** {timestamp}
**Targets scanned:** {count}
**Findings:** {total findings count}

---

## Target: {target_name}
- **Type:** {docker|lxc}
- **IP:Port:** {ip:port}
- **Services:** {comma-separated list}

### Findings

| # | Severity | Skill | Finding | Proof |
|---|----------|-------|---------|-------|
| 1 | HIGH | exploiting-sql-injection-vulnerabilities | Error-based SQLi in search.php | DB version extracted: 8.0.35 |
| 2 | MEDIUM | testing-for-xss-vulnerabilities | Reflected XSS in comment field | alert() executed |

### Flags Captured
- `CTF{sqli_error_based_extraction}` — SQL injection
- `CTF{xss_reflected_comment}` — Cross-site scripting

### Skipped Tests
- `ssh-hardening-assessment` — ssh-audit tool not installed
- `csrf-testing` — No state-changing forms found

### Recommendations
1. Sanitize SQL inputs with parameterized queries
2. Implement Content-Security-Policy header
3. ...

---

## Summary

| Metric | Value |
|--------|-------|
| Targets scanned | {count} |
| Skills executed | {executed} |
| Skills skipped | {skipped} |
| Findings (CRITICAL) | {critical_count} |
| Findings (HIGH) | {high_count} |
| Findings (MEDIUM) | {medium_count} |
| Flags captured | {flag_count} |
| Duration | {duration} |

## Pipeline Chain
starter → recon → skill-match → execute → report → notify
```

4. Write the report file to `/home/dazeb/projects/arsenal-cli/reports/scan-{date}.md`

5. Also output a compact summary for notification:

```
REPORT_READY: /home/dazeb/projects/arsenal-cli/reports/scan-{date}.md
  targets: {count}
  findings: {total} ({critical} CRIT, {high} HIGH, {medium} MED)
  flags: {count}
  duration: {duration}
```

## Chaining Configuration

on_complete:
  - trigger: arsenal-phase-notify
    condition: "output contains REPORT_READY"
    pass_output: true
