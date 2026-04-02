# test-hooks-demo

Demo repo for testing Git hooks.

## Setup

```bash
make init
```

## What's being checked

**Branch names** (`post-checkout`):
- Must start with: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- Format: `<type>/description` or `<type>-description`
- Examples: `feat/add-login`, `fix/KAN-123-memory-leak`

**Commit messages** (`commit-msg`):
- Format: `<type>[optional scope]: [TICKET-NUMBER - ]<description>`
- Examples: `feat: add login`, `fix(auth): KAN-123 - resolve token expiry`
