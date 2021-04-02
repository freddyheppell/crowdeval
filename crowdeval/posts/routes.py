"""Routes relating to posts functionality."""

from flask import Blueprint, abort, redirect, render_template
from flask.helpers import url_for
from flask_login import current_user, login_required
from sqlalchemy.orm.exc import NoResultFound

from crowdeval.extensions import db
from crowdeval.posts.forms.rate_post_form import SubmitRatingForm
from crowdeval.posts.forms.submit_post_form import SubmitPostForm
from crowdeval.posts.models import Category, Post, Rating, category_rating
from crowdeval.posts.support.post_recogniser import detect_post

blueprint = Blueprint("posts", __name__, static_folder="../static")


@blueprint.route("/post/<id>")
def show(id):
    """Return a post given an id."""
    if (post := Post.get_by_id(id)) is None:
        abort(404)

    similar_posts, total, scores = post.get_similar_posts(1, 10)

    return render_template(
        "posts/show.html",
        post=post,
        similar_posts=similar_posts[1:],
        scores=scores,
    )


@blueprint.route("/post/<id>/rate", methods=["GET", "POST"])
@login_required
def rate(id):
    """Show the rating form for a post."""
    if (post := Post.get_by_id(id)) is None:
        abort(404)

    form = SubmitRatingForm()
    form.category_id.choices = Category.get_tuples()

    if form.validate_on_submit():
        rating = Rating(rating=form.rating.data, comments=form.comments.data)
        rating.post = post
        rating.user = current_user

        db.session.add(rating)
        db.session.commit()

        for category_id in form.category_id.data:
            db.session.execute(
                category_rating.insert().values(
                    rating_id=rating.id, category_id=category_id
                )
            )
        db.session.commit()

        return redirect("/")

    return render_template("posts/rate.html", post=post, form=form)


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
            return redirect(url_for("posts.rate", id=existing_post.id))
        except NoResultFound:
            post_data = external_post.get_data()
            post = Post(**post_data)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("posts.rate", id=post.id))

    return render_template("posts/create.html", form=form)
