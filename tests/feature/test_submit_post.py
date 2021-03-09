import pytest
import TwitterAPI
from flask import url_for
from flask_dance.consumer.storage import MemoryStorage
from flask_login import login_user
from pytest_mock import MockFixture

from crowdeval.posts.models import Post
from tests.fixtures import load_fixture


class TestSubmitPost:
    @pytest.mark.usefixtures("test_with_authenticated_user")
    def test_can_submit_tweet(self, testapp, user, mocker: MockFixture):
        # storage = MemoryStorage({"access_token": "fake-token"})
        # monkeypatch.setattr(tw_blueprint, "storage", storage)

        res = testapp.get(url_for("posts.submit"))
        # print(res)

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
    def test_can_view_post(self, testapp, user, post):
        res = testapp.get(url_for("posts.show", id=post.id))

        assert res.status_int == 200
        res.mustcontain(post.text)