import pytest
from flask import url_for


@pytest.mark.functional
class TestAppRoutes:
    """Functional tests for application routes."""

    def test_index_page(self, client):
        """
        GIVEN: A Flask application
        WHEN: The index page is requested (GET /)
        THEN: The response should be successful and contain welcome text
        """
        response = client.get('/')
        assert response.status_code == 200
        assert b'Welcome to Seneschal' in response.data

    def test_login_page_get(self, client):
        """
        GIVEN: A Flask application
        WHEN: The login page is requested (GET /auth/login)
        THEN: The response should be successful and contain login form
        """
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'Login to Your Account' in response.data
        assert b'Email address' in response.data
        assert b'Password' in response.data

    def test_signup_page_get(self, client):
        """
        GIVEN: A Flask application
        WHEN: The signup page is requested (GET /auth/signup)
        THEN: The response should be successful and contain signup form
        """
        response = client.get('/auth/signup')
        assert response.status_code == 200
        assert b'Create Your Account' in response.data
        assert b'Full Name' in response.data
        assert b'Email address' in response.data
        assert b'Password' in response.data


@pytest.mark.functional
class TestAuthentication:
    """Functional tests for authentication workflows."""

    def test_user_signup_success(self, client):
        """
        GIVEN: A Flask application
        WHEN: A new user signs up with valid data
        THEN: The user should be created and redirected to login
        """
        response = client.post('/auth/signup', data={
            'name': 'New User',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Account created successfully!' in response.data

    def test_user_signup_duplicate_email(self, client, test_user):
        """
        GIVEN: A Flask application with an existing user
        WHEN: A new user tries to sign up with the same email
        THEN: The signup should fail with appropriate error message
        """
        response = client.post('/auth/signup', data={
            'name': 'Another User',
            'email': 'test@example.com',  # Same as test_user
            'password': 'anotherpassword'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Email address already exists' in response.data

    def test_user_login_success(self, client, test_user):
        """
        GIVEN: A Flask application with a registered user
        WHEN: The user logs in with correct credentials
        THEN: The user should be authenticated and redirected to profile
        """
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'testpass'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Test User' in response.data  # Should show user's name

    def test_user_login_invalid_credentials(self, client, test_user):
        """
        GIVEN: A Flask application with a registered user
        WHEN: Someone tries to log in with incorrect credentials
        THEN: The login should fail with appropriate error message
        """
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Please check your login details' in response.data

    def test_profile_requires_login(self, client):
        """
        GIVEN: A Flask application
        WHEN: An unauthenticated user tries to access the profile page
        THEN: They should be redirected to the login page
        """
        response = client.get('/profile')
        assert response.status_code == 302  # Redirect to login

    def test_logout_functionality(self, client, auth, test_user):
        """
        GIVEN: A Flask application with a logged-in user
        WHEN: The user logs out
        THEN: They should be logged out and redirected to home page
        """
        # First login
        auth.login()
        
        # Then logout
        response = client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'You have been logged out' in response.data


@pytest.mark.functional
class TestProtectedRoutes:
    """Test protected routes that require authentication."""

    def test_profile_page_authenticated(self, client, auth, test_user):
        """
        GIVEN: A Flask application with a logged-in user
        WHEN: The user accesses their profile page
        THEN: They should see their profile information
        """
        # Login first
        auth.login()
        
        response = client.get('/profile')
        assert response.status_code == 200
        assert b'User Profile' in response.data
        assert b'Test User' in response.data
        assert b'test@example.com' in response.data
