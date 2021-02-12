"""Public section, including homepage and signup."""

from flask import Blueprint, render_template

blueprint = Blueprint("public", __name__, static_folder="../static")


@blueprint.route("/")
def index():
    """Test route."""
    return render_template("index.html")
