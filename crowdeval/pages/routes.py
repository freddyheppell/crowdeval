"""Public section, including homepage."""

from flask import Blueprint, render_template

blueprint = Blueprint("pages", __name__, static_folder="../static")


@blueprint.route("/")
def index():
    """Index page route."""
    return render_template("index.html")
