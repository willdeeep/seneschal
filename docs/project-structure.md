# Project Structure

## Directory Overview

```
seneschal/
├── .github/                     # GitHub configuration
│   └── workflows/
│       └── run_tests.yml        # CI/CD pipeline
├── .vscode/                     # VS Code configuration
│   ├── launch.json             # Debug configurations
│   ├── tasks.json              # Development tasks
│   └── settings.json           # Python environment settings
├── docs/                        # Documentation
│   ├── database-initialization.md
│   ├── ci-cd-pipeline.md
│   ├── github-workflow.md
│   └── project-structure.md
├── project/                     # Main application package
│   ├── __init__.py             # Application factory
│   ├── auth.py                 # Authentication blueprint
│   ├── characters.py           # Character management blueprint
│   ├── main.py                 # Main routes blueprint
│   ├── models.py               # Database models
│   ├── db.py                   # Database utilities
│   └── templates/              # Jinja2 templates
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── signup.html
│       ├── profile.html
│       └── characters/         # Character-specific templates
│           ├── index.html      # Character list
│           ├── create.html     # Character creation form
│           ├── view.html       # Character sheet display
│           └── edit.html       # Character editing form
├── tests/                      # Test suite
│   ├── conftest.py            # Pytest configuration
│   ├── unit/                  # Unit tests
│   │   ├── test_models.py     # Model tests
│   │   ├── test_auth.py       # Authentication tests
│   │   └── test_character_dnd.py # D&D logic tests
│   └── functional/            # Functional tests
│       └── test_app.py        # Application integration tests
├── json_backups/              # D&D data files (gitignored)
├── instance/                  # Flask instance folder (gitignored)
├── app.py                     # Application entry point
├── init_db.py                 # Database initialization script
├── json_data_loader.py        # D&D data loading utilities
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker container definition
├── docker-compose.yml         # Multi-service orchestration
├── pytest.ini                # Pytest configuration
├── .gitignore                 # Git ignore rules
└── README.md                  # Project documentation
```

## Core Application (`project/`)

### Application Factory (`__init__.py`)

The application factory pattern enables flexible configuration and testing:

```python
def create_app(test_config=None):
    """Create and configure Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///seneschal.sqlite"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    from project import auth, characters, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(characters.bp)
    app.register_blueprint(main.bp)
    
    return app
```

### Blueprints

#### Authentication Blueprint (`auth.py`)
- User registration and login
- Session management
- Password security

#### Characters Blueprint (`characters.py`)
- Character CRUD operations
- Character sheet viewing and editing
- D&D rule integration

#### Main Blueprint (`main.py`)
- Home page and general routes
- User profile management
- Application navigation

### Database Models (`models.py`)

Comprehensive D&D 5e character modeling:

```python
class Character(db.Model):
    # Basic Information
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    race = db.Column(db.String(50), nullable=False)
    character_class = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, default=1)
    
    # Ability Scores
    strength = db.Column(db.Integer, nullable=False)
    dexterity = db.Column(db.Integer, nullable=False)
    # ... other abilities
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    proficiencies = db.relationship('Proficiency', secondary=character_proficiencies)
    # ... other relationships
```

### Templates (`templates/`)

Bootstrap-based responsive templates with Jinja2 inheritance:

- **base.html**: Main layout template
- **Character templates**: Specialized character management interfaces
- **Authentication templates**: Login and registration forms

## Configuration and Environment

### Environment Variables

```bash
# Development
FLASK_ENV=development
SECRET_KEY=development-secret-key
DATABASE_URL=sqlite:///instance/seneschal.sqlite

# Production
FLASK_ENV=production
SECRET_KEY=production-secret-key-very-secure
DATABASE_URL=postgresql://user:password@host:5432/seneschal
```

### Docker Configuration

#### Dockerfile
Multi-stage build for production optimization:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

#### docker-compose.yml
Development environment with PostgreSQL:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://seneschal:password@db:5432/seneschal
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: seneschal
      POSTGRES_USER: seneschal
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Testing Structure (`tests/`)

### Test Configuration (`conftest.py`)

Shared test fixtures and configuration:

```python
@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret-key',
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client."""
    return app.test_client()

@pytest.fixture
def authenticated_user(client):
    """Logged-in test user."""
    # User creation and authentication logic
    yield user
```

### Unit Tests (`tests/unit/`)

- **test_models.py**: Database model testing
- **test_auth.py**: Authentication logic testing
- **test_character_dnd.py**: D&D rule validation testing

### Functional Tests (`tests/functional/`)

- **test_app.py**: End-to-end application testing
- Integration testing across components
- User workflow validation

## Data Management

### D&D Data Integration

#### JSON Data Loader (`json_data_loader.py`)

Utility for loading D&D 5e SRD data:

```python
class FiveEDataLoader:
    def __init__(self, data_path=None):
        self.data_path = Path(data_path) if data_path else Path(__file__).parent / "json_backups"
        self._cache = {}
    
    def get_species(self):
        """Load race/species data."""
        return self.load_json_file("5e-SRD-Races.json")
    
    def get_classes(self):
        """Load character class data."""
        return self.load_json_file("5e-SRD-Classes.json")
```

#### Database Initialization (`init_db.py`)

Automated database setup with data population:

- Schema creation
- D&D data import
- Error handling and recovery
- User interaction for data management

### Data Storage

#### Local Development
- SQLite database in `instance/` directory
- JSON data files in `json_backups/`
- User uploads and temporary files

#### Production
- PostgreSQL database
- Environment-based configuration
- Secure file storage considerations

## Development Tools

### VS Code Configuration (`.vscode/`)

#### Debug Configurations (`launch.json`)

```json
{
    "configurations": [
        {
            "name": "Flask App",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/app.py",
            "env": {
                "FLASK_ENV": "development"
            }
        },
        {
            "name": "Run Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["-v"]
        }
    ]
}
```

#### Development Tasks (`tasks.json`)

```json
{
    "tasks": [
        {
            "label": "Run Flask App",
            "type": "shell",
            "command": "python app.py",
            "group": "build"
        },
        {
            "label": "Run Tests",
            "type": "shell",
            "command": "pytest",
            "group": "test"
        }
    ]
}
```

### Python Configuration

#### Requirements Management (`requirements.txt`)

```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.3
Werkzeug==2.3.7
gunicorn==21.2.0
pytest==7.4.2
pytest-cov==4.1.0
# ... other dependencies
```

#### Test Configuration (`pytest.ini`)

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    unit: Unit tests
    functional: Functional tests
    requires_db: Database-dependent tests
```

## Security Considerations

### File Security
- Sensitive files in `.gitignore`
- Environment variables for secrets
- Secure file upload handling

### Database Security
- SQLAlchemy ORM for query safety
- User input validation
- Session management

### Application Security
- CSRF protection (planned)
- Input sanitization
- Secure headers

## Scalability Considerations

### Database
- PostgreSQL for production scalability
- Indexed foreign keys
- Query optimization opportunities

### Application
- Blueprint modularization
- Caching strategies
- Static file serving

### Infrastructure
- Docker containerization
- Load balancer compatibility
- Health check endpoints

## Maintenance

### Regular Tasks
- Dependency updates
- Security patches
- Performance monitoring
- Database maintenance

### Code Organization
- Modular blueprint structure
- Clear separation of concerns
- Comprehensive testing
- Documentation maintenance
