import os
import tempfile
import pytest
from project import create_app, db
from project.models import User


def is_github_actions():
    """Check if running in GitHub Actions environment."""
    return os.getenv('GITHUB_ACTIONS') == 'true'


def is_ci_environment():
    """Check if running in any CI environment."""
    return any([
        os.getenv('CI'),
        os.getenv('GITHUB_ACTIONS'),
        os.getenv('TRAVIS'),
        os.getenv('CIRCLECI'),
        os.getenv('JENKINS_URL')
    ])


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    # Use SQLite for all tests to ensure CI compatibility
    config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SECRET_KEY': 'test-secret-key',
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }
    
    # Add CI-specific configuration
    if is_ci_environment():
        config.update({
            'CI_ENVIRONMENT': True,
            'SQLALCHEMY_ENGINE_OPTIONS': {
                'pool_pre_ping': True,
                'pool_recycle': 300,
            }
        })
    
    app = create_app(config)

    # Create the database and the database table
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    """Authentication helper for tests."""
    class AuthActions:
        def __init__(self, client):
            self._client = client

        def login(self, email='test@example.com', password='testpass'):
            return self._client.post(
                '/auth/login',
                data={'email': email, 'password': password}
            )

        def logout(self):
            return self._client.get('/auth/logout')

        def signup(self, name='Test User', email='test@example.com', password='testpass'):
            return self._client.post(
                '/auth/signup',
                data={'name': name, 'email': email, 'password': password}
            )

    return AuthActions(client)


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on environment."""
    github_skip = pytest.mark.skip(reason="Skipped in GitHub Actions environment")
    requires_network_skip = pytest.mark.skip(reason="Requires network access")
    local_only_skip = pytest.mark.skip(reason="Local development only")
    
    for item in items:
        # Skip tests marked as github_skip when in GitHub Actions
        if "github_skip" in item.keywords and is_github_actions():
            item.add_marker(github_skip)
        
        # Skip tests marked as local_only when in CI
        if "local_only" in item.keywords and is_ci_environment():
            item.add_marker(local_only_skip)
        
        # Skip network tests in CI unless explicitly enabled
        if "requires_network" in item.keywords and is_ci_environment():
            if not os.getenv('ENABLE_NETWORK_TESTS'):
                item.add_marker(requires_network_skip)


@pytest.fixture
def test_user(app):
    """Create a test user in the database."""
    with app.app_context():
        user = User(email='test@example.com', name='Test User')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def populated_db(app):
    """Create a test database with sample D&D data."""
    with app.app_context():
        from project.models import Character, Proficiency, Language
        
        # Create test user
        user = User(email='testuser@example.com', name='Test User')
        user.set_password('testpass')
        db.session.add(user)
        db.session.flush()  # Get user ID
        
        # Create test character
        character = Character(
            name="Test Character",
            race="Human",
            character_class="Fighter",
            level=1,
            strength=15,
            dexterity=14,
            constitution=13,
            intelligence=12,
            wisdom=10,
            charisma=8,
            user_id=user.id
        )
        db.session.add(character)
        
        # Create test proficiencies
        athletics = Proficiency(
            name="Athletics",
            proficiency_type="skill",
            associated_ability="strength"
        )
        longswords = Proficiency(
            name="Longswords",
            proficiency_type="weapon"
        )
        db.session.add_all([athletics, longswords])
        
        # Create test language
        common = Language(name="Common", language_type="Standard")
        db.session.add(common)
        
        db.session.commit()
        
        return {
            'user': user,
            'character': character,
            'proficiencies': [athletics, longswords],
            'languages': [common]
        }
