"""Automatically create and start the app."""
from crowdeval.app import create_app
from werkzeug.middleware.proxy_fix import ProxyFix

# The use of ProxyFix ensure that the URLs are generated correctly
# when we use OAuth to login via Twitter from behind a proxy.
# Note I'm not sure what happens if you use this and aren't behind
# a proxy....
app = ProxyFix(create_app(), x_for=1, x_host=1)
