#!/bin/bash
# Git Repository Initialization Script for Seneschal D&D Project

echo "🎲 Initializing Seneschal D&D Character Management Git Repository"
echo "================================================================"

# Initialize git repository
echo "📝 Initializing git repository..."
git init

# Add all files respecting .gitignore
echo "📁 Adding files to staging area..."
git add .

# Check what will be committed
echo "📋 Files to be committed:"
git status --short

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "🎉 Initial commit: D&D Character Management System

✨ Features:
- Complete D&D 5e character creation and management
- PostgreSQL database with comprehensive character models
- Flask web application with authentication
- VS Code debugging configurations
- Docker containerization
- Comprehensive test suite
- D20 SRD data integration

🏗️ Architecture:
- Flask application factory pattern
- SQLAlchemy ORM with relationship mapping
- Blueprint-based modular organization
- Enhanced character backstory fields
- Spell slot and inventory management
- Proficiency and feature tracking

🔧 Development Tools:
- VS Code debugging scenarios
- Docker Compose development environment
- Pytest testing framework
- Code coverage reporting
- Automated CI/CD ready"

echo ""
echo "✅ Git repository initialized successfully!"
echo ""
echo "🚀 Next steps:"
echo "1. Create a GitHub repository"
echo "2. Add remote origin:"
echo "   git remote add origin https://github.com/yourusername/seneschal.git"
echo "3. Push to GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "🎯 Your D&D project is ready for version control!"
