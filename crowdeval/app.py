"""The app module, builds and configures the application."""
import logging
import sys

from flask import Flask

from crowdeval import commands, extensions, posts, test, users


def create_app(config_object="crowdeval.settings"):
    """Create application."""
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)

    return app


def register_extensions(app):
    """Register extensions."""
    extensions.flask_static_digest.init_app(app)
    extensions.db.init_app(app)
    extensions.migrate.init_app(app, extensions.db)
    extensions.login_manager.init_app(app)
    extensions.debug_toolbar.init_app(app)
    extensions.csrf.init_app(app)
    extensions.bootstrap.init_app(app)


def register_blueprints(app):
    """Register application blueprints."""
    app.register_blueprint(test.views.blueprint)
    app.register_blueprint(users.routes.blueprint)
    app.register_blueprint(posts.routes.blueprint)


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": extensions.db, "User": users.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register commands to the flask cli."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
