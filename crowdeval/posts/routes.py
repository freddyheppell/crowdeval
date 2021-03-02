from flask import Blueprint, render_template, request, flash
from flask_login import login_required

from crowdeval.posts.forms.submit_post_form import SubmitPostForm
from crowdeval.posts.models import Post

blueprint = Blueprint("posts", __name__, static_folder="../static")


@blueprint.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    form = SubmitPostForm()

    if form.validate_on_submit():
        return "validated"

    return render_template('posts/create.html', form=form)
