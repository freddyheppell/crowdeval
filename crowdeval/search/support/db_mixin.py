"""Integration between elasticsearch and sqlalchemy."""

from crowdeval.extensions import db
from crowdeval.search.support.elasticsearch import (
    add_to_index,
    bert_search_by_term,
    query_index,
    remove_from_index,
)


class SearchableMixin(object):
    """A mixin to add event-based elasticsearch behaviour."""

    @classmethod
    def _process_search(cls, ids, total):
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return (
            cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)),
            total,
        )

    @classmethod
    def search(cls, expression, page, per_page):
        """Search the model."""
        ids, total, scores = query_index(cls.__tablename__, expression, page, per_page)

        return *cls._process_search(ids, total), scores

    @classmethod
    def bert_search(cls, expression, field, page, per_page):
        """Search the model with BERT."""
        if not hasattr(cls, "__bertify__") or field not in cls.__bertify__:
            raise Exception(f"Trying to search non-bertified field {field}")

        ids, total, scores = bert_search_by_term(
            cls.__tablename__, f"{field}_vector", expression, page, per_page
        )

        return *cls._process_search(ids, total), scores

    @classmethod
    def before_commit(cls, session):
        """Event hook which captures and stores changes in the session."""
        session._changes = {
            "add": list(session.new),
            "update": list(session.dirty),
            "delete": list(session.deleted),
        }

    @classmethod
    def after_commit(cls, session):
        """Event hook which pushes session changes to elasticsearch."""
        for obj in session._changes["add"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["update"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["delete"]:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        """Reindex all models in this query."""
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, "before_commit", SearchableMixin.before_commit)
db.event.listen(db.session, "after_commit", SearchableMixin.after_commit)
