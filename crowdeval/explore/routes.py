"""Routes for the explore blueprint."""

from flask import Blueprint, render_template, request

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
def explore():
    """Show paginated list of latest posts."""
    page = request.args.get("page", default=1, type=int)

    posts = Post.query.order_by(Post.id.desc())

    pagination = posts.paginate(page, PER_PAGE, False)
    return explore_page(pagination=pagination, label="Latest", active_filter="latest")
