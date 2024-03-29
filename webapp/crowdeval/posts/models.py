"""Models for stored posts."""

import html
from datetime import datetime
from typing import Tuple

import timeago
from sqlalchemy import func
from sqlalchemy.dialects.mysql import JSON, TINYINT
from sqlalchemy.dialects.mysql.types import TEXT

from crowdeval.database import CacheableMixin, Column, PkModel, reference_col
from crowdeval.extensions import cache, db
from crowdeval.posts.support.scoring import PostScorer, ScoreEnum
from crowdeval.search.support.db_mixin import SearchableMixin


class Post(SearchableMixin, PkModel, CacheableMixin):
    """Represents the model of a post."""

    __tablename__ = "posts"
    __searchable__ = ["text", "external_created_at"]
    __bertify__ = ["text"]
    _scorer = None

    platform = Column(TINYINT(unsigned=True), nullable=False)
    external_post_id = Column(db.String(length=64), nullable=False)
    text = Column(db.Text(), nullable=False)
    author_name = Column(db.String(length=255), nullable=False)
    author_username = Column(db.String(length=255), nullable=False)
    author_profile_url = Column(db.String(length=255), nullable=False)
    external_author_id = Column(db.String(length=64), nullable=False)
    additional_metadata = Column(JSON(), nullable=True)
    external_created_at = Column(db.DateTime, nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=datetime.utcnow)

    ratings = db.relationship(
        "Rating", order_by="desc(Rating.id)", back_populates="post"
    )

    def __init__(
        self,
        platform,
        external_post_id,
        text,
        author_name,
        author_username,
        author_profile_url,
        external_author_id,
        additional_metadata,
        external_created_at,
    ):
        """Create a new post."""
        super().__init__(
            platform=platform,
            external_post_id=external_post_id,
            text=text,
            author_name=author_name,
            author_username=author_username,
            author_profile_url=author_profile_url,
            external_author_id=external_author_id,
            additional_metadata=additional_metadata,
            external_created_at=datetime.strptime(
                external_created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
        )

    def formatted_external_created_at(self):
        """Return datetime formatted for user display of platform creation time."""
        return self.external_created_at.strftime("%I:%M %p · %b %-d, %Y")

    def formatted_created_at(self):
        """Return datetime formatted for user display of model creation time."""
        return self.created_at.strftime("%-d %b %Y, %X")

    @cache.memoize()
    def get_similar_post_ids(self, page, per_page):
        """Get posts with similar text to this one."""
        return self.bert_search(self.text, "text", page, per_page, 1.75)

    def get_scorer(self, force_rescore=False) -> PostScorer:
        """Return the scorer instance."""
        if force_rescore or self._scorer is None:
            self._scorer = PostScorer(self)

        return self._scorer

    def get_score(self, force_rescore=False) -> Tuple[float, float]:
        """Get the chosen bound and certainty width of this post's score.

        force_rescore:  Force the scorer to be recalculated
        """
        if force_rescore or self._scorer is None:
            self._scorer = PostScorer(self)

        return self._scorer.get_bound(), self._scorer.get_width()

    def get_rating_score_counts(self, force_rescore=False):
        """Get a score->freq dictionary of ratings."""
        if force_rescore or self._scorer is None:
            self._scorer = PostScorer(self)

        return self._scorer.score_counts

    @cache.memoize(120)  # memoize for 2 minutes
    def get_rounded_score(self, force_rescore=False) -> ScoreEnum:
        """Get the score rounded to the nearest integer.

        force_rescore:  Force the scorer to be recalculated
        """
        rounded = max(1, min(round(self.get_score(force_rescore)[0]), 5))
        return ScoreEnum(rounded)

    def is_score_certain(self, force_rescore=False) -> bool:
        """Is this score narrower than the threshold?."""
        if force_rescore or self._scorer is None:
            self._scorer = PostScorer(self)

        return self._scorer.get_width() < 1

    def get_rating_count(self) -> int:
        """Get the number of valid ratings for this post."""
        return len(self.ratings)

    def get_top_categories(self):
        """Get the top categories of the post."""
        # This is equivalent to
        # SELECT category_id, COUNT(category_id) FROM ratings
        # RIGHT JOIN category_rating ON ratings.id = category_rating.rating_id
        # WHERE ratings.post_id = <ID>
        # GROUP BY category_id
        # ORDER BY count(category_id) DESC
        count = func.count(category_rating.c.category_id)
        category_id_freqs = (
            db.session.query(category_rating.c.category_id, count)
            .select_from(Rating)
            .outerjoin(category_rating, Rating.id == category_rating.c.rating_id)
            .filter(Rating.post_id == self.id)
            .group_by(category_rating.c.category_id)
            .order_by(count.desc())
            .all()
        )

        return Category.query.filter(
            Category.id.in_([id for id, _ in category_id_freqs])
        ).all()

    def unescaped_text(self):
        """Get the post text with HTML entities decoded.

        The API returns some entities (e.g. &) as their HTML encoded forms (i.e. &amp;).
        If this is passed to Jinja it will double encode them (&amp;amp;).
        """
        return html.unescape(self.text)


class Rating(PkModel):
    """Represent's an individual's ratings of a post."""

    __tablename__ = "ratings"

    user_id = reference_col("users")
    user = db.relationship("User", backref="ratings")
    post_id = reference_col("posts")
    post = db.relationship("Post", back_populates="ratings")
    rating = Column(TINYINT(unsigned=True), nullable=False)
    comments = Column(TEXT(), nullable=False)
    categories = db.relationship("Category", secondary="category_rating")
    created_at = Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, rating, comments, user_id=None, post_id=None) -> None:
        """Create a new rating instance."""
        super().__init__(
            rating=rating, comments=comments, user_id=user_id, post_id=post_id
        )

    def to_enum(self) -> ScoreEnum:
        """Return the instance of the rating enum for this rating."""
        return ScoreEnum(self.rating)

    def get_human_created_at(self) -> str:
        """Get the time difference string for the created at date."""
        return timeago.format(self.created_at, datetime.now())

    @staticmethod
    def check_exists_for(post_id, user_id):
        """Check if this user has already submitted a review for this post."""
        return (
            Rating.query.filter(
                Rating.post_id == post_id, Rating.user_id == user_id
            ).first()
            is not None
        )


class Category(PkModel):
    """Represents a category of rumour."""

    __tablename__ = "categories"

    name = Column(db.String(length=64), nullable=False)
    icon_class = Column(db.String(length=64), nullable=True)
    category_type = Column(db.String(length=64), nullable=True)

    def __init__(self, name, icon_class=None, category_type=None):
        """Create a new category."""
        super().__init__(name=name, icon_class=icon_class, category_type=category_type)

    @staticmethod
    def get_tuples(categories):
        """Return a list of (id, name) tuples of all categories."""
        category_tuples = []
        for category in categories:
            category_tuples.append((str(category.id), category.name))

        return category_tuples


category_rating = db.Table(
    "category_rating",
    db.Column("category_id", db.Integer, db.ForeignKey("categories.id")),
    db.Column("rating_id", db.Integer, db.ForeignKey("ratings.id")),
)
