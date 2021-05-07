# CrowdEval

CrowdEval is an experimental crowdsourced factchecking application, created as part of my MComp Computer Science dissertation project.

## Installation

**Requirements**
* Docker
* Python 3.9.4
* [Poetry](https://python-poetry.org/)

### Install Poetry Dependencies
> On macOS Big Sur, set the environment variable `SYSTEM_VERSION_COMPAT` to `1`, otherwise Numpy may not install properly.

1. Ensure Poetry is installed
2. Run `poetry install`
3. To activate the virtual environment, run `poetry shell`, or run commands inside the environment individually with `poetry run <command>`
    * Any `flask` commands must be run inside this environment.

### Setup Environment
1. `cp .env.example .env`
2. Enter a `SECRET_KEY`, which should be a long random string
2. Enter the `TWITTER_` API keys. This has to be a [new-style Twitter project](https://developer.twitter.com/en/docs/projects/overview) because we use v2.0 of the Twitter API 
3. Enter the `RECAPTCHA_` API keys
4. The remainder of the file is already configured for the docker development environment and shouldn't need to be changed

### Start Docker Infrastructure

> This will download a ~400MB file as part of building the BERT-as-a-service container

The database, search, cache and BERT embedding services are dockerised. Run `docker-compose up` to start.

### Setup Elasticsearch

Once the Elasticsearch service has started, run:

```bash
$ flask create-index -i posts -c infrastructure/elasticsearch/posts.json
```

This tells Elasticsearch to store the BERT embeddings as a dense vector rather than an array.

### Install frontend

Install the frontend pipeline with

```shell
$ npm install
```


## Running

If it's not already running, start the docker environment with

```shell
$ docker-compose up
```

To start asset compilation and the flask dev server, run

```shell
$ npm run start
```

Flask will start on `localhost:5000`

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

In production this would ideally be run as a scheduled task.

### Quality Control

Tests and linting can be run with

```shell
$ flask test
$ flask lint
```