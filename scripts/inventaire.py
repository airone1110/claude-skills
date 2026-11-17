#!/usr/bin/env python3
"""Inventaire de tous les skills disponibles sur cette machine, regroupés par provenance.

Usage : scripts/inventaire.py [--court] [--sortie FICHIER.md]

Ne voit pas les skills ajoutés uniquement dans Claude Desktop / claude.ai
(Customize > Skills) ni les skills intégrés d'Anthropic : ceux-là se consultent
dans Claude Code avec /skills, ou dans Desktop sous Customize > Skills.
"""
import argparse
import json
import os
import re
from pathlib import Path

HOME = Path.home()
REPO = Path(__file__).resolve().parent.parent
USER_SKILLS = HOME / ".claude" / "skills"
PLUGINS_FILE = HOME / ".claude" / "plugins" / "installed_plugins.json"
PROJECTS = HOME / "Projets_code"


def frontmatter(path: Path) -> dict:
    """name/description du SKILL.md, y compris les descriptions sur plusieurs lignes (| ou >)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    meta, key = {}, None
    for line in (match.group(1).splitlines() if match else []):
        top = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if top:
            key, value = top.group(1), top.group(2).strip()
            meta[key] = "" if value in ("|", ">", "|-", ">-") else value.strip("\"'")
        elif key and line.startswith((" ", "\t")):
            meta[key] = (meta[key] + " " + line.strip()).strip()
    return meta


def skills_in(folder: Path):
    if not folder.is_dir():
        return []
    found = []
    for skill_md in sorted(folder.glob("*/SKILL.md")):
        meta = frontmatter(skill_md)
        found.append({"name": meta.get("name") or skill_md.parent.name, "description": meta.get("description", ""),
                      "path": skill_md, "real": skill_md.resolve()})
    return found


def collect():
    groups = []
    # 1. Ce dépôt : installé via le compte Claude → partout.
    for plugin in sorted((REPO / "plugins").glob("*/")):
        groups.append((f"mes-skills › {plugin.name}", "Desktop, claude.ai, Cowork, Code (via le compte)",
                       skills_in(plugin / "skills")))
    # 2. ~/.claude/skills : Claude Code uniquement, sur ce Mac.
    by_source = {}
    for skill in skills_in(USER_SKILLS):
        real = str(skill["real"])
        if "/gstack/" in real:
            source = "gstack (garrytan/gstack)"
        elif skill["name"].startswith("n8n-"):
            source = "n8n skills (czlonkowski)"
        else:
            source = "~/.claude/skills (autres)"
        by_source.setdefault(source, []).append(skill)
    for source, skills in sorted(by_source.items()):
        groups.append((source, "Claude Code (ce Mac)", skills))
    # 3. Plugins installés dans Claude Code.
    try:
        installed = json.loads(PLUGINS_FILE.read_text()).get("plugins", {})
    except (OSError, ValueError):
        installed = {}
    for plugin_id, installs in sorted(installed.items()):
        for install in installs[:1]:
            path = Path(install.get("installPath", ""))
            groups.append((f"plugin {plugin_id} v{install.get('version', '?')}", "Claude Code (ce Mac)",
                           skills_in(path / "skills")))
    # 4. Skills propres à un projet.
    for project in sorted(PROJECTS.glob("*/")):
        skills = skills_in(project / ".claude" / "skills")
        if skills:
            groups.append((f"projet {project.name}", f"Claude Code, dans {project.name} seulement", skills))
    return [g for g in groups if g[2]]


def render(groups, short: bool) -> str:
    total = sum(len(skills) for _, _, skills in groups)
    lines = [f"# Inventaire des skills ({total})", "",
             "| Provenance | Disponible dans | Nombre |", "|---|---|---|"]
    lines += [f"| {source} | {where} | {len(skills)} |" for source, where, skills in groups]
    lines += ["", "_Non listés ici : skills ajoutés dans Desktop/claude.ai (Customize › Skills) et skills intégrés "
                  "d'Anthropic. Voir `/skills` dans Claude Code._"]
    if short:
        return "\n".join(lines) + "\n"
    for source, where, skills in groups:
        lines += ["", f"## {source}", f"_{where}_", "", "| Skill | Description |", "|---|---|"]
        for skill in sorted(skills, key=lambda s: s["name"]):
            desc = re.sub(r"\s+", " ", skill["description"]).replace("|", "\\|")
            desc = desc if len(desc) <= 140 else desc[:137].rstrip() + "…"
            lines.append(f"| `{skill['name']}` | {desc} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--court", action="store_true", help="résumé par provenance seulement")
    parser.add_argument("--sortie", help="écrire dans un fichier Markdown au lieu de l'écran")
    args = parser.parse_args()
    output = render(collect(), args.court)
    if args.sortie:
        Path(args.sortie).write_text(output, encoding="utf-8")
        print(f"Écrit : {args.sortie}")
    else:
        print(output, end="")
