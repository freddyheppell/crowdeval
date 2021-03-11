"""Utilities for pushing to ElasticSearch."""

from crowdeval.extensions import es


def add_to_index(index, model):
    """Push the model to the specified index."""
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    es.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    """Remove the specified model from the index."""
    es.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    """Run a basic similarity query."""
    search = es.search(
        index=index,
        body={
            "query": {"multi_match": {"query": query, "fields": ["*"]}},
            "from": (page - 1) * per_page,
            "size": per_page,
        },
    )
    ids = [int(hit["_id"]) for hit in search["hits"]["hits"]]
    return ids, search["hits"]["total"]["value"]
