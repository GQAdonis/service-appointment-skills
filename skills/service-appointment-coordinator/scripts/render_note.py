#!/usr/bin/env python3
"""Render a dispatch note / appointment request from structured fields.

Stdlib only. Produces one paste-ready paragraph (<~90 words) matching the
structure in assets/note-template.md. Warns when the result is too long for
agents to read at a glance.

Usage:
  render_note.py annotate --name "Travis James" --phone 945-555-0100 \
      --when "tomorrow, Sun Nov 8, 12-4 p.m." --order 71-0000 \
      --what "my dog chewed through and severed the line where it runs under the edge of the gate" \
      --needs "replace/re-run that section of drop and bring materials to bury or protect it under the gate" \
      --access "dog will be secured inside; gate unlocked"

  render_note.py new --name ... --phone ... --service "AT&T Internet" \
      --what "no link light on the ONT since Tuesday" --tried "power-cycled ONT and gateway twice" \
      --windows "Tue 11/11 8-12; Wed 11/12 any" --access "..."

  render_note.py reschedule --name ... --phone ... --order ... \
      --when "Sun Nov 8, 12-4 p.m." --windows "Mon 11/9 8-12; Tue 11/10 12-4"

  render_note.py annotate --json fields.json     # any subcommand accepts --json
"""
from __future__ import annotations

import argparse
import json
import sys

MAX_WORDS = 90


def _req(fields: dict, *keys: str) -> None:
    missing = [k for k in keys if not fields.get(k)]
    if missing:
        sys.exit(f"error: missing required field(s): {', '.join(missing)}")


def _ident(f: dict) -> str:
    parts = [f["name"], f["phone"]]
    if f.get("order"):
        parts.append(f"order {f['order']}")
    return ", ".join(parts)


def annotate(f: dict) -> str:
    _req(f, "name", "phone", "when", "what")
    s = (
        f"I have a technician appointment {f['when']} ({_ident(f)}). "
        f"Please add a note to the work order: {f['what'].rstrip('.')}."
    )
    if f.get("needs"):
        s += f" The tech will need to {f['needs'].rstrip('.')}."
    if f.get("access"):
        s += f" Access: {f['access'].rstrip('.')}."
    s += " Please confirm once the note is on the dispatch ticket."
    return s


def new(f: dict) -> str:
    _req(f, "name", "phone", "service", "what", "windows")
    s = (
        f"I need a technician visit for {f['service']} ({_ident(f)}). "
        f"Problem: {f['what'].rstrip('.')}."
    )
    if f.get("tried"):
        s += f" Already tried: {f['tried'].rstrip('.')}; no change. Not a troubleshooting request."
    s += f" Available: {f['windows']}."
    if f.get("access"):
        s += f" Access: {f['access'].rstrip('.')}."
    s += " Please schedule and confirm the date, window, and ticket number."
    return s


def reschedule(f: dict) -> str:
    _req(f, "name", "phone", "when", "windows")
    return (
        f"I need to move my technician appointment currently set for {f['when']} ({_ident(f)}). "
        f"Acceptable windows: {f['windows']}. "
        "Please move it to the earliest of those and confirm the new date and window."
    )


RENDERERS = {"annotate": annotate, "new": new, "reschedule": reschedule}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("kind", choices=RENDERERS)
    p.add_argument("--json", help="path to a JSON object of fields (CLI flags override)")
    for k in ("name", "phone", "order", "when", "what", "needs", "access", "service", "tried", "windows"):
        p.add_argument(f"--{k}")
    a = p.parse_args(argv)

    fields: dict = {}
    if a.json:
        try:
            with open(a.json, encoding="utf-8") as fh:
                fields = json.load(fh)
        except (OSError, json.JSONDecodeError) as e:
            sys.exit(f"error: cannot read --json file: {e}")
        if not isinstance(fields, dict):
            sys.exit("error: --json must contain a JSON object")
    for k, v in vars(a).items():
        if k not in ("kind", "json") and v:
            fields[k] = v

    text = RENDERERS[a.kind](fields)
    print(text)
    n = len(text.split())
    if n > MAX_WORDS:
        print(f"warning: {n} words (> {MAX_WORDS}); agents skim long messages — tighten it.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
