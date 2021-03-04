from factory import Sequence
from factory.alchemy import SQLAlchemyModelFactory

from crowdeval.database import db
from crowdeval.users.models import User


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    username = Sequence(lambda n: f"user{n}")
    email = Sequence(lambda n: f"user{n}@example.org")
    is_admin = False

    class Meta:
        model = User
