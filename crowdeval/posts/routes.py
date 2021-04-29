"""Routes relating to posts functionality."""


from itertools import groupby

from flask import Blueprint, abort, flash, redirect, render_template
from flask.helpers import url_for
from flask_login import current_user, login_required
from sqlalchemy.orm import subqueryload
from sqlalchemy.orm.exc import NoResultFound

from crowdeval.extensions import db
from crowdeval.posts.forms.rate_post_form import SubmitRatingForm
from crowdeval.posts.forms.submit_post_form import SubmitPostForm
from crowdeval.posts.models import Category, Post, Rating, category_rating
from crowdeval.posts.support.post_recogniser import detect_post
from crowdeval.posts.support.scoring import ScoreEnum, WeightedAverageSimilarPostScorer

blueprint = Blueprint("posts", __name__, static_folder="../static")


@blueprint.route("/post/<id>")
def show(id):
    """Return a post given an id."""
    if (post := Post.query.options(subqueryload("ratings")).get(id)) is None:
        abort(404)

    similar_post_ids, total, scores = post.get_similar_post_ids(page=1, per_page=64)
    similar_posts = (
        Post.query.options(subqueryload("ratings"))
        .filter(Post.id.in_(similar_post_ids))
        .all()
    )
    weighted_scorer = WeightedAverageSimilarPostScorer(similar_posts, scores)
    similar_post_score = weighted_scorer.get_score()
    similar_post_rating = ScoreEnum(max(1, min(round(similar_post_score), 5)))
    post_count = Post.fast_count()
    return render_template(
        "posts/show.html",
        post=post,
        similar_posts=similar_posts[1:],
        scores=scores,
        similar_post_score=similar_post_score,
        similar_post_rating=similar_post_rating,
        post_count=post_count,
    )


@blueprint.route("/post/<id>/stats")
def stats(id):
    """Show statistics about a post."""
    if (post := Post.query.options(subqueryload("ratings")).get(id)) is None:
        abort(404)

    return render_template("posts/stats.html", post=post)


@blueprint.route("/post/<id>/rate", methods=["GET", "POST"])
@login_required
def rate(id):
    """Show the rating form for a post."""
    if (post := Post.get_by_id(id)) is None:
        abort(404)

    form = SubmitRatingForm()
    categories = Category.query.all()
    form.category_id.choices = Category.get_tuples(categories)
    grouped_categories = {
        k: list(g)
        for k, g in groupby(
            categories, lambda t: t.category_type if t.category_type is not None else ""
        )
    }

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

        flash("Your review has been added succesfully", category="success")
        return redirect(url_for("posts.show", id=post.id))

    return render_template(
        "posts/rate.html", post=post, form=form, grouped_categories=grouped_categories
    )


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
            flash("existing", "post_submit_status")
            return redirect(url_for("posts.show", id=existing_post.id))
        except NoResultFound:
            post_data = external_post.get_data()
            post = Post(**post_data)
            db.session.add(post)
            db.session.commit()
            flash("new", "post_submit_status")
            return redirect(url_for("posts.rate", id=post.id))

    return render_template("posts/create.html", form=form)
