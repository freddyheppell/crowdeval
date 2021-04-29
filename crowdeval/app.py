"""The app module, builds and configures the application."""
import logging
import os
import sys

from flask import Flask, send_from_directory

from crowdeval import (
    commands,
    explore,
    extensions,
    pages,
    posts,
    template_filters,
    users,
)


def create_app(config_object="crowdeval.settings"):
    """Create application."""
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    register_commands(app)
    register_template_filters(app)
    register_basic_routes(app)
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
    extensions.es.init_app(app)
    extensions.bert.init_app(app)
    extensions.cache.init_app(app)


def register_blueprints(app):
    """Register application blueprints."""
    app.register_blueprint(users.routes.blueprint)
    app.register_blueprint(posts.routes.blueprint)
    app.register_blueprint(explore.routes.blueprint)
    app.register_blueprint(pages.routes.blueprint)


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
    app.cli.add_command(commands.create_index)
    app.cli.add_command(commands.import_tweet_seeds)
    app.cli.add_command(commands.wipeout)
    app.cli.add_command(commands.seed_ratings)
    app.cli.add_command(commands.reindex)
    app.cli.add_command(commands.recache_explore)


def register_template_filters(app):
    """Register custom filters."""
    app.register_blueprint(template_filters.blueprint)


def register_basic_routes(app):
    """Register simple routes."""

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "icons/favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
