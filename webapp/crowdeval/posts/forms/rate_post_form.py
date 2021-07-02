"""Forms for rating posts."""

from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields.core import RadioField, SelectMultipleField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, Optional

RATING_CHOICES = [
    ("5", "True"),
    ("4", "Mostly True"),
    ("3", "Mixed"),
    ("2", "Mostly False"),
    ("1", "False"),
]


class SubmitRatingForm(FlaskForm):
    """Represents a submission of a rating."""

    rating = RadioField("Rating", validators=[DataRequired()], choices=RATING_CHOICES)
    category_id = SelectMultipleField("Category")
    comments = TextAreaField("Comments", validators=[Optional(), Length(max=65000)])
    recaptcha = RecaptchaField()
