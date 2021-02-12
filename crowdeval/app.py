"""The app module, builds and configures the application."""
import logging
import sys

from flask import Flask

from crowdeval import commands, test
from crowdeval.extensions import flask_static_digest


def create_app(config_object="crowdeval.settings"):
    """Create application."""
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    configure_logger(app)

    return app


def register_extensions(app):
    """Register extensions."""
    flask_static_digest.init_app(app)


def register_blueprints(app):
    """Register application blueprints."""
    app.register_blueprint(test.views.blueprint)


def register_commands(app):
    """Register commands to the flask cli."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
