# Seneschal - D&D Character Management System

## About This Project

This started as a personal project to practice object-oriented programming and learn more about D&D mechanics. What began as a simple character sheet has grown into a comprehensive web application for managing D&D 5e characters and campaigns. It's been a fantastic journey exploring Flask, database design, and the intricate rules of D&D.

The project continues to evolve as I discover new aspects of both web development and tabletop gaming. Whether you're here to explore the code, contribute to development, or use it for your own campaigns, welcome to Seneschal.

## Overview

Seneschal is a Flask web application for creating, managing, and tracking Dungeons & Dragons 5th Edition characters. Built with modern web development practices, it provides an interface for players and dungeon masters to manage their campaigns.

**DISCLAIMER**: This application is developed for educational and entertainment purposes only. It is not officially affiliated with Wizards of the Coast or D&D. Users are responsible for ensuring compliance with all applicable laws and regulations. The developers assume no responsibility for any issues arising from the use of this software.

## Key Features

### Character Management
- Complete D&D 5e character sheet support
- Level progression with automatic proficiency bonus updates
- Extended character backstory fields
- Spell slot tracking and spell library integration
- Equipment and inventory management
- Combat statistics tracking

### Technical Features
- User authentication and session management
- PostgreSQL database with comprehensive D&D data models
- Docker containerization for development and deployment
- Comprehensive test suite with Pytest
- CI/CD pipeline with GitHub Actions
- Responsive Bootstrap-based interface
- Application factory pattern with modular blueprints

### D&D Integration
- Automated import of D&D 5e SRD data
- Complete race and class feature integration
- Skill and proficiency tracking
- Racial, class, and background feature management

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose (recommended)
- PostgreSQL (for production) or SQLite (for development)

## Quick Start

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/willdeeep/seneschal.git
   cd seneschal
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   python init_db.py
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the Application**
   Open your browser to `http://localhost:5000`

### Docker Development (Recommended)

1. **Start Services**
   ```bash
   docker-compose up --build
   ```

2. **Initialize Database (First Time)**
   ```bash
   docker-compose exec web python init_db.py
   ```

3. **Access the Application**
   Open your browser to `http://localhost:5000`

## Testing

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
coverage run -m pytest
coverage report
coverage html
```

### Test Categories
```bash
pytest -m unit          # Unit tests only
pytest -m functional    # Functional tests only
pytest -m requires_db   # Database-dependent tests
```

### Docker Testing
```bash
docker-compose exec web pytest
```

## Deployment

### Environment Variables

Set these environment variables for production:

- `SECRET_KEY`: Flask secret key for session security
- `DATABASE_URL`: PostgreSQL connection string
- `FLASK_ENV`: Set to 'production' for production deployment

### Production Docker Build

```bash
docker build -t seneschal:latest .
docker run -p 5000:5000 \
  -e SECRET_KEY="your-production-secret-key" \
  -e DATABASE_URL="postgresql://user:pass@host:5432/seneschal" \
  seneschal:latest
```

## Documentation

- [Database Initialization Process](docs/database-initialization.md)
- [CI/CD Pipeline Guide](docs/ci-cd-pipeline.md)
- [GitHub Workflow Guide](docs/github-workflow.md)
- [Project Structure](docs/project-structure.md)

## Development

### Contributing

1. Fork the repository
2. Create a feature branch following our [GitHub workflow guidelines](docs/github-workflow.md)
3. Make your changes with appropriate tests
4. Ensure all tests pass and code follows style guidelines
5. Submit a pull request with clear documentation

### Code Style

- Follow PEP 8 style guidelines
- Run `flake8` for linting
- Add comprehensive tests for new features
- Update documentation for API changes

## Architecture

- **Framework**: Flask with application factory pattern
- **Database**: SQLAlchemy ORM with PostgreSQL/SQLite
- **Authentication**: Flask-Login with Werkzeug password hashing
- **Frontend**: Bootstrap-based responsive templates
- **Testing**: Pytest with comprehensive test coverage
- **Deployment**: Docker containerization

## License

This project is developed for educational and personal use. It follows Flask best practices and D&D 5e System Reference Document (SRD) guidelines for educational purposes.

## Support

For questions, issues, or contributions, please use the GitHub issue tracker. This is a learning project, so constructive feedback and contributions are welcome.
