"""Models for stored posts."""

from datetime import datetime

from sqlalchemy.dialects.mysql import JSON, TINYINT
from sqlalchemy.dialects.mysql.types import TEXT
from sqlalchemy.sql.schema import PrimaryKeyConstraint

from crowdeval.database import Column, Model, PkModel, reference_col
from crowdeval.extensions import db


class Post(PkModel):
    """Represents the model of a post."""

    __tablename__ = "posts"

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


class Rating(PkModel):
    """Represent's an individual's ratings of a post."""

    __tablename__ = "ratings"

    user_id = reference_col("users")
    user = db.relationship("User", backref="ratings")
    post_id = reference_col("posts")
    post = db.relationship("Post", backref="ratings")
    rating = Column(TINYINT(unsigned=True), nullable=False)
    comments = Column(TEXT(), nullable=False)
    categories = db.relationship("Category", secondary="category_rating")

    def __init__(self, rating, comments):
        """Create a new rating instance."""
        super().__init__(rating=rating, comments=comments)


class Category(PkModel):
    """Represents a category of rumour."""

    __tablename__ = "categories"

    name = Column(db.String(length=64), nullable=False)
    icon_class = Column(db.String(length=64), nullable=True)
    category_type = Column(db.String(length=64), nullable=True)

    def __init__(self, name, icon_class, category_type):
        """Create a new category."""
        super().__init__(name=name, icon_class=icon_class, category_type=category_type)

    @staticmethod
    def get_tuples():
        categories = Category.query.all()

        category_tuples = []
        for category in categories:
            category_tuples.append((str(category.id), category.name))

        return category_tuples

category_rating = db.Table('category_rating',
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id')),
    db.Column('rating_id', db.Integer, db.ForeignKey('ratings.id'))
)
