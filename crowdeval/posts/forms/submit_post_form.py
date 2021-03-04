"""Validation logic for create post form submission."""

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField
from wtforms.validators import URL, DataRequired


class SubmitPostForm(FlaskForm):
    """Represents a submission of the post form."""

    url = StringField("url", validators=[DataRequired(), URL(require_tld=True)])
    recaptcha = RecaptchaField()
