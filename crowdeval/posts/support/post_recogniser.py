"""Match URLs to a platform and extract data from them."""

import re

from crowdeval.posts.support.dummy_post import DummyPost
from crowdeval.posts.support.twitter_post import TwitterPost


class UnsupportedUrlException(Exception):
    """Exception meaning the URL could not be matched to a platform."""

    def __init__(self, url):
        """Create new exception instance."""
        super().__init__("Unable to match ${url}".format(url=url))


TWITTER_REGEXP = re.compile(
    r"https?://(?:mobile.)?twitter\.com/(?:#!/)?(\w+)/status(es)?/(\d+)", re.IGNORECASE
)

DUMMY_REGEXP = re.compile(r"https://example.org/(\d+)", re.IGNORECASE)


def detect_post(url):
    """Recognise a URL and return an external post class."""
    if twitter_url := TWITTER_REGEXP.match(url):
        return TwitterPost(twitter_url.group(3))
    elif dummy_url := DUMMY_REGEXP.match(url):
        return DummyPost(dummy_url.group(1))
    else:
        raise UnsupportedUrlException(url)
