# -*- coding: utf-8 -*-
"""Click commands."""
import json
import os
import time
import traceback
from glob import glob
from itertools import zip_longest
from subprocess import call

import click
from flask.cli import with_appcontext

from crowdeval.extensions import db, es
from crowdeval.posts.models import Post
from crowdeval.posts.support.twitter_post import TwitterPost

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = "tests/"


@click.command()
@click.option(
    "-x",
    "--exit-on-fail",
    default=False,
    is_flag=True,
    help="End testing at first failure",
)
def test(exit_on_fail):
    """Run the tests."""
    rv = call(["pytest", TEST_PATH, "--verbose", "-x" if exit_on_fail else ""])
    exit(rv)


@click.command()
@click.option(
    "-f",
    "--fix-imports",
    default=True,
    is_flag=True,
    help="Fix imports using isort, before linting",
)
@click.option(
    "-c",
    "--check",
    default=False,
    is_flag=True,
    help="Don't make any changes to files, just confirm they are formatted\
    correctly",
)
def lint(fix_imports, check):
    """Lint and check code style with black, flake8 and isort."""
    skip = ["node_modules", "requirements", "migrations"]
    root_files = glob("*.py")
    root_directories = [
        name for name in next(os.walk("."))[1] if not name.startswith(".")
    ]
    files_and_directories = [
        arg for arg in root_files + root_directories if arg not in skip
    ]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        click.echo(f"{description}: {' '.join(command_line)}")
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    isort_args = []
    black_args = []
    if check:
        isort_args.append("--check")
        black_args.append("--check")
    if fix_imports:
        execute_tool("Fixing import order", "isort", *isort_args)
    execute_tool("Formatting style", "black", *black_args)
    execute_tool("Checking code style", "flake8")


@click.command()
@click.option("-i", "--index", help="The ES Index name")
@click.option("-c", "--config", help="The ES Index file")
@with_appcontext
def create_index(index, config):
    """Create the elasticsearch index."""
    with open(config) as file:
        config = json.load(file)

        es.indices.create(index=index, body=config)


@click.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option(
    "-r",
    "--rate",
    default=300,
    help="The number of tweets that can be retrieved per rate limit window",
)
@click.option(
    "-d",
    "--delay",
    default=900,
    help="The number of seconds that should be left before retrieving the next batch",
)
@with_appcontext
def import_tweet_seeds(directory, rate, delay):
    """Bulk import tweets to the database."""
    ratelimit_count = 0
    succesful_imports = 0
    failed_imports = 0

    tweet_files = [
        f.path for f in os.scandir(directory) if str(f.name).endswith(".json")
    ]

    tweet_ids = set()

    for tweet_file in tweet_files:
        with open(tweet_file, "r") as file:
            jsoned_tweets = json.load(file)

            for tweet in jsoned_tweets:
                tweet_ids.add(tweet["id_str"])

    def grouper(n, iterable, padvalue=None):
        """Chunk the iterable into groups of n."""
        return list(zip_longest(*[iter(iterable)] * n, fillvalue=padvalue))

    grouped_tweets = grouper(rate, tweet_ids)

    print(
        "There are",
        len(tweet_ids),
        "tweets to import. This will take approximately",
        len(grouped_tweets * delay),
        "seconds to import. Continue?",
    )

    input()

    for group in grouped_tweets:
        for tweet_id in group:
            # If the tweets can't be equally split, the chunk will be padded with Nones
            if tweet_id is None:
                continue

            try:
                # nb fails for some tweet names eg with id 500375839498723328
                ratelimit_count += 1
                tweet_obj = TwitterPost(tweet_id)
                tweet_data = tweet_obj.get_data()
                post = Post(**tweet_data)
                db.session.add(post)
                db.session.commit()
                succesful_imports += 1
            except Exception:  # noqa: B902
                db.session.rollback()
                print("Error importing", tweet_id)
                traceback.print_exc()
                failed_imports += 1

        print(
            "Batch imported, waiting for",
            delay,
            "seconds (starting at",
            time.strftime("%H:%M:%S", time.localtime()),
            ")",
        )
        time.sleep(delay)

    print("FINISHED")
    print("Imported", succesful_imports, "ok")
    print("Failed for", failed_imports)
