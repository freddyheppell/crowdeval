import pytest
from flask import url_for


class TestCanViewRateForm:
    def test_can_see_homepage(self, testapp):
        res = testapp.get(url_for("pages.index"))

        assert res.status_int == 200