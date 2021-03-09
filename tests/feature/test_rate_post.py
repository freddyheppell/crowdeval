import pytest
from flask import url_for

from crowdeval.posts.models import Rating


class TestCanViewRateForm:
    @pytest.mark.usefixtures("test_with_authenticated_user")
    def test_can_view_rate_form(self, testapp, post):
        res = testapp.get(url_for("posts.rate", id=post.id))

        assert res.status_int == 200
        res.mustcontain(post.text)

    @pytest.mark.usefixtures("test_with_authenticated_user")
    def test_can_submit_rate_form(self, testapp, post, category):
        res = testapp.get(url_for("posts.rate", id=post.id))
        form = res.form
        form["rating"] = "0"
        form["category_id"] = str(category.id)
        form["comments"] = "Lorem ipsum"

        res = form.submit()

        rating = Rating.query.one()
        assert rating.post_id == post.id
