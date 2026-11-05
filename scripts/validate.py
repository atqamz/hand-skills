#!/usr/bin/env python3
import re
import sys
from pathlib import Path

MAX_DESCRIPTION = 400
MAX_NAME = 64
MAX_BYTES = 20000
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KEY = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s+(.*))?$")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)|!\[[^\]]*\]\(([^)\s]+)\)")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
PATHS = [re.compile(p, re.IGNORECASE) for p in (r"/home/", r"/Users/", r"C:\\{1,2}Users")]
SECRETS = [
    re.compile(p)
    for p in (
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"AKIA[0-9A-Z]{16}",
        r"gh[pousr]_[A-Za-z0-9]{36,}",
        r"github_pat_[A-Za-z0-9_]{22,}",
        r"sk-[A-Za-z0-9_-]{20,}",
        r"xox[baprs]-[A-Za-z0-9-]{10,}",
    )
]


def frontmatter(text):
    lines = text.split("\n")
    if lines[0].rstrip() != "---":
        return None, ["frontmatter missing: the first line must be ---"]
    for end in range(1, len(lines)):
        if lines[end].rstrip() == "---":
            break
    else:
        return None, ["frontmatter is not closed with ---"]
    fields, errors = {}, []
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        match = KEY.match(line.rstrip())
        if not match:
            errors.append(f"line {number}: not a key: value pair")
            continue
        fields[match.group(1)] = (match.group(2) or "").strip()
    return fields, errors


def check_skill_file(path, name):
    errors = []
    if path.stat().st_size > MAX_BYTES:
        errors.append(f"{path.name} is {path.stat().st_size} bytes, over the {MAX_BYTES} byte limit")
    fields, found = frontmatter(path.read_text(encoding="utf-8"))
    errors += found
    if fields is None:
        return errors
    if fields.get("name") != name:
        errors.append(f"name {fields.get('name')!r} must equal the folder name {name!r}")
    if not NAME.match(name) or len(name) > MAX_NAME:
        errors.append(f"folder name {name!r} must be lowercase kebab-case of at most {MAX_NAME} characters")
    description = fields.get("description")
    if not description:
        errors.append("description is missing or empty")
    elif description[0] in "|>&*!":
        errors.append("description must be a single line, not a block or alias")
    elif len(description) > MAX_DESCRIPTION:
        errors.append(f"description is {len(description)} characters, over the {MAX_DESCRIPTION} limit")
    return errors


def check_text(path, root):
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    errors = []
    for number, line in enumerate(text.split("\n"), start=1):
        for pattern in PATHS:
            if pattern.search(line):
                errors.append(f"{path.name}:{number}: machine-specific path")
        for pattern in SECRETS:
            if pattern.search(line):
                errors.append(f"{path.name}:{number}: looks like a secret")
    if path.suffix == ".md":
        for match in LINK.finditer(text):
            target = match.group(1) or match.group(2)
            if target.startswith("#") or SCHEME.match(target):
                continue
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            if not resolved.is_relative_to(root):
                errors.append(f"{path.name}: link {target} leaves the skill folder")
            elif not resolved.exists():
                errors.append(f"{path.name}: link {target} does not resolve")
    return errors


def check(directory):
    root = directory.resolve()
    entry = root / "SKILL.md"
    if not entry.is_file():
        return ["SKILL.md is missing"]
    errors = check_skill_file(entry, root.name)
    for path in sorted(root.rglob("*")):
        if path.is_file():
            errors += check_text(path, root)
    return errors


def main(argv):
    directories = [Path(a) for a in argv]
    if not directories:
        base = Path(__file__).resolve().parent.parent
        directories = [base / "template"] + sorted(p for p in (base / "skills").iterdir() if p.is_dir())
    failed = False
    for directory in directories:
        for error in check(directory):
            print(f"{directory}: {error}")
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
