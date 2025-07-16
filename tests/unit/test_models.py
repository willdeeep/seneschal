import pytest
from project.models import User
from project import db


@pytest.mark.unit
class TestUserModel:
    """Test cases for the User model."""

    def test_user_creation(self, app):
        """
        GIVEN: A new user with email, name, and password
        WHEN: The user is created
        THEN: The user should be created with correct attributes
        """
        with app.app_context():
            user = User(email='test@example.com', name='Test User')
            user.set_password('testpass')
            
            assert user.email == 'test@example.com'
            assert user.name == 'Test User'
            assert user.password_hash is not None
            assert user.password_hash != 'testpass'  # Password should be hashed

    def test_password_hashing(self, app):
        """
        GIVEN: A user with a password
        WHEN: The password is set using set_password method
        THEN: The password should be hashed and verifiable
        """
        with app.app_context():
            user = User(email='test@example.com', name='Test User')
            user.set_password('testpass')
            
            assert user.check_password('testpass') is True
            assert user.check_password('wrongpass') is False

    def test_user_representation(self, app):
        """
        GIVEN: A user instance
        WHEN: The user is converted to string representation
        THEN: It should return the email in the format '<User email>'
        """
        with app.app_context():
            user = User(email='test@example.com', name='Test User')
            assert str(user) == '<User test@example.com>'

    @pytest.mark.functional
    def test_user_persistence(self, app):
        """
        GIVEN: A new user
        WHEN: The user is saved to the database
        THEN: The user should be retrievable from the database
        """
        with app.app_context():
            user = User(email='test@example.com', name='Test User')
            user.set_password('testpass')
            
            db.session.add(user)
            db.session.commit()
            
            retrieved_user = User.query.filter_by(email='test@example.com').first()
            assert retrieved_user is not None
            assert retrieved_user.email == 'test@example.com'
            assert retrieved_user.name == 'Test User'
            assert retrieved_user.check_password('testpass') is True

    def test_unique_email_constraint(self, app):
        """
        GIVEN: Two users with the same email
        WHEN: Both users are added to the database
        THEN: Only the first user should be saved (unique constraint)
        """
        with app.app_context():
            user1 = User(email='test@example.com', name='Test User 1')
            user1.set_password('testpass1')
            
            user2 = User(email='test@example.com', name='Test User 2')
            user2.set_password('testpass2')
            
            db.session.add(user1)
            db.session.commit()
            
            db.session.add(user2)
            with pytest.raises(Exception):  # Should raise integrity error
                db.session.commit()
