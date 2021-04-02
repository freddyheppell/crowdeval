"""Instantiate all flask extensions."""
from flask_bs4 import Bootstrap
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_elasticsearch import FlaskElasticsearch
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_static_digest import FlaskStaticDigest
from flask_wtf import CSRFProtect

from crowdeval.search.support.ext_bert import FlaskBert

flask_static_digest = FlaskStaticDigest()
db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = "twitter.login"

debug_toolbar = DebugToolbarExtension()
csrf = CSRFProtect()
bootstrap = Bootstrap()

es = FlaskElasticsearch()
bert = FlaskBert()

cache = Cache()
