from crowdeval.posts.models import Category, Post
from factory import Sequence
from factory.alchemy import SQLAlchemyModelFactory

from crowdeval.database import db
from crowdeval.users.models import User

from faker import Faker
from faker.providers import lorem, profile, date_time

faker = Faker()
faker.add_provider(lorem)
faker.add_provider(profile)
faker.add_provider(date_time)

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
    text =  faker.paragraph()
    author_name = _profile['name']
    author_username = _profile['username']
    author_profile_url = "http://example.org"
    additional_metadata = {'verified': False}
    external_created_at = faker.date_time().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    external_author_id = '1234'

    class Meta:
        model = Post

class CategoryFactory(BaseFactory):
    name = faker.sentence()
    
    class Meta:
        model = Category