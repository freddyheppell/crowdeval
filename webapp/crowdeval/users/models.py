"""Model storing user data."""
import datetime as dt

from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import UserMixin

from crowdeval.database import Column, PkModel
from crowdeval.extensions import db


class User(UserMixin, PkModel):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, username, email, **kwargs):
        """Create instance."""
        super().__init__(username=username, email=email, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"


class OAuth(OAuthConsumerMixin, db.Model):
    """Represents a social login session."""

    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)
