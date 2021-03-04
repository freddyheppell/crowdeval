import pytest

from crowdeval.posts.support.dummy_post import DummyPost
from crowdeval.posts.support.post_recogniser import UnsupportedUrlException, detect_post
from crowdeval.posts.support.twitter_post import TwitterPost


class TestPostRecogniser:
    @pytest.mark.parametrize(
        "url,expected_id",
        [
            (
                "https://twitter.com/freddyheppell/status/1362771196945793024",
                "1362771196945793024",
            ),
            (
                "http://twitter.com/freddyheppell/status/1362771196945793024",
                "1362771196945793024",
            ),
            (
                "https://twitter.com/#!/freddyheppell/status/1362771196945793024",
                "1362771196945793024",
            ),
            (
                "https://mobile.twitter.com/freddyheppell/status/1362771196945793024",
                "1362771196945793024",
            ),
            (
                "https://twitter.com/MLHacks/status/1321819281433202690/photo/1",
                "1321819281433202690",
            ),
        ],
    )
    def test_can_recognise_twitter_url(self, url, expected_id):
        post = detect_post(url)

        assert isinstance(post, TwitterPost)
        assert post.get_external_id() == expected_id

    @pytest.mark.parametrize(
        "url",
        [
            "https://twitter.com/freddyheppell",
            "https://about.twitter.com/",
            "https://sheffield.ac.uk",
        ],
    )
    def test_fails_non_status_twitter_urls(self, url):
        with pytest.raises(UnsupportedUrlException):
            detect_post(url)

    def test_can_recognise_dummy_url(self):
        post = detect_post("https://example.org/389102382901")

        assert isinstance(post, DummyPost)
        assert post.get_external_id() == "389102382901"
