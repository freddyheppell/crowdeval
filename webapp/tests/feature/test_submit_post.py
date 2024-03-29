import pytest
import TwitterAPI
from flask import url_for
from pytest_mock import MockFixture

from crowdeval.posts.models import Post
from tests.fixtures import load_fixture


class TestSubmitPost:
    @pytest.mark.usefixtures("test_with_authenticated_user")
    def test_can_submit_tweet(self, testapp, mocker: MockFixture):

        res = testapp.get(url_for("posts.submit"))

        mocker.patch.object(
            TwitterAPI.TwitterAPI,
            "request",
            return_value=load_fixture("tweets", "1362771196945793024.json"),
        )

        form = res.form
        form["url"] = "https://twitter.com/freddyheppell/status/1362771196945793024"

        res = form.submit().follow()
        assert Post.query.one().external_post_id == "1362771196945793024"

    @pytest.mark.usefixtures("test_with_authenticated_user")
    def test_can_submit_dummy_post(self, testapp):
        res = testapp.get(url_for("posts.submit"))

        form = res.form
        form["url"] = "https://example.org/2830388933812890"

        res = form.submit().follow()
        assert Post.query.one().external_post_id == "2830388933812890"

    @pytest.mark.usefixtures("test_with_authenticated_user")
    def test_can_submit_tweet_with_emoji(self, testapp, mocker: MockFixture):
        res = testapp.get(url_for("posts.submit"))

        mocker.patch.object(
            TwitterAPI.TwitterAPI,
            "request",
            return_value=load_fixture("tweets", "500375839498723328.json"),
        )

        form = res.form
        form["url"] = "https://twitter.com/AngryBlackLady/status/500375839498723328"

        res = form.submit().follow()
        print(Post.query.one().author_name)
        assert Post.query.one().external_post_id == "500375839498723328"

    @pytest.mark.usefixtures("test_with_authenticated_user")
    def test_can_view_post(self, testapp, post):
        res = testapp.get(url_for("posts.show", id=post.id))

        assert res.status_int == 200
        res.mustcontain(post.text)
