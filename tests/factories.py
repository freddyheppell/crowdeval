from factory import LazyAttribute, Sequence, post_generation
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyInteger
from faker import Faker
from faker.providers import date_time, lorem, profile
from sqlalchemy.sql.expression import func

from crowdeval.database import db
from crowdeval.posts.models import Category, Post, Rating
from crowdeval.users.models import User

faker = Faker()
faker.add_provider(lorem)
faker.add_provider(profile)
faker.add_provider(date_time)

veracities = None


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


class PostFactory(BaseFactory):
    _profile = faker.simple_profile()
    platform = 1
    external_post_id = Sequence(lambda n: f"extid{n}")
    text = faker.paragraph()
    author_name = _profile["name"]
    author_username = _profile["username"]
    author_profile_url = "http://example.org"
    additional_metadata = {"verified": False}
    external_created_at = faker.date_time().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    external_author_id = "1234"

    class Meta:
        model = Post


class CategoryFactory(BaseFactory):
    name = faker.sentence()

    class Meta:
        model = Category


class RatingFactory(BaseFactory):
    user_id = LazyAttribute(lambda a: UserFactory().save().id)
    post_id = LazyAttribute(lambda a: PostFactory().save().id)
    rating = FuzzyInteger(1, 5)
    comments = LazyAttribute(lambda a: faker.paragraph())

    @post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.categories.append(group)
        else:
            # No categories passed in, pick some random ones
            category = Category.query.order_by(func.rand()).limit(1).first()
            self.categories.append(category)

    class Meta:
        model = Rating
        sqlalchemy_session = db.session
