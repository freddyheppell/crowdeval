"""Application configuration.

This file should load the values from the .env file and
they will be set as flask config variables
"""
from environs import Env

env = Env()
env.read_env()

# Basic flask settings
ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SECRET_KEY = env.str("SECRET_KEY")

# SQlAlchemy
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}:{port}/{database}?charset=utf8mb4".format(
    username=env.str("DB_USER"),
    password=env.str("DB_PASSWORD"),
    hostname=env.str("DB_HOSTNAME"),
    port=env.str("DB_PORT"),
    database=env.str("DB_DATABASE"),
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Twitter Auth
TWITTER_OAUTH_CLIENT_KEY = env.str("TWITTER_OAUTH_CLIENT_KEY")
TWITTER_OAUTH_CLIENT_SECRET = env.str("TWITTER_OAUTH_CLIENT_SECRET")
TWITTER_ACCESS_TOKEN = env.str("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = env.str("TWITTER_ACCESS_TOKEN_SECRET")

# Debugbar
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Flask-WTF
RECAPTCHA_PUBLIC_KEY = env.str("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env.str("RECAPTCHA_PRIVATE_KEY")

ELASTICSEARCH_HOST = env.str("ELASTICSEARCH_HOST")

BERT_HOST = env.str("BERT_HOST")
BERT_PORT = env.int("BERT_PORT")
BERT_PORT_OUT = env.int("BERT_PORT_OUT")
BERT_TIMEOUT = env.int("BERT_TIMEOUT")

# Caching
CACHE_TYPE = env.str("CACHE_TYPE")
CACHE_REDIS_HOST = env.str("CACHE_REDIS_HOST")
CACHE_REDIS_PORT = env.int("CACHE_REDIS_PORT")
CACHE_DEFAULT_TIMEOUT = 3600