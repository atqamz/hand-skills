# hand-skills

Optional skills for [Hand](https://github.com/atqamz/hand) fleets, under the [MIT license](LICENSE).

## What this is, and is not

- This repository holds optional skills: things a fleet may want, such as a browser-automation skill. Each one lives in `skills/NAME/`.
- It does not hold Hand's core skills. `secondhand` and `secondhand-cleanup` stay in Hand, and `hand init` installs them itself.
- It holds no code that Hand runs. A skill is a folder of text that an agent reads.

## Safety

A skill is instructions for an agent that runs with permission prompts skipped. Read a skill, and every file beside it, before you install it. Skills here must not fetch and run remote code. `scripts/validate.py` catches machine-specific paths and obvious secrets, but it cannot judge intent: your read is the check.

## Install a skill

Pick a version first: clone a tag or a commit, not a moving branch. Nothing updates automatically.

```sh
git clone https://github.com/atqamz/hand-skills
git -C hand-skills checkout TAG_OR_COMMIT
```

Copy the folder to one of the two places Claude Code reads skills from:

| Scope | Destination | Seen by |
| --- | --- | --- |
| One fleet | `FLEET_FOLDER/.claude/skills/NAME/` | agents started in that fleet folder |
| Every project of your user | `~/.claude/skills/NAME/` | every Claude Code session you run |

```sh
cp -R hand-skills/skills/NAME FLEET_FOLDER/.claude/skills/
```

`hand init` writes its own skills to `.claude/skills/` in the fleet folder (and to `.agents`, `.grok` and `.pi` for other agents). A folder named like a skill Hand owns, `secondhand` or `secondhand-cleanup`, is not Hand's to overwrite: never name a skill that way. Other agents read their own folder: copy to `FLEET_FOLDER/.agents/skills/NAME/` for them.

## Update and remove

- Update: check out a newer tag or commit, read the diff of the skill, then copy the folder over the old one. Delete files the new version dropped.
- Remove: delete `.../skills/NAME/`.

## Write a skill

1. Copy [`template/`](template) to `skills/NAME/`. `NAME` is lowercase kebab-case.
2. Set `name` to the folder name and write a one-line `description` that says what the skill does and when to use it.
3. Run `python scripts/validate.py`. Run `python -m unittest discover -s tests` if you changed the script.

The validator checks every skill for:

- frontmatter with `name` equal to the folder name, lowercase kebab, at most 64 characters;
- a one-line `description` of at most 400 characters;
- `SKILL.md` of at most 20000 bytes;
- no `/home/`, `/Users/` or `C:\Users` paths and no obvious secrets, in any text file of the skill;
- relative links that resolve inside the skill folder.

It needs Python 3 and nothing else. [`skills/hand-commit-message`](skills/hand-commit-message) is a small worked example.

## Catalogue

| Name | What it does | What it needs |
| --- | --- | --- |
| [`hand-commit-message`](skills/hand-commit-message) | Writes commit messages that follow Hand's rules | nothing |

## Roadmap

A sketch only; Hand has no such command today. A future `hand skills add NAME` could clone this repository at a pinned tag or commit, run the validator, show the skill for the operator to read, then copy it into the fleet's skill folders the way `hand init` does and refuse to overwrite a folder it does not own. `hand skills remove NAME` would delete it.
