# GitHub Feature-Branch Workflow Guide

Complete workflow with reusable templates and CLI snippets for issues, commits, PRs, version tags, and local CI with Act.

## Templates

### Issue Template
```md
Title: <type>: <short summary>

## Summary
- What and why in 2–4 lines.

## User story
- As a <role>, I want <capability> so that <benefit>.

## Scope
- **In scope:**
- **Out of scope:**

## Acceptance criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Implementation notes
- Design decisions, data model changes, risks.

## Test plan
- **Unit:** classes/functions and cases.
- **Integration/functional:** scenarios and data.

## Links
- Related issues/PRs/Docs
```

### Commit Message Template (Conventional Commits)
```md
<type>(<scope>): <short imperative summary>

## Why
- <one line>

## What
- <bulleted key changes>

## Notes
- Breaking changes/migrations/follow-ups

Refs: #<issue>
Closes: #<issue>   # when appropriate
```

### Pull Request Template
```md
Title: <type>(<scope>): <summary>

## Summary
- What changed and why.

## Changes
- Bullets of notable changes.

## How to test
- Steps, data, expected results.

## Refactoring
- Readability/maintainability/performance improvements.

## Risks and mitigations
- Notes.

## Checklist
- [ ] Unit tests added/updated
- [ ] Linting/formatting passed
- [ ] Docs updated

Refs: #<issue>
```

### Release/Tag Notes Template
```md
Tag: v<major>.<minor>.<patch>

## Release notes
- Highlights
- Breaking changes
- Migration/upgrade steps

## Verification
- Test summary, coverage, key checks
```

### CI Workflow Template (GitHub vs Act conditions)
```yaml
name: CI

on:
  push:
    branches: [ dev, main ]
  pull_request:
    branches: [ dev, main ]

env:
  CI: true
  PIP_CACHE_DIR: ~/.cache/pip

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install deps
        run: |
          python -m venv venv
          . venv/bin/activate
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Lint (flake8)
        run: |
          . venv/bin/activate
          flake8

      - name: Format check (black)
        run: |
          . venv/bin/activate
          black --check .

      - name: Tests (pytest with coverage)
        run: |
          . venv/bin/activate
          pytest -q --maxfail=1 --disable-warnings --cov=project --cov-report=term-missing

      - name: Upload coverage artifact (GitHub Actions only)
        if: ${{ github.actor != 'nektos/act' }}
        uses: actions/upload-artifact@v4
        with:
          name: coverage-${{ matrix.python-version }}
          path: |
            .coverage
            htmlcov/

      - name: Local coverage summary (Act only)
        if: ${{ github.actor == 'nektos/act' }}
        run: |
          echo "Running under Act; skipping artifact upload."
          ls -la htmlcov || true

  test-with-postgres:
    needs: test
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        ports: ['5432:5432']
        env:
          POSTGRES_DB: app
          POSTGRES_USER: app
          POSTGRES_PASSWORD: password
        options: >-
          --health-cmd="pg_isready -U app -d app"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install deps
        run: |
          python -m venv venv
          . venv/bin/activate
          pip install -r requirements.txt
      - name: Integration tests (Postgres)
        env:
          DATABASE_URL: postgresql://app:password@localhost:5432/app
        run: |
          . venv/bin/activate
          pytest -q tests/integration
```

## Feature-Branch Workflow Steps

### 1. Create/checkout feature branch from dev and link to issue

```bash
# Ensure dev is current
git checkout dev
git pull origin dev

# Create an issue (or note its number)
gh issue create -t "feat: DB-driven proficiencies" -b "Summary and scope..." -l "enhancement,refactor"
# Or list to get an existing number
gh issue list
ISSUE=123   # set your issue number

# Create feature branch from dev
git checkout -b feat/123-db-driven-proficiencies

# Push and set upstream
git push -u origin feat/123-db-driven-proficiencies

# (Link by reference) – use the issue number in commits/PRs: Refs: #$ISSUE
```

### 2. Write unit tests for planned classes/methods/functions

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Add tests, then run quickly
pytest -q
```

### 3. Implement changes and commit incrementally

```bash
git add -p
git commit -m "feat(characters): query optional proficiencies from DB

Why
- Replace hardcoded lists.

What
- Use CharacterClass.optional_skill_proficiencies.

Refs: #123"
git push
```

Repeat until all elements of the issue are implemented.

### 4. Refactor stage

- Improve readability/maintainability/performance.
- Extract services, reduce route complexity, add type hints.

```bash
git add -p
git commit -m "refactor(characters): extract ProficiencyService to separate concerns

What
- Moved business logic out of routes."

# Lint & format
black .
isort .
flake8
git add -A
git commit -m "style: apply black/isort and fix flake8 warnings"
```

### 5. Run local tests and fix failures

```bash
pytest -q
pytest -q tests/unit
pytest -q tests/functional

# Fix issues, then:
git add -p
git commit -m "fix: address failing tests and edge cases in proficiency resolver
Refs: #123"
git push
```

### 6. Create PR to merge feature into dev

```bash
gh pr create \
  -B dev \
  -H feat/123-db-driven-proficiencies \
  -t "feat(characters): DB-driven proficiencies and refactor" \
  -F .github/PULL_REQUEST_TEMPLATE.md

# Add labels if needed
gh pr edit --add-label "refactor" --add-label "enhancement"
```

### 7. Merge PR into dev and label with version

```bash
# Squash merge and delete branch on remote
gh pr merge --squash --delete-branch

# Add version label to the PR (if you maintain such labels)
gh pr edit --add-label "v0.2.1"
```

### 8. Switch to dev and clean up local branch

```bash
git checkout dev
git pull origin dev
git branch -d feat/123-db-driven-proficiencies || true
```

### 9. Test dev with Act CLI (Mac M-series)

```bash
# Ensure Docker is running
# Run the entire workflow locally (use amd64 on Apple Silicon)
act --container-architecture linux/amd64 --verbose

# Or just the matrix test job
act -j test --container-architecture linux/amd64 --verbose

# Or the Postgres job
act -j test-with-postgres --container-architecture linux/amd64 --verbose
```

**Investigate any failed tests and fix on dev:**

```bash
# Make fixes on dev
git add -p
git commit -m "fix(ci): adjust workflow for act and GH artifact conditions"
git push
```

### 10. QA checks

- Manual functional checks
- Accessibility/UX sanity pass
- Docs updates

```bash
git add -A
git commit -m "chore(qA): minor UX and docs updates"
git push
```

### 11. Tag a new version on dev

```bash
# Show current tag
git describe --tags --abbrev=0

# Bump minor (example: v0.1.0 -> v0.2.0)
NEW_TAG=v0.2.0
git tag -a "$NEW_TAG" -m "chore(release): $NEW_TAG"
git push origin "$NEW_TAG"

# Optional GitHub release
gh release create "$NEW_TAG" --generate-notes
```

### 12. Merge dev into main (release PR)

```bash
gh pr create \
  -B main \
  -H dev \
  -t "release: $NEW_TAG to main" \
  -b "Promote dev to main. Tag: $NEW_TAG. CI green and validated via Act. Refs: #123"

# Merge when approved
gh pr merge --squash
```

## Quick Reference

### Branch Naming Conventions
- `feat/<issue>-<kebab-title>` - New features
- `fix/<issue>-<kebab-title>` - Bug fixes  
- `chore/<issue>-<kebab-title>` - Maintenance tasks
- `refactor/<issue>-<kebab-title>` - Code improvements

### Commit Message Types
- `feat:` - New features
- `fix:` - Bug fixes
- `refactor:` - Code restructuring
- `style:` - Formatting/linting
- `test:` - Adding tests
- `chore:` - Maintenance
- `docs:` - Documentation

### Act CLI Usage (Apple Silicon)
```bash
# Run whole workflow locally
act --container-architecture linux/amd64 --verbose

# Run only the matrix test job
act -j test --container-architecture linux/amd64 --verbose

# Run the Postgres job after test
act -j test-with-postgres --container-architecture linux/amd64 --verbose
```

### GitHub CLI Quick Commands
```bash
# List labels
gh label list

# Create issue
gh issue create -t "Title" -b "Body" -l "label1,label2"

# Create PR
gh pr create -B dev -H feature-branch -t "Title" -b "Body"

# Merge PR
gh pr merge --squash --delete-branch

# Create release
gh release create "v1.0.0" --generate-notes
```

## Notes
- Keep commits small and descriptive
- Reference issue numbers in commits and PRs (`Refs: #123`, `Closes: #123`)
- Always test locally with Act CLI before pushing to ensure CI compatibility
- Use conventional commit format for consistency
- Tag versions follow semantic versioning (MAJOR.MINOR.PATCH)
