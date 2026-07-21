#!/usr/bin/env python3
"""Validate the repository-local Xuerong animation agent bundle."""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path


REQUIRED_AGENTS = {
    "xuerong_animation_builder": "workspace-write",
    "xuerong_deterministic_qa": "workspace-write",
    "xuerong_visual_quality_reviewer": "read-only",
    "xuerong_release_integrator": "workspace-write",
}
REQUIRED_AGENT_FIELDS = {"name", "description", "developer_instructions"}


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated YAML frontmatter")
    metadata: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.project_root.resolve()
    errors: list[str] = []

    skill = root / ".agents" / "skills" / "xuerong-animation-studio"
    skill_md = skill / "SKILL.md"
    if not skill_md.is_file():
        errors.append(f"missing {skill_md}")
    else:
        try:
            metadata = parse_frontmatter(skill_md)
            if metadata.get("name") != "xuerong-animation-studio":
                errors.append("SKILL.md has the wrong name")
            if not metadata.get("description"):
                errors.append("SKILL.md description is empty")
        except ValueError as error:
            errors.append(f"{skill_md}: {error}")

    for relative in (
        "agents/openai.yaml",
        "references/animation-standard.md",
        "references/state-recipes.md",
        "references/agent-handoffs.md",
    ):
        path = skill / relative
        if not path.is_file():
            errors.append(f"missing {path}")

    openai_yaml = skill / "agents" / "openai.yaml"
    if openai_yaml.is_file():
        yaml_text = openai_yaml.read_text(encoding="utf-8")
        if "$xuerong-animation-studio" not in yaml_text:
            errors.append("openai.yaml default_prompt must mention $xuerong-animation-studio")

    found: dict[str, str] = {}
    for path in sorted((root / ".codex" / "agents").glob("*.toml")):
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except Exception as error:
            errors.append(f"{path}: invalid TOML: {error}")
            continue
        missing = REQUIRED_AGENT_FIELDS - data.keys()
        if missing:
            errors.append(f"{path}: missing {sorted(missing)}")
            continue
        name = data["name"]
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", name):
            errors.append(f"{path}: invalid name {name!r}")
            continue
        if name in found:
            errors.append(f"duplicate agent name {name!r}")
        found[name] = data.get("sandbox_mode", "")
        if name in REQUIRED_AGENTS and "xuerong-animation-studio" not in data["developer_instructions"]:
            errors.append(f"{path}: does not invoke xuerong-animation-studio")

    for name, sandbox in REQUIRED_AGENTS.items():
        if name not in found:
            errors.append(f"missing agent {name}")
        elif found[name] != sandbox:
            errors.append(f"{name}: expected sandbox_mode={sandbox!r}, got {found[name]!r}")

    agents_md = root / "AGENTS.md"
    if not agents_md.is_file():
        errors.append("missing AGENTS.md")
    else:
        if agents_md.stat().st_size > 32 * 1024:
            errors.append("AGENTS.md exceeds the 32 KiB project-doc limit")
        if "xuerong-animation-studio" not in agents_md.read_text(encoding="utf-8"):
            errors.append("AGENTS.md does not document xuerong-animation-studio")

    config_example = root / ".codex" / "config.toml.example"
    if not config_example.is_file():
        errors.append("missing .codex/config.toml.example")
    else:
        try:
            tomllib.loads(config_example.read_text(encoding="utf-8"))
        except Exception as error:
            errors.append(f"{config_example}: invalid TOML: {error}")

    ownership_doc = root / "docs" / "agent-system" / "XUERONG_ANIMATION_AGENTS.md"
    if not ownership_doc.is_file():
        errors.append(f"missing {ownership_doc}")

    print(f"Project root: {root}")
    print(f"Xuerong agents: {len(REQUIRED_AGENTS & found.keys())}/{len(REQUIRED_AGENTS)}")
    for error in errors:
        print(f"ERROR: {error}")
    print("Validation: FAIL" if errors else "Validation: PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
