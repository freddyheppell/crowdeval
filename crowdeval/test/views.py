"""Public section, including homepage and signup."""

from flask import Blueprint

blueprint = Blueprint("public", __name__, static_folder="../static")


@blueprint.route("/")
def index():
    """Test route."""
    return "hey"
