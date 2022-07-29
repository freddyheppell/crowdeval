"""Utilities for pushing to ElasticSearch."""


from jina import Document

from crowdeval.extensions import bert, es


def _doc_to_embedding(text):
    document = Document(content=text)
    resp = bert.client.post("/encode", document)
    return resp[0].embedding


def add_to_index(index, model):
    """Push the model to the specified index."""
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)

    if hasattr(model, "__bertify__"):
        for field in model.__bertify__:
            payload[field + "_vector"] = _doc_to_embedding(getattr(model, field))

    es.index(index=index, id=model.id, document=payload)


def remove_from_index(index, model):
    """Remove the specified model from the index."""
    es.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    """Run a basic similarity query."""
    search = es.search(
        index=index,
        query={"multi_match": {"query": query, "fields": ["*"]}},
        from_=(page - 1) * per_page,
        size=per_page,
    )
    ids = [int(hit["_id"]) for hit in search["hits"]["hits"]]
    scores = dict(zip(ids, {int(hit["_score"]) for hit in search["hits"]["hits"]}))
    return ids, search["hits"]["total"]["value"], scores


def bert_search_by_term(index, field, query, page, per_page, min_score):
    """Search with a textual query using BERT."""
    query_vector = _doc_to_embedding(query)

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
        query=script_query,
        from_=(page - 1) * per_page,
        size=per_page,
        _source={"includes": ["text"]},
    )

    ids = [int(hit["_id"]) for hit in search["hits"]["hits"]]

    scores = dict(zip(ids, [hit["_score"] for hit in search["hits"]["hits"]]))

    return ids, search["hits"]["total"]["value"], scores
