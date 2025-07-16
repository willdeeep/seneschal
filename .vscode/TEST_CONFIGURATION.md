# Test Configuration for GitHub Actions

## Overview

The test suite is configured to handle different environments gracefully, with specific markers for tests that should be skipped in CI environments like GitHub Actions.

## Test Markers

### Environment-Based Markers

- `@pytest.mark.unit` - Fast unit tests with no external dependencies
- `@pytest.mark.functional` - Tests requiring database (uses SQLite in CI)
- `@pytest.mark.requires_db` - Tests requiring real PostgreSQL database
- `@pytest.mark.requires_env` - Tests requiring environment variables/config
- `@pytest.mark.requires_network` - Tests requiring network access
- `@pytest.mark.github_skip` - Tests explicitly skipped in GitHub Actions
- `@pytest.mark.local_only` - Tests that only run in local development
- `@pytest.mark.slow` - Tests that take significant time to run

### Usage Examples

```python
@pytest.mark.unit
def test_ability_modifier_calculation():
    """Fast unit test - runs everywhere."""
    pass

@pytest.mark.functional
def test_character_creation(app, test_user):
    """Database test - uses SQLite in CI."""
    pass

@pytest.mark.requires_db
@pytest.mark.local_only
def test_complex_postgres_queries():
    """PostgreSQL-specific test - skipped in CI."""
    pass

@pytest.mark.requires_network
@pytest.mark.github_skip
def test_d20_srd_api():
    """Network test - skipped in GitHub Actions."""
    pass
```

## CI Environment Detection

The test suite automatically detects CI environments:

- GitHub Actions: `GITHUB_ACTIONS=true`
- Generic CI: `CI=true`
- Travis CI: `TRAVIS=true`
- CircleCI: `CIRCLECI=true`
- Jenkins: `JENKINS_URL` exists

## GitHub Actions Workflow

### Standard Test Job

Runs on multiple Python versions (3.9, 3.10, 3.11) with:

```bash
# Unit tests (fast, no external dependencies)
pytest tests/unit/ -m "unit and not requires_db and not requires_env and not github_skip"

# Functional tests (database using SQLite)
pytest tests/functional/ -m "functional and not github_skip and not local_only"
```

### PostgreSQL Integration Job

Separate job with PostgreSQL service for database-specific tests:

```yaml
services:
  postgres:
    image: postgres:13
    env:
      POSTGRES_PASSWORD: testpass
      POSTGRES_USER: testuser
      POSTGRES_DB: testdb
```

## Local Development

### Run All Tests
```bash
pytest
```

### Run by Category
```bash
# Unit tests only
pytest -m unit

# Functional tests only
pytest -m functional

# Local-only tests
pytest -m local_only

# Skip slow tests
pytest -m "not slow"
```

### Run with Coverage
```bash
coverage run -m pytest
coverage report
coverage html
```

## Test Database Configuration

### CI Environment (GitHub Actions)
- Uses temporary SQLite databases
- Automatic database creation/teardown per test
- No external dependencies required

### Local Development
- Can use SQLite (default) or PostgreSQL
- Environment variables for database URL
- Populated test fixtures available

### PostgreSQL Integration Tests
- Runs in separate CI job with PostgreSQL service
- Tests marked with `@pytest.mark.requires_db`
- Real database connection for complex queries

## Environment Variables

### CI-Specific
- `CI=true` - Indicates CI environment
- `GITHUB_ACTIONS=true` - GitHub Actions specific
- `TESTING=true` - Test mode flag

### Optional
- `DATABASE_URL` - Override database connection
- `ENABLE_NETWORK_TESTS=true` - Enable network tests in CI
- `CODECOV_TOKEN` - Coverage reporting (optional)

## Skipped Tests in GitHub Actions

The following tests are automatically skipped in GitHub Actions:

1. **Network-dependent tests** (`@pytest.mark.requires_network`)
2. **Local-only tests** (`@pytest.mark.local_only`)
3. **Tests explicitly marked** (`@pytest.mark.github_skip`)
4. **Tests requiring real PostgreSQL** (unless in integration job)

## Best Practices

### Writing Tests

1. **Mark tests appropriately**:
   ```python
   @pytest.mark.unit          # For fast, isolated tests
   @pytest.mark.functional    # For database-dependent tests
   @pytest.mark.local_only    # For development-only tests
   ```

2. **Use fixtures for database tests**:
   ```python
   def test_character_creation(app, test_user):
       # Uses app context and test user fixture
   ```

3. **Skip expensive tests in CI**:
   ```python
   @pytest.mark.slow
   @pytest.mark.local_only
   def test_performance_intensive():
       # Skipped in CI, runs locally
   ```

### Running Tests Locally

```bash
# Quick unit tests during development
pytest -m unit

# Full test suite (including slow tests)
pytest

# Test specific functionality
pytest tests/unit/test_character_dnd.py -v

# Skip network tests
pytest -m "not requires_network"
```

This configuration ensures your D&D character management tests run efficiently in GitHub Actions while allowing comprehensive testing in local development environments.
