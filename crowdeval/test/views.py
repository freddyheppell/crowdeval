"""Public section, including homepage and signup."""

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

blueprint = Blueprint("public", __name__, static_folder="../static")


@blueprint.route("/")
def index():
    return "hey"
