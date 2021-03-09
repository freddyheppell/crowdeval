"""Forms for rating posts."""

from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields.core import RadioField, SelectMultipleField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, Optional

RATING_CHOICES = [
    ("0", "True"),
    ("1", "Mostly True"),
    ("2", "Mixed"),
    ("3", "Mostly False"),
    ("4", "False"),
]


class SubmitRatingForm(FlaskForm):
    """Represents a submission of a rating."""

    rating = RadioField("Rating", validators=[DataRequired()], choices=RATING_CHOICES)
    category_id = SelectMultipleField("Category")
    comments = TextAreaField("Comments", validators=[Optional(), Length(max=65000)])
    recaptcha = RecaptchaField()
