"""Instantiate all flask extensions."""
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_static_digest import FlaskStaticDigest
from flask_debugtoolbar import DebugToolbarExtension

flask_static_digest = FlaskStaticDigest()
db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = "twitter.login"

debug_toolbar = DebugToolbarExtension()