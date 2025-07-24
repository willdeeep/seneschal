# GitHub Workflow Guide

## Branch Strategy

### Branch Structure

- **main**: Production-ready code, protected branch
- **dev**: Integration branch for tested features before release
- **feature/**: Individual feature development branches
- **hotfix/**: Critical production fixes
- **release/**: Release preparation branches

### Branch Protection Rules

**Main Branch Protection:**
- Require pull request reviews
- Require status checks to pass
- Require up-to-date branches before merging
- Restrict pushes to main branch

**Dev Branch Protection:**
- Require pull request reviews
- Require status checks to pass
- Allow merge commits and squash merging

## Commit Message Format

### Conventional Commits Standard

Use the conventional commits format for clear, consistent commit messages:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect code meaning (formatting, etc.)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to build process or auxiliary tools

### Examples

```bash
# Feature addition
git commit -m "feat(characters): add spell slot tracking functionality"

# Bug fix
git commit -m "fix(auth): resolve session timeout issue"

# Documentation
git commit -m "docs: update database initialization guide"

# Refactoring
git commit -m "refactor(models): break down models.py into separate files"

# Performance improvement
git commit -m "perf(database): optimize character query with eager loading"

# Test addition
git commit -m "test(characters): add unit tests for level progression"
```

### Scope Guidelines

Common scopes for this project:
- **characters**: Character management functionality
- **auth**: Authentication and user management
- **database**: Database-related changes
- **api**: API endpoints and responses
- **ui**: User interface changes
- **docs**: Documentation updates
- **ci**: CI/CD pipeline changes
- **docker**: Docker configuration changes

## GitHub Issues

### Issue Templates

#### Feature Request Template

```markdown
# Feature Request

## User Story
As a [type of user], I want [functionality] so that [benefit].

## Description
Detailed description of the feature request.

## Acceptance Criteria
- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2
- [ ] Acceptance criterion 3

## Additional Context
Any additional information, mockups, or examples.

**Priority:** High/Medium/Low
**Estimated Effort:** Small/Medium/Large
**Dependencies:** List any dependencies
```

#### Bug Report Template

```markdown
# Bug Report

## Bug Description
Clear and concise description of the bug.

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- OS: [e.g., macOS, Ubuntu, Windows]
- Browser: [e.g., Chrome, Firefox, Safari]
- Python Version: [e.g., 3.9.0]
- Application Version: [e.g., commit hash or tag]

## Screenshots
If applicable, add screenshots to help explain the problem.

## Additional Context
Any other relevant information.
```

### Issue Labels

#### Priority Labels
- **priority-high**: Critical issues requiring immediate attention
- **priority-medium**: Important issues for next sprint
- **priority-low**: Nice-to-have improvements

#### Type Labels
- **enhancement**: New features or improvements
- **bug**: Something isn't working correctly
- **documentation**: Documentation improvements
- **refactor**: Code restructuring without functionality changes
- **security**: Security-related issues

#### Component Labels
- **d&d-5e**: D&D-specific functionality
- **frontend-ui**: User interface changes
- **backend**: Server-side functionality
- **database**: Database-related changes
- **infrastructure**: DevOps and deployment
- **testing**: Test-related changes

#### Status Labels
- **ready**: Ready for development
- **in-progress**: Currently being worked on
- **blocked**: Waiting for dependencies
- **needs-review**: Requires code review
- **needs-testing**: Requires additional testing

## Feature Branch Workflow

### Creating a Feature Branch

1. **Start from Dev Branch**
   ```bash
   git checkout dev
   git pull origin dev
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/issue-number-brief-description
  
   # Examples:
   git checkout -b feature/24-background-proficiency-integration
   git checkout -b feature/10-spell-slot-management-ui
   ```

3. **Link to GitHub Issue**
   ```bash
   # Include issue number in branch name and commits
   git commit -m "feat(characters): implement background selection (#24)"
   ```

### Branch Naming Conventions

```
feature/[issue-number]-[brief-description]
fix/[issue-number]-[brief-description]
hotfix/[issue-number]-[brief-description]
docs/[brief-description]
refactor/[brief-description]

# Examples:
feature/24-background-proficiency-integration
fix/15-character-creation-validation
hotfix/32-session-timeout-fix
docs/update-deployment-guide
refactor/models-separation
```

## Pull Request Process

### Pull Request Template

```markdown
# Pull Request

## Summary
Brief description of changes made.

## Related Issue
Closes #[issue-number]

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that causes existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)

## Testing
- [ ] Unit tests pass
- [ ] Functional tests pass
- [ ] Manual testing completed
- [ ] Database migrations tested (if applicable)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Comments added to hard-to-understand areas
- [ ] Documentation updated (if applicable)
- [ ] No new warnings introduced

## Screenshots (if applicable)
Add screenshots for UI changes.

## Additional Notes
Any additional information for reviewers.
```

### PR Review Process

#### For Authors

1. **Self-Review**
   - Review your own code before requesting review
   - Ensure tests pass locally
   - Verify documentation is updated

2. **Request Review**
   - Assign appropriate reviewers
   - Add relevant labels
   - Link to related issues

3. **Address Feedback**
   - Respond to all review comments
   - Make requested changes
   - Re-request review after changes

#### For Reviewers

1. **Code Quality**
   - Check for code style consistency
   - Verify proper error handling
   - Ensure security best practices

2. **Functionality**
   - Verify changes meet requirements
   - Test functionality if possible
   - Check for edge cases

3. **Documentation**
   - Ensure code is well-commented
   - Verify documentation updates
   - Check for clear commit messages

### Merge Strategies

#### Squash and Merge (Preferred)
- Use for feature branches with multiple commits
- Creates clean history on main/dev branches
- Preserves detailed history in feature branch

#### Merge Commit
- Use for release branches
- Preserves full commit history
- Shows explicit merge points

#### Rebase and Merge
- Use for simple, single-commit changes
- Creates linear history
- Use sparingly for complex features

## Release Process

### Version Numbering

Use semantic versioning (SemVer):
- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Workflow

1. **Create Release Branch**
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b release/v1.2.0
   ```

2. **Prepare Release**
   - Update version numbers
   - Update changelog
   - Final testing

3. **Create Release PR**
   ```bash
   # Create PR from release/v1.2.0 to main
   # Include release notes and changelog
   ```

4. **Tag Release**
   ```bash
   git checkout main
   git pull origin main
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin v1.2.0
   ```

5. **Merge Back to Dev**
   ```bash
   # Create PR from main to dev to sync changes
   ```

## Automation and Bots

### GitHub Actions Integration

- **Automatic Testing**: Run tests on every PR
- **Code Coverage**: Track coverage changes
- **Dependency Updates**: Automated dependency PRs
- **Release Automation**: Automatic changelog generation

### Issue and PR Automation

```yaml
# .github/workflows/issue-automation.yml
name: Issue Automation

on:
  issues:
    types: [opened, labeled]

jobs:
  auto-assign:
    runs-on: ubuntu-latest
    steps:
      - name: Auto-assign issues
        if: contains(github.event.issue.labels.*.name, 'ready')
        run: |
          # Auto-assign logic here
```

## Best Practices

### Commit Best Practices

1. **Atomic Commits**: Each commit should represent a single logical change
2. **Clear Messages**: Write descriptive commit messages
3. **Frequent Commits**: Commit often with small, focused changes
4. **Test Before Commit**: Ensure tests pass before committing

### Branch Best Practices

1. **Short-lived Branches**: Keep feature branches focused and short-lived
2. **Regular Updates**: Regularly sync with dev branch
3. **Clean History**: Use rebase to clean up commit history before merging
4. **Descriptive Names**: Use clear, descriptive branch names

### Issue Management

1. **Clear Descriptions**: Write detailed issue descriptions
2. **Proper Labels**: Use appropriate labels for categorization
3. **Regular Updates**: Update issues with progress and blockers
4. **Close Promptly**: Close issues when work is complete

### Code Review

1. **Constructive Feedback**: Provide helpful, specific feedback
2. **Timely Reviews**: Review PRs promptly to avoid blocking development
3. **Test Thoroughly**: Test changes when reviewing
4. **Knowledge Sharing**: Use reviews as learning opportunities
