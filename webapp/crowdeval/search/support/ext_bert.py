"""A simple flask extension to wrap Bert searching."""

from flask import _app_ctx_stack, current_app
from jina import Client


class FlaskBert(object):
    """Context wrapper for BERT client."""

    def __init__(self, app=None):
        """Create a new instance of the extension.

        Either pass app now or call init_app later.
        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialise the default config and register teardown."""
        app.config.setdefault("JINA_URL", "grpc://localhost:5555")

    def connect(self):
        """Create the connection to BERT."""
        return Client(host=current_app.config["JINA_URL"])

    @property
    def client(self):
        """Get the connection to BERT."""
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "bert"):
                ctx.bert = self.connect()
            return ctx.bert
