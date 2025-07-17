from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """Home page."""
    return render_template("index.html")


@bp.route("/profile")
@login_required
def profile():
    """User profile page - requires authentication."""
    return render_template("profile.html", name=current_user.name)
