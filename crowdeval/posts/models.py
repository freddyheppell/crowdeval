"""Models for stored posts."""

import datetime as dt

from sqlalchemy.dialects.mysql import JSON, TINYINT

from crowdeval.database import Column, PkModel
from crowdeval.extensions import db


class Post(PkModel):
    """Represents the model of a post."""

    platform = Column(TINYINT(unsigned=True), nullable=False)
    external_post_id = Column(db.String(length=64), nullable=False)
    text = Column(db.Text(), nullable=False)
    author_name = Column(db.String(length=255), nullable=False)
    external_author_id = Column(db.String(length=64), nullable=False)
    additional_metadata = Column(JSON(), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(
        self,
        platform,
        external_post_id,
        text,
        author_name,
        external_author_id,
        additional_metadata,
    ):
        """Create a new post."""
        super().__init__(
            platform=platform,
            external_post_id=external_post_id,
            text=text,
            author_name=author_name,
            external_author_id=external_author_id,
            additional_metadata=additional_metadata,
        )