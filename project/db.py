import click
from flask import g
from flask.cli import with_appcontext
from project import db


def get_db():
    """Get database connection."""
    if 'db' not in g:
        g.db = db
    return g.db


def close_db(e=None):
    """Close database connection."""
    g.pop('db', None)


def init_db():
    """Initialize the database with all tables."""
    db.create_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
