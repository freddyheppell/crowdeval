from crowdeval.posts.models import Post
from flask import Blueprint

from crowdeval.extensions import db


blueprint = Blueprint("explore", __name__, static_folder="../static")


@blueprint.route("/explore")
def explore():
    posts = Post.query.order_by(Post.id.desc()).all()
    return explore_page(posts)
