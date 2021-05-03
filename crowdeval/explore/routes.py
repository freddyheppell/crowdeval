"""Routes for the explore blueprint."""


from flask import Blueprint, redirect, render_template, request, url_for
from sqlalchemy.orm import subqueryload

from crowdeval.extensions import cache
from crowdeval.posts.models import Post

blueprint = Blueprint("explore", __name__, static_folder="../static")

PER_PAGE = 20


def explore_page(pagination, active_filter=None, label=None):
    """Generate an explore page for a list of posts."""
    return render_template(
        "posts/explore.html",
        pagination=pagination,
        label=label,
        active_filter=active_filter,
    )


@blueprint.route("/explore")
def latest():
    """Show paginated list of latest posts."""
    page = request.args.get("page", default=1, type=int)

    posts = Post.query.order_by(Post.id.desc())

    pagination = posts.paginate(page, PER_PAGE, False)
    return explore_page(pagination=pagination, label="Latest", active_filter="latest")


@cache.memoize(0)
def post_ids_for_rating(result):
    """Get the post ids that have this rating currently."""
    posts = Post.query.all()

    filtered_posts = filter(
        lambda p: p.get_rounded_score() == result and p.is_score_certain() and p.get_rating_count() > 0, posts
    )
    filtered_ids = list(map(lambda p: p.id, filtered_posts))

    return filtered_ids


@blueprint.route("/explore/by-rating/<rating>")
def by_result(rating):
    """Get posts by rating."""
    scores = {"true": 5, "likely-true": 4, "mixed": 3, "likely-false": 2, "false": 1}
    page = request.args.get("page", default=1, type=int)

    if rating not in scores.keys():
        return redirect(url_for("explore.latest"))

    human_rating = "Posts Rated " + rating.replace("-", " ").title()

    filtered_ids = post_ids_for_rating(scores[rating])

    matching_posts = (
        Post.query.options(subqueryload("ratings"))
        .filter(Post.id.in_(filtered_ids))
        .paginate(page, PER_PAGE, False)
    )

    return explore_page(
        pagination=matching_posts, label=human_rating, active_filter=rating
    )
