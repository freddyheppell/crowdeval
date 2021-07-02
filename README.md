# CrowdEval

CrowdEval is an experimental crowdsourced factchecking application, created as part of my MComp Computer Science dissertation project. The idea for this project was provided by the project supervisor, [Carolina Scarton](https://carolscarton.github.io/).

[![Test & Lint](https://github.com/freddyheppell/crowdeval/actions/workflows/test.yml/badge.svg)](https://github.com/freddyheppell/crowdeval/actions/workflows/test.yml) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?logo=python&logoColor=white)](https://github.com/psf/black) [![js-standard-style](https://img.shields.io/badge/code%20style-standard-f3df49.svg?logo=javascript&logoColor=white)](http://standardjs.com)

CrowdEval ships with two Docker environments:

* a development environment with containerised infrastructure, but the app and frontend run natively
* a fully containerised production environment


## Installation of Development Environment

Dependencies:
* Python 3.9.4
* [Poetry](https://python-poetry.org/)

1. `cd` into the `webapp` directory
2. Run `poetry install`
    * On macOS Big Sur, if Numpy fails to install, ensure  the environment variable `SYSTEM_VERSION_COMPAT` is set to `1` and try again
3. `cp .env.dev .env`
    * Enter a `SECRET_KEY`, which can be any string
    * Enter the `TWITTER_` API keys. This has to be a [new-style Twitter project](https://developer.twitter.com/en/docs/projects/overview) because we use v2.0 of the Twitter API 
        * The callback URL for development should be `localhost:5000/login/twitter/authorized`
    * Enter the `RECAPTCHA_` API keys
    * The remainder of the file is already configured for the development environment and shouldn't need to be changed
4. Run `docker-compose up` to start
    * This will download a ~400MB file as part of building the BERT-as-a-Service container
5. Once the Elasticsearch service has started, run:
    ```
    $ poetry run flask create-index -i posts -c infrastructure/elasticsearch/posts.json
    ```
    This will create the required posts index.
6. Install frontend dependencies with `npm install`
7. To start asset compilation and the Flask dev server, run
    ```
    $ npm run start
    ```
    **The app will be started on `localhost:5000`**
8. Migrate the database with `poetry run flask db upgrade`

## Deploying to production

Working from the root directory:

1. `cp webapp/.env.prod webapp/.env`
    * Enter a `SECRET_KEY`, which should be a random ~32-character secret
    * Enter the `TWITTER_` API keys. This has to be a [new-style Twitter project](https://developer.twitter.com/en/docs/projects/overview) because we use v2.0 of the Twitter API 
        * The callback URL should be `<your hostname>/login/twitter/authorized`
    * Enter the `RECAPTCHA_` API keys
    * The remainder of the file is already configured for the development environment and shouldn't need to be changed
2. `docker-compose up`

The application should now be built and started via Gunicorn.


## Administrative commands

> In development, these commands should be prefixed with `poetry run` (or run `poetry shell` once to activate and run as is).
> 
> In production, attach to the `crowdeval` service and run as is, i.e.:
> ```shell
> docker-compose run --entrypoint "bash -l" crowdeval
> ```

### Seeding with dummy data

The system can import the Kochkina et al.'s PHEME dataset, which has been pre-processed and stored in [/seeds/kochkina_et_al_PHEME](/seeds/kochkina_et_al_PHEME). To import it:

```shell
$ flask import-tweet-seeds seeds/kochkina_et_al_PHEME
```

This will create a `.veracities.json` file, which can then be used to seed random (but biased towards the dataset's veracity) ratings with

```shell
$ flask seed-ratings
```

### Regenerating explore cache

The explore by rating pages are served from Redis, and must be manually regenerated.

```shell
$ flask recache-explore
```

In production this is probably best run as a scheduled task on the host machine via cron with an entry such as (note the
hard coded path to the docker-compose.yml file):

```
*/5 * * * * /usr/local/bin/docker-compose -f /data/crowdeval/docker-compose.yml run --entrypoint "venv/bin/flask recache-explore" crowdeval >> crowdeval-cron.log 2>&1
```

### Quality Control

Tests and linting can be run with

```shell
$ flask test
$ flask lint
```