# ⚔️ Seneschal - D&D Character Management System

**Seneschal** is a comprehensive Flask web application for creating, managing, and tracking Dungeons & Dragons 5th Edition characters. Built with modern web development practices, it provides an intuitive interface for players and dungeon masters to manage their campaigns.

## 🎲 Features

### Character Management
- 🧙‍♂️ **Complete Character Creation**: Full D&D 5e character sheet support
- 📈 **Level Progression**: Experience tracking and automatic proficiency bonus updates
- 🎭 **Enhanced Backstory**: Extended character background fields beyond basic traits
- 🔮 **Spell Management**: Spell slot tracking and spell library integration
- 🎒 **Inventory System**: Equipment tracking with condition and attunement support
- 🏹 **Combat Ready**: Initiative, HP, armor class, and death save tracking

### Technical Features
- 🔐 **Secure Authentication**: User registration, login, and session management with Flask-Login
- 📊 **PostgreSQL Database**: Robust relational database with comprehensive D&D data models
- 🐳 **Docker Ready**: Containerized for both development and production deployment
- 🧪 **Comprehensive Testing**: Unit and functional tests with Pytest and code coverage
- 🎯 **Advanced Debugging**: VS Code debugging configurations for all scenarios
- 🚀 **CI/CD Ready**: GitHub Actions workflow for continuous integration
- 🎨 **Modern UI**: Bootstrap-based responsive interface optimized for character sheets
- 🏗️ **Best Practices**: Application factory pattern, blueprints, and modular structure

### D&D Integration
- 📚 **D20 SRD Data**: Automated import of official D&D 5e reference data
- 🏛️ **Race & Class Support**: Complete race and class feature integration
- 🗣️ **Language & Proficiency**: Comprehensive skill and tool proficiency tracking
- ✨ **Feature Management**: Racial, class, and background feature tracking
- 🎲 **Dice Integration**: Built-in dice rolling and modifier calculations

## 📁 Project Structure

```
seneschal/
├── .github/
│   └── workflows/
│       └── run_tests.yml          # CI/CD pipeline
├── .vscode/                       # VS Code debugging configurations
│   ├── launch.json               # Debug scenarios for D&D app
│   ├── tasks.json                # Development tasks
│   └── settings.json             # Python environment settings
├── project/                       # Main application package
│   ├── __init__.py               # Application factory
│   ├── auth.py                   # Authentication blueprint
│   ├── characters.py             # Character management blueprint
│   ├── main.py                   # Main routes blueprint
│   ├── models.py                 # D&D character and game models
│   ├── db.py                     # Database utilities
│   └── templates/                # Jinja2 templates
│       ├── base.html
│       ├── index.html
│       ├── characters/           # Character-specific templates
│       │   ├── create.html       # Character creation form
│       │   ├── view.html         # Character sheet display
│       │   └── list.html         # Character list
│       ├── auth/                 # Authentication templates
│       │   ├── login.html
│       │   └── signup.html
│       └── includes/             # Reusable template components
├── scraper/                      # D20 SRD data scraping
│   ├── populate_with_enhanced_d20srd.py  # Main data import script
│   ├── scrapers/                 # Individual data scrapers
│   ├── data/                     # Scraped D&D reference data
│   └── config.py                 # Scraper configuration
├── tests/                        # Test suite
│   ├── conftest.py              # Pytest configuration
│   ├── unit/                    # Unit tests
│   │   ├── test_models.py       # Character model tests
│   │   └── test_auth.py         # Authentication tests
│   └── functional/              # Functional tests
│       ├── test_character_creation.py
│       └── test_app.py
├── sql/                          # Database schemas and migrations
│   └── schema.sql               # PostgreSQL schema
├── debug_character_validation.py # Character model debugging script
├── create_tables.py             # Database initialization
├── init_db.py                   # Database setup utility
├── app.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker container definition
├── docker-compose.yml           # Multi-service orchestration (Flask + PostgreSQL)
├── pytest.ini                  # Pytest configuration
├── .gitignore                   # Git ignore rules
└── .gitattributes              # Git file handling rules
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- PostgreSQL (for production) or Docker for development

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd seneschal
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```bash
   # Option 1: Using Docker (Recommended)
   docker-compose up -d db
  
   # Option 2: Local PostgreSQL
   # Create database 'seneschal' with user 'seneschal'
   ```

5. **Initialize the database schema**
   ```bash
   python create_tables.py
   ```

6. **Populate with D&D 5e reference data**
   ```bash
   python scraper/populate_with_enhanced_d20srd.py
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Visit the application**
   Open your browser and go to `http://localhost:5000`

### 🐳 Docker Development (Recommended)

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Initialize database (first time only)**
   ```bash
   # In another terminal, while containers are running:
   docker-compose exec web python create_tables.py
   docker-compose exec web python scraper/populate_with_enhanced_d20srd.py
   ```

3. **Visit the application**
   Open your browser and go to `http://localhost:5000`

### 🎯 VS Code Debugging

The project includes comprehensive VS Code debugging configurations:

1. **Open the project in VS Code**
2. **Go to Run and Debug (F5)**
3. **Select a debug configuration:**
   - 🎯 **Flask App (Local Development)** - Standard debugging
   - 🎲 **Character Creation Debug** - Debug character workflows
   - 🛡️ **Character Model Validation** - Test character models
   - 🧪 **Run Unit Tests** - Debug test execution

### 🧪 Testing

#### Run all tests
```bash
pytest
```

#### Run specific test categories
```bash
# Unit tests only
pytest tests/unit/

# Functional tests only
pytest tests/functional/

# Character model tests
pytest tests/unit/test_models.py -v
```

#### Run with coverage
```bash
coverage run -m pytest
coverage report
coverage html  # Generate HTML coverage report
```

#### Debug specific tests
```bash
# Use VS Code "Debug Specific Test" configuration
# Or run manually:
pytest tests/unit/test_models.py::TestCharacter::test_ability_modifiers -v -s
```

#### Run specific test types
```bash
pytest -m unit          # Unit tests only
pytest -m functional    # Functional tests only
```

## 🎲 D&D Character Management

### Character Creation Workflow

1. **Basic Information**: Name, race, class, background, alignment
2. **Ability Scores**: Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma
3. **Skills & Proficiencies**: Class-based and background proficiencies
4. **Equipment**: Starting gear based on class and background
5. **Backstory**: Enhanced character background including:
   - Why is your character adventuring?
   - What motivates your character?
   - Where did your character grow up?
   - Why is your character their current class?
   - Special attachments to people, places, things
   - Does your character have a secret?
   - What is your character like and why?

### Supported D&D Content

- **All PHB Races**: Including variant humans and subraces
- **All PHB Classes**: With subclass support
- **Complete Spell System**: Spell slots, known spells, and spellcasting
- **Equipment Management**: Weapons, armor, tools, and magic items
- **Character Features**: Racial traits, class features, and background features
- **Leveling System**: Automatic proficiency bonus and feature unlocking

### Character Sheet Features

- **Combat Statistics**: AC, HP, initiative, death saves
- **Ability Checks**: Automatic modifier calculations
- **Saving Throws**: Proficiency tracking and bonus calculations
- **Skills**: Proficiency and expertise support
- **Spell Tracking**: Spell slots, prepared spells, and spell details
- **Inventory Management**: Equipment condition and attunement tracking

## 🗃️ Database Models

### Character Model
The heart of the application with comprehensive D&D 5e support:

```python
class Character(db.Model):
    # Basic Information
    name, race, character_class, level, background, alignment

    # Ability Scores
    strength, dexterity, constitution, intelligence, wisdom, charisma

    # Combat Stats
    current_hp, max_hp, armor_class, initiative, speed

    # Enhanced Backstory Fields
    why_adventuring, motivation, origin, class_origin,
    attachments, secret, attitude_origin

    # Relationships
    proficiencies, languages, features, spells, inventory, spell_slots
```

### Supporting Models
- **Proficiency**: Skills, weapons, tools, armor proficiencies
- **Language**: Character languages (Common, Elvish, etc.)
- **Feature**: Racial traits, class features, background features
- **Spell**: Complete D&D 5e spell database
- **Item**: Weapons, armor, equipment with full D&D properties
- **SpellSlot**: Spell slot tracking by level

## 🛠️ API Endpoints

### Character Management
- `GET /characters` - List user's characters
- `GET /characters/create` - Character creation form
- `POST /characters/create` - Create new character
- `GET /characters/<id>` - View character sheet
- `PUT /characters/<id>` - Update character
- `DELETE /characters/<id>` - Delete character

### Character Data APIs
- `GET /api/races` - Available races (with filtering)
- `GET /api/classes` - Available classes (with filtering)
- `GET /api/spells` - Spell database
- `GET /api/equipment` - Equipment database

### Authentication
- `GET /auth/login` - Login page
- `POST /auth/login` - Process login
- `GET /auth/signup` - Registration page
- `POST /auth/signup` - Process registration
- `GET /auth/logout` - Logout user

## 📊 Production Deployment

### Environment Variables

- `SECRET_KEY`: Flask secret key for session security
- `DATABASE_URL`: PostgreSQL connection string
- `FLASK_ENV`: Set to 'production' for production deployment

### Docker Production

```bash
# Build production image
docker build -t seneschal:latest .

# Run with PostgreSQL
docker run -p 5000:5000 \
  -e SECRET_KEY="your-production-secret-key" \
  -e DATABASE_URL="postgresql://user:pass@host:5432/seneschal" \
  seneschal:latest
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Run linting (`flake8 project/ tests/`)
7. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comprehensive tests for new features
- Update documentation for API changes
- Use descriptive commit messages
- Test with both SQLite (development) and PostgreSQL (production)

## 🔒 Security Considerations

- **Password Security**: Werkzeug PBKDF2 password hashing
- **Session Management**: Flask-Login secure session handling
- **CSRF Protection**: Form-based CSRF protection in production
- **Input Validation**: SQLAlchemy ORM with parameter binding
- **Container Security**: Non-root user in Docker container
- **Environment Isolation**: Secrets via environment variables

## 📜 License

This project is built for educational and personal use, following Flask best practices and D&D 5e System Reference Document (SRD) guidelines.

## 🏗️ Architecture Decisions

- **Application Factory Pattern**: Flexible configuration and testing support
- **Blueprint Organization**: Modular route organization (auth, characters, main)
- **SQLAlchemy ORM**: Database abstraction with relationship mapping
- **Many-to-Many Relationships**: Character-to-proficiency/spell associations
- **Enhanced Character Model**: Extended backstory fields beyond basic D&D
- **Docker Multi-service**: Flask app + PostgreSQL container orchestration
- **VS Code Integration**: Comprehensive debugging configurations
- **Automated Testing**: Pytest with character-specific test scenarios

## 🎯 Roadmap

- [ ] **Spell Slot Management**: Visual spell slot tracking interface
- [ ] **Combat Tracker**: Initiative order and combat state management
- [ ] **Campaign Management**: Multi-character campaign support
- [ ] **Dice Rolling**: Integrated dice roller with character modifiers
- [ ] **Character Portraits**: Image upload and management
- [ ] **Export Features**: PDF character sheet generation
- [ ] **Mobile Responsive**: Enhanced mobile character sheet interface
- [ ] **Real-time Updates**: WebSocket support for shared sessions
