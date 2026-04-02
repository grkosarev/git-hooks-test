# test-hooks-demo

Demo repo for testing Git hooks.

## Setup

```bash
make init
```

## What's being checked

**Branch names** (`post-checkout`):
- Must start with: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `revert`
- Format: `<type>/description` or `<type>-description`
- Examples: `feat/DATA-299-paynext-staging`, `fix/DATA-123-primer-webhook`, `chore/update-dbt-deps`

**Commit messages** (`commit-msg`):
- Format: `<type>[optional scope]: [TICKET-NUMBER - ]<description>`
- Examples: `feat: DATA-299 - add paynext staging model`, `fix(primer): resolve webhook payment_id extraction`
