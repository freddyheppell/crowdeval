import re

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField
from wtforms.validators import DataRequired, URL, Regexp


class SubmitPostForm(FlaskForm):
    url = StringField('url', validators=[DataRequired(), URL(require_tld=True)])
    recaptcha = RecaptchaField()
