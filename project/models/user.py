"""
User model for authentication and user management.

This module contains the User model and related functionality for user
authentication, password management, and user-character relationships.
"""

from project import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """User model for authentication and user management."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Relationship to characters
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    characters = db.relationship("Character", backref="owner", lazy=True)

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the user's password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"
