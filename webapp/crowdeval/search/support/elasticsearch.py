"""Utilities for pushing to ElasticSearch."""


from crowdeval.extensions import bert, es


def add_to_index(index, model):
    """Push the model to the specified index."""
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)

    if hasattr(model, "__bertify__"):
        for field in model.__bertify__:
            vectorised = bert.connection.encode([getattr(model, field)])[0]
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
    scores = dict(zip(ids, {int(hit["_score"]) for hit in search["hits"]["hits"]}))
    return ids, search["hits"]["total"]["value"], scores


def bert_search_by_term(index, field, query, page, per_page, min_score):
    """Search with a textual query using BERT."""
    query_vector = bert.connection.encode([query])[0]

    return bert_search_by_vector(index, field, query_vector, page, per_page, min_score)


def bert_search_by_vector(index, field, query_vector, page, per_page, min_score):
    """Search with a pre-obtained vector using BERT."""
    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": f"cosineSimilarity(params.query_vector, '{field}') + 1.0",
                "params": {"query_vector": query_vector},
            },
            "min_score": min_score,
        }
    }

    search = es.search(
        index=index,
        body={
            "size": per_page,
            "from": (page - 1) * per_page,
            "query": script_query,
            "_source": {"includes": ["text"]},
        },
    )

    ids = [int(hit["_id"]) for hit in search["hits"]["hits"]]

    scores = dict(zip(ids, [hit["_score"] for hit in search["hits"]["hits"]]))

    return ids, search["hits"]["total"]["value"], scores
