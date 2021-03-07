"""Models for stored posts."""

from datetime import datetime

from sqlalchemy.dialects.mysql import JSON, TINYINT
from sqlalchemy.dialects.mysql.types import TEXT

from crowdeval.database import Column, PkModel, reference_col
from crowdeval.extensions import db


class Post(PkModel):
    """Represents the model of a post."""

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

    def formatted_date(self):
        """Return datetime formatted for user display."""
        return self.external_created_at.strftime("%I:%M %p · %b %d, %Y")


class Rating(PkModel):
    """Represent's an individual's ratings of a post."""

    user_id = reference_col("users")
    user = db.relationship("User", backref="ratings")
    rating = Column(TINYINT(unsigned=True), nullable=False)
    comments = Column(TEXT(), nullable=False)

    def __init__(self, rating, comments):
        """Create a new rating instance."""
        super().__init__(rating=rating, comments=comments)
