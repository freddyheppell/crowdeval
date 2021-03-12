# -*- coding: utf-8 -*-
"""Click commands."""
import os
from glob import glob
from json import load
from subprocess import call

import click
from flask.cli import with_appcontext

from crowdeval.extensions import es

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = "tests/"


@click.command()
@click.option(
    '-x',
    '--exit-on-fail',
    default=False,
    is_flag=True,
    help="End testing at first failure"
)
def test(exit_on_fail):
    """Run the tests."""
    rv = call(["pytest", TEST_PATH, "--verbose", "-x" if exit_on_fail else ''])
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
        config = load(file)

        es.indices.create(index=index, body=config)
