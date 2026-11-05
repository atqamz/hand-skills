# hand-skills

Optional skills for Hand fleets. Public repository, English only.

- Smallest correct change. Delete before adding.
- Layout: `skills/NAME/SKILL.md` with YAML frontmatter (`name` equal to the folder, one-line `description`), supporting files beside it. `template/` is the skill to copy.
- Core skills belong to Hand, not here.
- No code comments in scripts beyond shebangs and linter directives.
- Standard library only: `scripts/validate.py` is Python 3 stdlib and runs on Linux, macOS and Windows.
- No absolute home paths, personal profiles, tokens or remote-code execution in any skill.
- Run `python scripts/validate.py` and `python -m unittest discover -s tests` before committing.
- Pin workflow actions by commit SHA and run `actionlint` on workflow changes.
- Commits: imperative, lowercase first word, no trailing period, no attribution trailers.
