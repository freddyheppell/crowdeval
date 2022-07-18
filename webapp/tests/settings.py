"""Settings module for test app."""
from environs import Env

env = Env()
env.read_env()

ENV = "development"
TESTING = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}:{port}/{database}?charset=utf8mb4".format(
    username="crowdeval",
    password="crowdeval",
    hostname="localhost",
    port=env.str("TEST_DB_PORT", "3308"),
    database="crowdeval-test",
)
SECRET_KEY = "not-so-secret-in-tests"
BCRYPT_LOG_ROUNDS = (
    4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
)
DEBUG_TB_ENABLED = False
CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False  # Allows form testing
RECAPTCHA_PUBLIC_KEY = "public"
RECAPTCHA_PRIVATE_KEY = "secret"
PRESERVE_CONTEXT_ON_EXCEPTION = False
TWITTER_OAUTH_CLIENT_KEY = "key"
TWITTER_OAUTH_CLIENT_SECRET = "secret"
TWITTER_ACCESS_TOKEN = "token"
TWITTER_ACCESS_TOKEN_SECRET = "secret"
ELASTICSEARCH_HOST = "http://elasticsearch:9200"
JINA_URL = "grpc://dummy"
CACHE_TYPE = "SimpleCache"
