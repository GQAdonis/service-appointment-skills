#!/usr/bin/env python3
"""Validate Agent Skills directories against the agentskills.io specification.

Stdlib only (no YAML dependency) — a focused check of the rules the spec
states explicitly, intended for local pre-commit use and CI alongside the
official `skills-ref validate`.

Checks per skill directory:
  * SKILL.md exists and starts with a YAML frontmatter block
  * name: 1-64 chars, [a-z0-9-], no leading/trailing/consecutive hyphens,
    equals the parent directory name
  * description: 1-1024 chars, non-empty
  * compatibility (optional): 1-500 chars
  * metadata (optional): simple string->string mapping
  * body under 500 lines (spec recommendation; warning only)
  * relative links in SKILL.md resolve to files inside the skill dir

Usage:
  validate_skills.py skills/service-appointment-coordinator
  validate_skills.py skills/*            # several
  validate_skills.py --root skills       # every direct subdirectory
Exit code 1 on any error; warnings don't fail.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


def parse_frontmatter(text: str) -> tuple[dict | None, str, list[str]]:
    """Minimal YAML subset: top-level `key: value` and one level of indented
    `key: value` mapping (for `metadata`). Returns (fm, body, errors)."""
    errs: list[str] = []
    if not text.startswith("---\n"):
        return None, text, ["SKILL.md must start with a '---' frontmatter line"]
    end = text.find("\n---", 4)
    if end == -1:
        return None, text, ["frontmatter is not closed with '---'"]
    raw = text[4:end]
    body = text[end + 4 :].lstrip("\n")
    fm: dict = {}
    current_map: str | None = None
    for ln, line in enumerate(raw.splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            if current_map is None:
                errs.append(f"line {ln}: unexpected indentation")
                continue
            k, _, v = line.strip().partition(":")
            if not _:
                errs.append(f"line {ln}: expected 'key: value' inside {current_map}")
                continue
            fm[current_map][k.strip()] = _unquote(v.strip())
            continue
        k, sep, v = line.partition(":")
        if not sep:
            errs.append(f"line {ln}: expected 'key: value'")
            continue
        k = k.strip()
        v = v.strip()
        if v == "":
            fm[k] = {}
            current_map = k
        else:
            fm[k] = _unquote(v)
            current_map = None
    return fm, body, errs


def _unquote(v: str) -> str:
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def validate(skill_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    md = skill_dir / "SKILL.md"
    if not md.is_file():
        return [f"{skill_dir}: SKILL.md not found"], warnings
    text = md.read_text(encoding="utf-8")
    fm, body, perrs = parse_frontmatter(text)
    errors += [f"{md}: {e}" for e in perrs]
    if fm is None:
        return errors, warnings

    name = fm.get("name")
    if not isinstance(name, str) or not name:
        errors.append(f"{md}: 'name' is required")
    else:
        if len(name) > 64:
            errors.append(f"{md}: name exceeds 64 characters")
        if not NAME_RE.match(name):
            errors.append(f"{md}: name '{name}' must be lowercase a-z, 0-9, hyphens; no leading/trailing/double hyphens")
        if name != skill_dir.name:
            errors.append(f"{md}: name '{name}' must match directory name '{skill_dir.name}'")

    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        errors.append(f"{md}: 'description' is required and non-empty")
    elif len(desc) > 1024:
        errors.append(f"{md}: description exceeds 1024 characters ({len(desc)})")

    compat = fm.get("compatibility")
    if compat is not None and (not isinstance(compat, str) or not 1 <= len(compat) <= 500):
        errors.append(f"{md}: compatibility must be 1-500 characters if present")

    meta = fm.get("metadata")
    if meta is not None:
        if not isinstance(meta, dict):
            errors.append(f"{md}: metadata must be a mapping")
        else:
            for k, v in meta.items():
                if not isinstance(v, str):
                    errors.append(f"{md}: metadata.{k} must be a string")

    known = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    for k in fm:
        if k not in known:
            warnings.append(f"{md}: unknown frontmatter key '{k}' (allowed but not in spec)")

    lines = body.count("\n") + 1
    if lines > 500:
        warnings.append(f"{md}: body is {lines} lines (> 500 recommended); move detail to references/")

    for target in LINK_RE.findall(body):
        if re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
            continue
        p = (skill_dir / target).resolve()
        try:
            p.relative_to(skill_dir.resolve())
        except ValueError:
            errors.append(f"{md}: link '{target}' escapes the skill directory")
            continue
        if not p.exists():
            errors.append(f"{md}: link target '{target}' does not exist")
        elif Path(target).parts and len(Path(target).parts) > 2:
            warnings.append(f"{md}: link '{target}' is nested more than one level (spec recommends one)")

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="skill directories")
    ap.add_argument("--root", help="validate every direct subdirectory of this path")
    a = ap.parse_args(argv)

    dirs = [Path(p) for p in a.paths]
    if a.root:
        dirs += sorted(p for p in Path(a.root).iterdir() if p.is_dir() and not p.name.startswith("."))
    if not dirs:
        ap.error("give skill directories or --root")

    total_err = 0
    for d in dirs:
        errs, warns = validate(d)
        for w in warns:
            print(f"WARN  {w}")
        for e in errs:
            print(f"ERROR {e}")
        status = "FAIL" if errs else "OK"
        print(f"{status}  {d}")
        total_err += len(errs)
    return 1 if total_err else 0


if __name__ == "__main__":
    raise SystemExit(main())
