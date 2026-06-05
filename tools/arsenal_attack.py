"""
Arsenal attack tool — run a full red/blue team operation against a target.
Usage: arsenal_attack(target="192.168.8.51", attack_type="full-audit")
"""
import json, subprocess, os

ARSENAL_HOME = os.environ.get("ARSENAL_HOME", os.path.expanduser("~/projects/arsenal-cli"))

def arsenal_attack(target: str, attack_type: str = "full-audit", json_mode: bool = False) -> str:
    """Run a full attack operation against a target using Arsenal CLI.

    Phases: recon → skill selection → execution → report → lateral movement.

    Args:
        target: Domain, IP, or URL to attack
        attack_type: Attack profile — full-audit, quick-scan, web-app, api-audit, blue-team
        json_mode: If True, return structured JSON for agent consumption
    """
    cmd = ["node", f"{ARSENAL_HOME}/dist/index.js", "attack", target, "-t", attack_type]
    if json_mode:
        cmd.append("--json")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=120,
            cwd=ARSENAL_HOME
        )
        output = result.stdout or result.stderr
        if not output:
            return "No output from Arsenal attack."
        return output[:8000]
    except subprocess.TimeoutExpired:
        return "Attack timed out after 120s."
    except Exception as e:
        return f"Arsenal attack failed: {e}"

# ── Hermes Tool Registry ──────────────────────────────────────────────────────
try:
    from tools.registry import registry

    registry.register(
        name="arsenal_attack",
        toolset="arsenal",
        schema={
            "name": "arsenal_attack",
            "description": "Run a full red/blue team attack operation against a target. 5 phases: recon, skill selection, exploitation, report, lateral movement. Uses 764 built-in cybersecurity skills.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Target domain, IP, or URL to attack"},
                    "attack_type": {"type": "string", "enum": ["full-audit", "quick-scan", "web-app", "api-audit", "blue-team"], "default": "full-audit", "description": "Attack profile type"},
                    "json_mode": {"type": "boolean", "default": False, "description": "Return structured JSON output"},
                },
                "required": ["target"],
            },
        },
        handler=lambda args, **kw: arsenal_attack(
            target=args.get("target", ""),
            attack_type=args.get("attack_type", "full-audit"),
            json_mode=args.get("json_mode", False),
        ),
        check_fn=lambda: os.path.isdir(ARSENAL_HOME),
        requires_env=["ARSENAL_HOME"],
    )
except ImportError:
    pass
