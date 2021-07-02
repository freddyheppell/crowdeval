"""A simple flask extension to wrap Bert searching."""

from bert_serving.client import BertClient
from flask import _app_ctx_stack, current_app


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
        app.config.setdefault("BERT_HOST", "localhost")
        app.config.setdefault("BERT_PORT", 5555)
        app.config.setdefault("BERT_PORT_OUT", 5556)
        app.config.setdefault("BERT_TIMEOUT", 10000)
        app.teardown_appcontext(self.teardown)

    def connect(self):
        """Create the connection to BERT."""
        return BertClient(
            ip=current_app.config["BERT_HOST"],
            port=current_app.config["BERT_PORT"],
            port_out=current_app.config["BERT_PORT_OUT"],
            timeout=current_app.config["BERT_TIMEOUT"],
        )

    def teardown(self, exception):
        """Close the connection to BERT."""
        ctx = _app_ctx_stack.top
        if hasattr(ctx, "sqlite3_db"):
            ctx.bert.close()

    @property
    def connection(self):
        """Get the connection to BERT."""
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "bert"):
                ctx.bert = self.connect()
            return ctx.bert
