"""Functionality to store and retrieve posts from Twitter."""

import json

from flask.globals import current_app
from TwitterAPI import TwitterAPI

from crowdeval.posts.support.platform import Platform

EXPANSIONS = "author_id,referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id,attachments.media_keys,attachments.poll_ids,geo.place_id,entities.mentions.username"
MEDIA_FIELDS = (
    "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics"
)
TWEET_FIELDS = "created_at,author_id,public_metrics"
USER_FIELDS = "location,profile_image_url,verified"


class TwitterPost:
    """Represents an external post on Twitter."""

    def __init__(self, status_id):
        """Create a new post."""
        self.status_id = status_id

    def get_platform(self):
        """Get the enum representation of this platform."""
        return Platform.TWITTER

    def get_external_id(self):
        """Get the retrieved status id."""
        return self.status_id

    def get_data(self):
        """Retrieve this post's representation from the API."""
        tweet = self._retrieve_tweet()

        return {
            "platform": self.get_platform().value,
            "external_post_id": tweet["id"],
            "text": tweet["text"],
            "author_name": tweet["author_id"]["name"],
            "author_username": tweet["author_id"]["username"],
            "author_profile_url": tweet["author_id"]["profile_image_url"],
            "external_author_id": tweet["author_id"]["id"],
            "additional_metadata": json.dumps(
                {"verified": tweet["author_id"]["verified"]}
            ),
            "external_created_at": tweet["created_at"],
        }

    def _retrieve_tweet(self):
        api = self._get_api()

        tweet = api.request(
            f"tweets/:{self.status_id}",
            {
                "expansions": EXPANSIONS,
                "tweet.fields": TWEET_FIELDS,
                "user.fields": USER_FIELDS,
                "media.fields": MEDIA_FIELDS,
            },
            hydrate_tweets=True,
        )

        # Returns a list of tweets so only use first
        return list(tweet.get_iterator())[0]

    def _get_api(self):
        return TwitterAPI(
            current_app.config.get("TWITTER_OAUTH_CLIENT_KEY"),
            current_app.config.get("TWITTER_OAUTH_CLIENT_SECRET"),
            current_app.config.get("TWITTER_ACCESS_TOKEN"),
            current_app.config.get("TWITTER_ACCESS_TOKEN_SECRET"),
            api_version="2",
        )
