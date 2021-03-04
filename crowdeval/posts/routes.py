"""Routes relating to posts functionality."""

import json

from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy.orm.exc import NoResultFound

from crowdeval.extensions import db
from crowdeval.posts.forms.submit_post_form import SubmitPostForm
from crowdeval.posts.models import Post
from crowdeval.posts.support.post_recogniser import detect_post

blueprint = Blueprint("posts", __name__, static_folder="../static")


@blueprint.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    """Submit a route, then either create or take to existing known post."""
    form = SubmitPostForm()

    if form.validate_on_submit():
        external_post = detect_post(form.url.data)

        # Check if we already know about this post
        query = Post.query.filter_by(
            platform=external_post.get_platform().value,
            external_post_id=external_post.get_external_id(),
        )

        try:
            existing_post = query.one()
            return json.dumps(existing_post)
        except NoResultFound:
            post_data = external_post.get_data()
            post = Post(**post_data)
            db.session.add_all([post])
            db.session.commit()

    return render_template("posts/create.html", form=form)
