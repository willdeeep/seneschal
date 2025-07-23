# CI/CD Pipeline Guide

## Overview

The CI/CD pipeline automates testing, quality checks, and deployment preparation using GitHub Actions. The pipeline ensures code quality and functionality before merging changes.

## Pipeline Configuration

### GitHub Actions Workflow

The pipeline is defined in `.github/workflows/run_tests.yml`:

```yaml
name: Run Tests

on:
  push:
    branches: [ main, dev ]
  pull_request:
    branches: [ main, dev ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_USER: postgres
          POSTGRES_DB: test_seneschal
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost/test_seneschal
        SECRET_KEY: test-secret-key
      run: |
        pytest --cov=project --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## Local Testing with Act

### Installing Act

[Act](https://github.com/nektos/act) allows you to run GitHub Actions locally:

```bash
# macOS
brew install act

# Linux
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Windows (with chocolatey)
choco install act-cli
```

### Running Tests Locally

```bash
# Run all workflow tests
act

# Run specific job
act -j test

# Run with specific event
act push

# Run with custom environment file
act --env-file .env.test
```

### Act Configuration

Create `.actrc` for default settings:

```
--container-architecture linux/amd64
--artifact-server-path /tmp/artifacts
```

## Container Testing

### Docker Test Environment

Run tests in the Docker environment:

```bash
# Build test image
docker-compose build

# Run tests in container
docker-compose run --rm web pytest

# Run tests with coverage
docker-compose run --rm web pytest --cov=project --cov-report=html

# Run specific test categories
docker-compose run --rm web pytest -m unit
docker-compose run --rm web pytest -m functional
```

### Test Database Setup

For container testing with fresh database:

```bash
# Start services
docker-compose up -d db

# Initialize test database
docker-compose run --rm web python init_db.py --force

# Run tests
docker-compose run --rm web pytest

# Cleanup
docker-compose down -v
```

## Test Categories and Markers

### Pytest Markers

The project uses custom pytest markers for test organization:

```ini
[pytest]
markers =
    unit: Unit tests that don't require external services
    functional: Functional tests that may require database
    e2e: End-to-end tests
    slow: Tests that take a long time to run
    requires_db: Tests that require a real database connection
    requires_env: Tests that require environment variables
    requires_network: Tests that require network access
    github_skip: Tests that should be skipped in GitHub Actions
    local_only: Tests that only run in local development
```

### Running Specific Test Types

```bash
# Unit tests only (fast)
pytest -m unit

# Database-dependent tests
pytest -m requires_db

# Skip slow tests
pytest -m "not slow"

# Run only tests suitable for CI
pytest -m "not (local_only or github_skip)"
```

## Quality Checks

### Code Linting

```bash
# Run flake8 linting
flake8 project/ tests/

# In Docker
docker-compose run --rm web flake8 project/ tests/
```

### Code Coverage

```bash
# Generate coverage report
coverage run -m pytest
coverage report
coverage html

# View coverage in browser
open htmlcov/index.html
```

### Type Checking (Optional)

```bash
# Install mypy
pip install mypy

# Run type checking
mypy project/
```

## Pre-commit Hooks

### Setup Pre-commit

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install
```

### Pre-commit Configuration

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
  
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
```

## Environment Variables for Testing

### Required Test Environment Variables

```bash
# .env.test
SECRET_KEY=test-secret-key-not-for-production
DATABASE_URL=postgresql://postgres:postgres@localhost/test_seneschal
FLASK_ENV=testing
```

### GitHub Secrets Configuration

Set these secrets in your GitHub repository:

- `SECRET_KEY`: Production secret key
- `DATABASE_URL`: Test database connection string
- `CODECOV_TOKEN`: Code coverage service token

## Deployment Pipeline

### Staging Deployment

```yaml
deploy-staging:
  needs: test
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/dev'
  
  steps:
    - name: Deploy to staging
      run: |
        # Deployment commands here
        echo "Deploying to staging..."
```

### Production Deployment

```yaml
deploy-production:
  needs: test
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/main'
  
  steps:
    - name: Deploy to production
      run: |
        # Production deployment commands
        echo "Deploying to production..."
```

## Performance Testing

### Load Testing Setup

```bash
# Install locust
pip install locust

# Run load tests
locust -f tests/performance/locustfile.py --host=http://localhost:5000
```

### Database Performance

```bash
# Profile database queries
docker-compose run --rm web python -m cProfile -s cumulative app.py

# Analyze slow queries
docker-compose logs db | grep "slow query"
```

## Monitoring and Alerts

### Health Check Endpoint

```python
@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Check database connectivity
        db.session.execute('SELECT 1')
        return {'status': 'healthy', 'database': 'connected'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500
```

### Monitoring Setup

```bash
# Add to docker-compose.yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## Troubleshooting CI/CD Issues

### Common Pipeline Failures

**Database Connection Issues**
```bash
# Check service configuration
# Ensure PostgreSQL service is properly configured in workflow
# Verify DATABASE_URL format
```

**Test Failures**
```bash
# Run tests locally first
pytest -xvs

# Check for environment-specific issues
pytest --tb=long

# Isolate failing tests
pytest tests/path/to/failing_test.py::test_name
```

**Container Build Failures**
```bash
# Test Docker build locally
docker build -t seneschal-test .

# Check for missing dependencies
docker run --rm seneschal-test pip list

# Validate Dockerfile syntax
docker build --no-cache -t seneschal-test .
```

### Debugging Act Issues

```bash
# Run with verbose output
act -v

# Use specific runner image
act --container-architecture linux/amd64

# Check act version compatibility
act --version
```

## Best Practices

1. **Test Locally First**: Always run tests locally before pushing
2. **Use Act**: Validate GitHub Actions workflows locally
3. **Monitor Pipeline**: Watch for failures and performance degradation
4. **Environment Parity**: Keep development and CI environments similar
5. **Fast Feedback**: Optimize test execution time for quick feedback
6. **Clear Failures**: Ensure test failures provide actionable information
7. **Security**: Never commit secrets or sensitive data
8. **Documentation**: Keep pipeline documentation current with changes
