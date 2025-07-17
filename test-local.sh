#!/bin/bash
# Local test runner that mimics GitHub Actions workflow

set -e

echo "🚀 Running tests locally (GitHub Actions simulation)"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run: python -m venv .venv"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run critical linting (must pass)
echo "🔍 Running critical linting checks..."
flake8 project/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics

if [ $? -ne 0 ]; then
    echo "❌ Critical linting errors found. Please fix before continuing."
    exit 1
fi

# Run style linting (warnings only)
echo "🎨 Running style checks (warnings only)..."
flake8 project/ tests/ --count --max-complexity=15 --max-line-length=120 --statistics || echo "⚠️  Style warnings found but not blocking"

# Run unit tests
echo "🧪 Running unit tests..."
coverage run -m pytest tests/unit/ -v -m "unit and not requires_db and not requires_env and not github_skip"

if [ $? -ne 0 ]; then
    echo "❌ Unit tests failed"
    exit 1
fi

# Run functional tests
echo "🔧 Running functional tests..."
coverage run --append -m pytest tests/functional/ -v -m "functional and not github_skip and not local_only"

if [ $? -ne 0 ]; then
    echo "❌ Functional tests failed"
    exit 1
fi

# Generate coverage report
echo "📊 Generating coverage report..."
coverage report -m --skip-covered
coverage html

echo "✅ All tests passed! Coverage report generated in htmlcov/"
echo "🌐 Open htmlcov/index.html in your browser to view coverage report"
