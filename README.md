# CrowdEval

## Installing Poetry Dependencies

On macOS Big Sur, the environment variable `SYSTEM_VERSION_COMPAT` must be set to `1`, otherwise Numpy won't install properly.

## Setup Elasticsearch

Ensuring the Elasticsearch Docker service is running, run

```bash
$ flask create-index -i posts -c infrastructure/elasticsearch/posts.json
```

## Running

To start asset compilation and the flask dev server, run

```shell
$ npm run start
```

Flask will start on `localhost:5000`