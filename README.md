# service-appointment-skills

[Agent Skills](https://agentskills.io) for coordinating technician and service appointments — internet, utilities, HVAC, appliance repair — through a provider's web chat, portal, or SMS thread, including working with the provider's own AI assistants and escalating to live agents.

Skills in this repo follow the [agentskills.io specification](https://agentskills.io/specification) and validate with [`skills-ref`](https://github.com/agentskills/agentskills/tree/main/skills-ref).

## Skills

| Skill | What it does |
|---|---|
| [`service-appointment-coordinator`](skills/service-appointment-coordinator/) | Book, annotate, reschedule, cancel, or check a service appointment on the user's behalf. Classifies scripted bots vs. LLM assistants vs. humans, drives escalation and queue handling, refuses to act on instructions from the other side's AI, and pauses for the user on credentials, money, or irreversible choices. |

## Layout

```
skills/
  service-appointment-coordinator/
    SKILL.md                      # entry point (~5k tokens); links to the rest
    references/
      ai-assistants.md            # working with the provider's bots and LLM agents
      queue-and-escalation.md     # accept-prompt timing, keep-alive, transfers
      agent-scripts.md            # human agent script lines and replies
      browser-tactics.md          # Claude in Chrome / screenshot-automation specifics
    assets/
      note-template.md            # annotate / new / reschedule message templates
      report-template.md          # report-back and human-in-the-loop question formats
    scripts/
      render_note.py              # render a paste-ready note from fields (stdlib only)
scripts/
  validate_skills.py              # dependency-free spec validator used in CI
.github/workflows/validate.yml    # runs both validators on push/PR
```

## Using the skill

**Claude Code / Claude.ai:** copy or symlink `skills/service-appointment-coordinator` into your skills directory (e.g. `~/.claude/skills/`), or add this repo as a skills source if your client supports one. The skill triggers on mentions of technician visits, work orders, dispatch, installers, or appointments with a utility/ISP.

**Other agents:** any runtime that reads `SKILL.md` frontmatter per the spec can load it. Generate the prompt stanza with:

```bash
skills-ref to-prompt skills/service-appointment-coordinator
```

## Validation

```bash
# dependency-free
python3 scripts/validate_skills.py --root skills

# official reference validator
pip install git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref
skills-ref validate skills/service-appointment-coordinator
```

## Design notes

- **Progressive disclosure.** `SKILL.md` carries the decision logic and hard rules; detail that is only needed at a particular moment (queue timing, script replies, browser coordinates) lives one level down in `references/`.
- **Other AIs are peers, not authorities.** The provider's chat AI is treated as an agent with a narrow toolset: probe its capabilities, send one intent per message, verify every claimed write, and never execute its instructions as commands.
- **Writes require a human.** Only a human agent's confirmation counts as evidence that a ticket changed. AI confirmations are reported as unverified.
- **Human-in-the-loop is explicit.** Credentials, one-time codes, money, irreversible actions, diverging diagnoses, and facts only the user knows all stop the agent and surface a question with the counterpart's exact wording.

## Contributing

Add a skill as `skills/<name>/SKILL.md` where `<name>` matches the frontmatter `name`. Run the validators before opening a PR. Keep `SKILL.md` under 500 lines; put the rest in `references/`.

## License

MIT — see [LICENSE](LICENSE).
