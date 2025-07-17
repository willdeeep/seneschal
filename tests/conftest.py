import os
import tempfile
import pytest
from project import create_app, db
from project.models import User, Character


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

        def signup(
                self,
                name='Test User',
                email='test@example.com',
                password='testpass'):
            return self._client.post(
                '/auth/signup',
                data={'name': name, 'email': email, 'password': password}
            )

    return AuthActions(client)


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on environment."""
    github_skip = pytest.mark.skip(
        reason="Skipped in GitHub Actions environment")
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


# Advanced session-scoped fixtures for complex testing scenarios

@pytest.fixture(scope="function")
def persistent_test_user(app):
    """Create a test user that persists across test operations."""
    with app.app_context():
        user = User(
            email='persistent@example.com',
            name='Persistent Test User')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()

        # Keep the user attached to the session for the entire test
        db.session.expunge(user)
        yield db.session.merge(user)

        # Cleanup after test - first delete all characters, then user
        merged_user = db.session.merge(user)
        # Delete all characters belonging to this user first
        characters = Character.query.filter_by(user_id=merged_user.id).all()
        for character in characters:
            db.session.delete(character)
        db.session.commit()

        # Now safe to delete the user
        db.session.delete(merged_user)
        db.session.commit()


@pytest.fixture(scope="function")
def character_lifecycle_setup(app, persistent_test_user):
    """
    Setup for testing complete character lifecycle scenarios.
    Returns a context manager that maintains session state.
    """
    class CharacterLifecycle:
        def __init__(self, user):
            self.user = user
            self.characters = []

        def create_character(self, **kwargs):
            """Create a character and keep it in session."""
            defaults = {
                'name': f'Test Character {len(self.characters) + 1}',
                'race': 'Human',
                'character_class': 'Fighter',
                'level': 1,
                'strength': 15, 'dexterity': 14, 'constitution': 13,
                'intelligence': 12, 'wisdom': 10, 'charisma': 8,
                'user_id': self.user.id
            }
            defaults.update(kwargs)

            character = Character(**defaults)
            db.session.add(character)
            db.session.commit()
            self.characters.append(character)
            return character

        def level_up_character(self, character, new_level):
            """Level up a character and update related stats."""
            character.level = new_level
            character.update_proficiency_bonus()
            db.session.commit()
            return character

        def add_equipment(self, character, items):
            """Add equipment to character (placeholder for future feature)."""
            # This would integrate with item management system
            pass

        def save_campaign_progress(self, character, story_beats):
            """Save character's campaign progress (future feature)."""
            # This would save character development over time
            pass

    with app.app_context():
        lifecycle = CharacterLifecycle(persistent_test_user)
        yield lifecycle

        # Cleanup all characters created during test
        for character in lifecycle.characters:
            try:
                # Refresh the character from database to ensure it's attached
                # to session
                character = db.session.merge(character)
                db.session.delete(character)
            except Exception:
                # Character might already be deleted, skip
                pass
        db.session.commit()


@pytest.fixture(scope="function")
def campaign_party_setup(app, persistent_test_user):
    """Setup a complete party of characters for campaign testing."""
    with app.app_context():
        party = {
            'tank': Character(
                name='Thorin Ironshield',
                race='Dwarf',
                character_class='Paladin',
                level=3,
                strength=16, dexterity=10, constitution=15,
                intelligence=8, wisdom=14, charisma=13,
                user_id=persistent_test_user.id
            ),
            'dps': Character(
                name='Legolas Swiftarrow',
                race='Elf',
                character_class='Ranger',
                level=3,
                strength=13, dexterity=17, constitution=12,
                intelligence=14, wisdom=15, charisma=10,
                user_id=persistent_test_user.id
            ),
            'healer': Character(
                name='Gandalf Brightstaff',
                race='Human',
                character_class='Cleric',
                level=3,
                strength=10, dexterity=12, constitution=13,
                intelligence=14, wisdom=16, charisma=15,
                user_id=persistent_test_user.id
            ),
            'utility': Character(
                name='Bilbo Lightfingers',
                race='Halfling',
                character_class='Rogue',
                level=3,
                strength=8, dexterity=18, constitution=12,
                intelligence=13, wisdom=14, charisma=16,
                user_id=persistent_test_user.id
            )
        }

        for character in party.values():
            db.session.add(character)
        db.session.commit()

        yield party

        # Cleanup
        for character in party.values():
            try:
                # Refresh the character from database to ensure it's attached
                # to session
                character = db.session.merge(character)
                db.session.delete(character)
            except Exception:
                # Character might already be deleted, skip
                pass
        db.session.commit()
