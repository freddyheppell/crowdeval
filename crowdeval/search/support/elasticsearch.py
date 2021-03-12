"""Utilities for pushing to ElasticSearch."""

from bert_serving.client import BertClient

from crowdeval.extensions import es


def add_to_index(index, model):
    """Push the model to the specified index."""
    bc = BertClient(output_fmt="list", check_length=False)

    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)

    if hasattr(model, "__bertify__"):
        for field in model.__bertify__:
            data = getattr(model, field)
            vectorised = bc.encode([data])[0]
            payload[field + "_vector"] = vectorised

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


def bert_search(query):
    """Search the specified query using BERT.

    TODO: make function more generic.
    """
    bc = BertClient(output_fmt="list", check_length=False)
    query_vector = bc.encode([query])[0]
    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'text_vector') + 1.0",
                "params": {"query_vector": query_vector},
            },
        }
    }

    response = es.search(
        index="posts",  # name of the index
        body={
            "size": 1,
            "query": script_query,
            "_source": {"includes": ["text"]},
        },
    )

    return response
