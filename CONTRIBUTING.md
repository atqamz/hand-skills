# Contributing

Optional skills for Hand fleets, under the [MIT license](LICENSE). The repository is public: add no machine-specific paths, tokens or personal data. The maintainer decides every merge.

- Read [`AGENTS.md`](AGENTS.md) and the safety notice in [`README.md`](README.md).
- Open one pull request per change, and say what changed and why.
- A new skill starts from [`template/`](template), passes `python scripts/validate.py`, and adds its row to the catalogue in the README.
- A skill never fetches and runs remote code, and says what it needs.
- Run `python scripts/validate.py` and `python -m unittest discover -s tests` before you push. CI runs both on Linux, macOS and Windows.
- Write commits with an imperative, lowercase subject and no trailing period.
- Report a vulnerability privately to the maintainer, never in a pull request.
