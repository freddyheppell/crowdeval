#!/bin/sh

# Wait until elasticsearch is up and running before trying to do anything else
# and because elasticsearch takes a while by the time this completes MySQL will
# also be up and running so we can safely init the db as well as the index
# https://gist.github.com/rochacbruno/bdcad83367593fd52005#gistcomment-3468326
timeout 300 bash -c "until curl --silent --output /dev/null http://elasticsearch:9200/_cat/health?h=st; do printf '.'; sleep 5; done; printf '\n'"

# Make sure the MySQL db exists and is the latest version
# This completes cleanly even if there are no changes
venv/bin/flask db upgrade

# Make sure the elasticsearch index exists and has the right mappings in place
# Note that this does put an error in the logs if the index already exists
# but this is safe to ignore.
venv/bin/flask create-index -i posts -c infrastructure/elasticsearch/posts.json

# Now we start the flask app using gunicorn.
exec /sbin/tini --  venv/bin/gunicorn autoapp:app -w $WORKERS --threads $THREADS -b 0.0.0.0:8000
