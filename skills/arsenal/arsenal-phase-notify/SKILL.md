---
name: arsenal-phase-notify
description: Phase 5 — Notification. Deliver pipeline results via Telegram message. Terminal link for any phase — starter failure, recon no-targets, execution critical findings, or final report.
---

# Arsenal Phase 5 — Notification

Deliver pipeline results to the user via Telegram. This is the terminal node of the chain
and receives output from any phase that hits an early-exit condition or the final report.

## Instructions

1. Determine what triggered this notification:
   - From **arsenal-pipeline-starter** (FAILED): No lab targets running, Docker not available, deploy failed
   - From **arsenal-phase-recon** (NO_TARGETS): Recon found no accessible services
   - From **arsenal-phase-skill-match** (NO_SKILLS): No matching skills for the detected services
   - From **arsenal-phase-execute** (CRITICAL): A CRITICAL severity finding was discovered → immediate alert
   - From **arsenal-phase-report** (REPORT_READY): Final report is complete

2. Compose a Telegram message appropriate to the trigger:

   **FAILED / NO_TARGETS / NO_SKILLS → Short alert:**
   ```
   ⚔️ Arsenal Pipeline — {STATUS}
   {brief description of what went wrong}
   Check `arsenal lab list` or `docker ps` to debug.
   ```

   **CRITICAL finding → Priority alert:**
   ```
   🚨 Arsenal — CRITICAL Finding
   Target: {target_name}
   Finding: {description}
   Proof: {proof}
   Flag: {flag}
   ```

   **REPORT_READY → Full summary:**
   ```
   ⚔️ Arsenal Pipeline — Complete
   📅 {date} | 🎯 {N} targets | 🔍 {M} findings
   🏁 {F} flags captured
   📄 Report: {path}
   ```

3. Send via `send_message` tool:
   - Target: `telegram`
   - Message: the composed notification text

4. Log completion: No further chaining — this is the terminal node.

## Chaining Configuration

# Terminal node — no on_complete triggers.
# Any phase can route here for error notifications or final delivery.
