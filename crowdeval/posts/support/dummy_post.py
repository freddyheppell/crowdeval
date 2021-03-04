"""An example social network implementation."""


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
