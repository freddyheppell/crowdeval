# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import logging

import pytest
from pytest_mock import MockFixture
from webtest import TestApp

from crowdeval.app import create_app
from crowdeval.database import db as _db
from crowdeval.extensions import login_manager
from crowdeval.users.models import User

from .factories import CategoryFactory, PostFactory, UserFactory


@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app("tests.settings")
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app):
    """Create Webtest app."""
    return TestApp(app)


@pytest.fixture
def db(app):
    """Create database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def user(db):
    """Create user for the tests."""
    user = UserFactory()
    db.session.commit()
    return user


@pytest.fixture
def post(db):
    post = PostFactory()
    db.session.commit()
    return post


@pytest.fixture
def category(db):
    category = CategoryFactory()
    db.session.commit()
    return category


@pytest.fixture
def test_with_authenticated_user(app, user):
    @login_manager.request_loader
    def load_user_from_request(request):
        return User.query.first()


@pytest.fixture(autouse=True)
def mock_elasticsearch(mocker: MockFixture):
    mocker.patch("elasticsearch.Elasticsearch.index")
