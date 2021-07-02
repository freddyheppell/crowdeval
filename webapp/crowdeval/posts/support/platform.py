"""Shared behaviour for all platforms."""

from enum import Enum


class Platform(Enum):
    """Represents the post types in the db."""

    TWITTER = 1
    DUMMY = 2
