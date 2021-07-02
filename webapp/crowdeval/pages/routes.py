"""Public section, including homepage."""

from flask import Blueprint, render_template

blueprint = Blueprint("pages", __name__, static_folder="../static")


@blueprint.route("/")
def index():
    """Index page route."""
    return render_template("index.html")


@blueprint.route("/terms")
def terms():
    """Terms and conditions page."""
    return render_template("pages/terms.html")


@blueprint.route("/privacy")
def privacy():
    """Privacy page."""
    return render_template("pages/privacy.html")
