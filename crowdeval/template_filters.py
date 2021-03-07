"""Custom template filters."""

import re

from flask import Blueprint
from jinja2 import Markup, escape, evalcontextfilter

blueprint = Blueprint("custom_template_filters", __name__)


@evalcontextfilter
@blueprint.app_template_filter()
def newline_to_br(context, value: str) -> str:
    """Replace newlines with break tags."""
    result = "<br /> ".join(re.split(r"(?:\r\n|\r|\n)", escape(value)))

    if context.autoescape:
        result = Markup(result)

    return result
