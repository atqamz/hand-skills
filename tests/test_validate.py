import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "validate.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run(*directories):
    done = subprocess.run(
        [sys.executable, str(SCRIPT), *map(str, directories)],
        capture_output=True,
        text=True,
    )
    return done.returncode, done.stdout


class Fixtures(unittest.TestCase):
    def test_good_passes(self):
        self.assertEqual(run(FIXTURES / "good"), (0, ""))

    def test_bad_fail(self):
        cases = {
            "bad-no-frontmatter": "frontmatter missing",
            "bad-name": "must equal the folder name",
            "Bad-Case": "lowercase kebab-case",
            "bad-multiline": "single line",
            "bad-long": "over the 400 limit",
            "bad-path": "machine-specific path",
            "bad-link": "does not resolve",
            "bad-big": "byte limit",
        }
        for name, message in cases.items():
            with self.subTest(name):
                code, out = run(FIXTURES / name)
                self.assertEqual(code, 1)
                self.assertIn(message, out)

    def test_missing_skill_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = run(tmp)
        self.assertEqual(code, 1)
        self.assertIn("SKILL.md is missing", out)


class Generated(unittest.TestCase):
    def skill(self, tmp, body):
        folder = Path(tmp) / "gen"
        folder.mkdir()
        (folder / "SKILL.md").write_text(
            "---\nname: gen\ndescription: Generated.\n---\n" + body, encoding="utf-8"
        )
        return folder

    def test_secrets_fail(self):
        samples = [
            "-----BEGIN " + "RSA PRIVATE KEY-----",
            "AKIA" + "A" * 16,
            "ghp_" + "a" * 36,
            "github_pat_" + "a" * 30,
            "sk-" + "a" * 24,
            "xoxb-" + "1" * 12,
        ]
        for sample in samples:
            with self.subTest(sample[:8]), tempfile.TemporaryDirectory() as tmp:
                code, out = run(self.skill(tmp, sample + "\n"))
                self.assertEqual(code, 1)
                self.assertIn("looks like a secret", out)

    def test_home_paths_fail(self):
        for sample in ("/Users/x", "C:" + "\\" + "Users" + "\\x", "/home/x"):
            with self.subTest(sample), tempfile.TemporaryDirectory() as tmp:
                code, out = run(self.skill(tmp, sample + "\n"))
                self.assertEqual(code, 1)
                self.assertIn("machine-specific path", out)

    def test_link_escaping_folder_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = run(self.skill(tmp, "[up](../other.md)\n"))
        self.assertEqual(code, 1)
        self.assertIn("leaves the skill folder", out)


class Repository(unittest.TestCase):
    def test_default_run_passes(self):
        self.assertEqual(run(), (0, ""))


if __name__ == "__main__":
    unittest.main()
