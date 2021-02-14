"""Application configuration.

This file should load the values from the .env file and
they will be set as flask config variables
"""
from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SECRET_KEY = env.str("SECRET_KEY")

TWITTER_OAUTH_CLIENT_KEY = env.str("TWITTER_OAUTH_CLIENT_KEY")
TWITTER_OAUTH_CLIENT_SECRET = env.str("TWITTER_OAUTH_CLIENT_SECRET")

print("------", env.str("SQLALCHEMY_DATABASE_URI"))
SQLALCHEMY_DATABASE_URI = env.str("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False
