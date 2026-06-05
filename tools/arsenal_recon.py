"""
Arsenal recon tool — run reconnaissance operations against a target.
"""
import subprocess, os

ARSENAL_HOME = os.environ.get("ARSENAL_HOME", os.path.expanduser("~/projects/arsenal-cli"))

def arsenal_recon(target: str, operation: str = "all") -> str:
    """Run reconnaissance against a target.

    Args:
        target: Domain, IP, or URL
        operation: recon operation — all, subenum, dnsrecon, portscan, techdetect, certscan
    """
    if operation == "all":
        cmd = ["node", f"{ARSENAL_HOME}/dist/index.js", "recon", "all", target]
    else:
        cmd = ["node", f"{ARSENAL_HOME}/dist/index.js", "recon", operation, target]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90, cwd=ARSENAL_HOME)
        return (result.stdout or result.stderr or "No output")[:6000]
    except subprocess.TimeoutExpired:
        return "Recon timed out."
    except Exception as e:
        return f"Recon failed: {e}"

try:
    from tools.registry import registry
    registry.register(
        name="arsenal_recon",
        toolset="arsenal",
        schema={
            "name": "arsenal_recon",
            "description": "Run reconnaissance operations: port scanning (nmap), DNS enumeration (dig), HTTP tech detection (curl), SSL certificate analysis (openssl).",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Target domain, IP, or URL"},
                    "operation": {"type": "string", "enum": ["all", "subenum", "dnsrecon", "portscan", "techdetect", "certscan"], "default": "all", "description": "Recon operation to run"},
                },
                "required": ["target"],
            },
        },
        handler=lambda args, **kw: arsenal_recon(
            target=args.get("target", ""),
            operation=args.get("operation", "all"),
        ),
        check_fn=lambda: os.path.isdir(ARSENAL_HOME),
        requires_env=["ARSENAL_HOME"],
    )
except ImportError:
    pass
