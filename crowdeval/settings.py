"""Application configuration.

This file should load the values from the .env file and
they will be set as flask config variables
"""
from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
