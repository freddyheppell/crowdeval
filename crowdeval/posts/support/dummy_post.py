"""An example social network implementation."""

import json

from faker import Faker
from faker.providers import date_time, lorem, profile, python

from crowdeval.posts.support.platform import Platform


class DummyPost:
    """Represents an external post on Twitter."""

    def __init__(self, id):
        """Create a new post."""
        self.id = id

    def get_platform(self):
        """Get the enum representation of this platform."""
        return Platform.DUMMY

    def get_external_id(self):
        """Get the retrieved status id."""
        return self.id

    def get_data(self):
        faker = Faker()
        Faker.seed(self.id)
        faker.add_provider(lorem)
        faker.add_provider(profile)
        faker.add_provider(python)
        faker.add_provider(date_time)
        author = faker.simple_profile()

        return {
            "platform": self.get_platform().value,
            "external_post_id": self.id,
            "text": faker.paragraph(),
            "author_name": author["name"],
            "author_username": author["username"],
            "author_profile_url": "https://picsum.photos/seed/{id}/256/256".format(
                id=self.id
            ),
            "external_author_id": faker.pyint(),
            "additional_metadata": json.dumps({"verified": faker.pybool()}),
            "external_created_at": faker.date_time_this_century(before_now=True).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
