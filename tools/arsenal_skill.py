"""
Arsenal skill tools — browse, search, and read the 764-skill catalog.
"""
import subprocess, os

ARSENAL_HOME = os.environ.get("ARSENAL_HOME", os.path.expanduser("~/projects/arsenal-cli"))

def arsenal_skill_list(group: str = "", search: str = "") -> str:
    """Browse the skill catalog. 764 skills across 11 groups.

    Args:
        group: Filter by group (recon, defense, cloud, web, network, exploit, malware, identity, specialized, vuln-mgmt, compliance)
        search: Free-text search across skill names and descriptions
    """
    cmd = ["node", f"{ARSENAL_HOME}/dist/index.js", "skill", "list"]
    if group:
        cmd.extend(["--group", group])
    if search:
        cmd.extend(["--search", search])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=ARSENAL_HOME)
        return (result.stdout or result.stderr or "No output")[:6000]
    except Exception as e:
        return f"Skill list failed: {e}"

def arsenal_skill_show(skill_id: str) -> str:
    """Read a skill's full playbook — tools, commands, verification steps.

    Args:
        skill_id: The skill ID to read (e.g. 'exploiting-sql-injection-vulnerabilities')
    """
    cmd = ["node", f"{ARSENAL_HOME}/dist/index.js", "skill", "show", skill_id]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=ARSENAL_HOME)
        return (result.stdout or result.stderr or "Skill not found")[:8000]
    except Exception as e:
        return f"Skill show failed: {e}"

def arsenal_skill_stats() -> str:
    """Show group → category breakdown of all 764 skills."""
    cmd = ["node", f"{ARSENAL_HOME}/dist/index.js", "skill", "stats"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=ARSENAL_HOME)
        return (result.stdout or result.stderr or "No output")[:6000]
    except Exception as e:
        return f"Stats failed: {e}"

try:
    from tools.registry import registry

    registry.register(
        name="arsenal_skill_list",
        toolset="arsenal",
        schema={
            "name": "arsenal_skill_list",
            "description": "Browse the Arsenal skill catalog. 764 skills organized in 11 groups, 40+ categories. Use --group to drill down, --search for free-text queries.",
            "parameters": {
                "type": "object",
                "properties": {
                    "group": {"type": "string", "description": "Filter by group name (recon, defense, cloud, web, network, exploit, malware, identity, specialized, vuln-mgmt, compliance)"},
                    "search": {"type": "string", "description": "Free-text search across skill names/descriptions"},
                },
            },
        },
        handler=lambda args, **kw: arsenal_skill_list(
            group=args.get("group", ""),
            search=args.get("search", ""),
        ),
        check_fn=lambda: os.path.isdir(ARSENAL_HOME),
        requires_env=["ARSENAL_HOME"],
    )

    registry.register(
        name="arsenal_skill_show",
        toolset="arsenal",
        schema={
            "name": "arsenal_skill_show",
            "description": "Read a skill's full playbook. Skills are SKILL.md documents containing attack procedures, tool commands, verification steps, and pitfalls.",
            "parameters": {
                "type": "object",
                "properties": {
                    "skill_id": {"type": "string", "description": "The skill ID to read"},
                },
                "required": ["skill_id"],
            },
        },
        handler=lambda args, **kw: arsenal_skill_show(skill_id=args.get("skill_id", "")),
        check_fn=lambda: os.path.isdir(ARSENAL_HOME),
        requires_env=["ARSENAL_HOME"],
    )

    registry.register(
        name="arsenal_skill_stats",
        toolset="arsenal",
        schema={
            "name": "arsenal_skill_stats",
            "description": "Show group → category breakdown with counts for all 764 skills.",
            "parameters": {"type": "object", "properties": {}},
        },
        handler=lambda args, **kw: arsenal_skill_stats(),
        check_fn=lambda: os.path.isdir(ARSENAL_HOME),
        requires_env=["ARSENAL_HOME"],
    )
except ImportError:
    pass
