"""
Module: commit_lint.py
Check if commit message follows the Conventional Commits format.

Notes: Conventional Commits format: <type>[optional scope]: [TICKET-NUMBER - ]<description>
"""

import os
import re
import sys

COMMIT_MESSAGE_FORMAT = "<type>[optional scope]: [TICKET-NUMBER - ]<description>"

TYPES = (
    "feat",
    "fix",
    "docs",
    "refactor",
    "test",
    "chore",
    "revert",
)


def format_text(text: str, format_type: str) -> str:
    format_start = {"bold": "\033[1m", "yellow": "\033[33m", "yellow_bold": "\033[1;33m"}
    format_end = "\033[0m"
    if format_type not in format_start:
        return f"Unknown format type: {format_type}. Text without formatting: {text}"
    return f"{format_start[format_type]}{text}{format_end}"


def read_commit_message():
    commit_editmsg = os.path.join(os.getcwd(), ".git", "COMMIT_EDITMSG")
    if os.path.exists(commit_editmsg):
        with open(commit_editmsg, "r", encoding="utf-8") as f:
            return f.read().strip()

    if not sys.stdin.isatty():
        return sys.stdin.read().strip()

    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            with open(arg, "r", encoding="utf-8") as f:
                return f.read().strip()

    print("Error: Unable to read commit message from any source.")
    return None


def log_commit_error(specific_error: str) -> None:
    commit_msg_format = format_text(COMMIT_MESSAGE_FORMAT, "yellow_bold")
    print(
        f"Error: {specific_error}\n"
        f"Commit message does not follow the Conventional Commits format.\n"
        f"...............................................................\n"
        f"Info: https://www.conventionalcommits.org/ru/v1.0.0/\n"
        f"Format should be: {commit_msg_format}\n"
        f"Examples:\n"
        f"   - feat: DATA-299 - add paynext staging model\n"
        f"   - fix(primer): resolve webhook payment_id extraction\n"
        f"   - docs(marketing): added new models description\n"
        f"   - chore: update dbt dependencies\n"
        f"\n\033[1;31m✗ Commit aborted.\033[0m\n"
    )


def log_branch_error(branch: str) -> None:
    types = "|".join(TYPES)
    print(
        f"Error: Branch '{format_text(branch, 'yellow_bold')}' does not follow naming convention.\n"
        f"Format: <type>/description or <type>-description\n"
        f"Types:  {types}\n"
        f"Examples:\n"
        f"   - feat/DATA-299-paynext-staging\n"
        f"   - fix/DATA-123-primer-webhook\n"
        f"   - docs/add-models-descriptions\n"
        f"   - chore/update-dbt-deps\n"
        f"\n\033[1;31m✗ Branch creation aborted.\033[0m\n"
    )


def check_commit_message(commit_msg: str) -> bool:
    if not commit_msg:
        log_commit_error("Empty commit message received.")
        return False

    parts = commit_msg.split(": ", 1)
    if len(parts) != 2:
        log_commit_error("Missing ': ' separator between type and description.")
        return False

    type_part, description_part = parts

    type_pattern = r"^(feat|fix|docs|refactor|test|chore|revert)(\([a-z ]+\))?$"
    if not re.match(type_pattern, type_part):
        log_commit_error("Invalid commit type or scope.")
        return False

    ticket_pattern = r"^([A-Z]+-\d+)( - )?(.+)$"
    ticket_match = re.match(ticket_pattern, description_part)

    if ticket_match:
        ticket, dash, rest = ticket_match.groups()
        if not dash:
            log_commit_error("Dash is missing after the ticket number.")
            return False
    else:
        if not description_part[0].isalpha():
            log_commit_error("Description must start with a letter when there's no ticket number.")
            return False

    print("\033[1;32m✓ Commit message is valid.\033[0m")
    return True


def check_branch_name(branch: str) -> bool:
    if branch in ("main", "master", "develop", "HEAD"):
        return True

    pattern = r"^(feat|fix|docs|refactor|test|chore|revert)[/\-].+"
    if not re.match(pattern, branch):
        log_branch_error(branch)
        return False

    print(f"\033[1;32m✓ Branch name '{branch}' is valid.\033[0m")
    return True


def main() -> None:
    if "--branch" in sys.argv:
        idx = sys.argv.index("--branch")
        branch = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
        if not branch or not check_branch_name(branch):
            sys.exit(1)
        return

    commit_message = read_commit_message()
    if commit_message is None:
        sys.exit(1)

    if not check_commit_message(commit_message):
        sys.exit(1)


if __name__ == "__main__":
    main()
