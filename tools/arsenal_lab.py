"""
Arsenal lab tool — manage vulnerable Docker and Proxmox LXC targets.
"""
import subprocess, os

ARSENAL_HOME = os.environ.get("ARSENAL_HOME", os.path.expanduser("~/projects/arsenal-cli"))

def arsenal_lab_targets() -> str:
    """List all 22 vulnerable lab targets (Docker + Proxmox LXC)."""
    cmd = ["node", f"{ARSENAL_HOME}/dist/index.js", "lab", "targets"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=ARSENAL_HOME)
        return (result.stdout or result.stderr or "No output")[:6000]
    except Exception as e:
        return f"Lab targets failed: {e}"

def arsenal_lab_info(target: str) -> str:
    """Get detailed info about a lab target — ports, skills, flags, deploy instructions.

    Args:
        target: Target name (e.g. dvwa, sqli-labs, proxmox-ssrf)
    """
    cmd = ["node", f"{ARSENAL_HOME}/dist/index.js", "lab", "info", target]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=ARSENAL_HOME)
        return (result.stdout or result.stderr or "Target not found")[:5000]
    except Exception as e:
        return f"Lab info failed: {e}"

try:
    from tools.registry import registry

    registry.register(
        name="arsenal_lab_targets",
        toolset="arsenal",
        schema={
            "name": "arsenal_lab_targets",
            "description": "Browse the catalog of 22 vulnerable lab targets — Docker containers (DVWA, Juice Shop, WebGoat) and Proxmox LXC templates (SQLi, CMDi, LFI, SSRF).",
            "parameters": {"type": "object", "properties": {}},
        },
        handler=lambda args, **kw: arsenal_lab_targets(),
        check_fn=lambda: os.path.isdir(ARSENAL_HOME),
        requires_env=["ARSENAL_HOME"],
    )

    registry.register(
        name="arsenal_lab_info",
        toolset="arsenal",
        schema={
            "name": "arsenal_lab_info",
            "description": "Get detailed info about a specific lab target: ports, relevant skills, difficulty, flags, and deploy instructions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Target name (dvwa, sqli-labs, juiceshop, proxmox-ssrf, etc.)"},
                },
                "required": ["target"],
            },
        },
        handler=lambda args, **kw: arsenal_lab_info(target=args.get("target", "")),
        check_fn=lambda: os.path.isdir(ARSENAL_HOME),
        requires_env=["ARSENAL_HOME"],
    )
except ImportError:
    pass
