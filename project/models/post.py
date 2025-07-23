"""
Post model for user-generated content.

This module contains the Post model for user-generated content and community features.
"""

from project import db


class Post(db.Model):
    """Post model for user-generated content."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship to User
    author = db.relationship("User", backref=db.backref("posts", lazy=True))

    def __repr__(self):
        return f"<Post {self.title}>"
