import json
import pickle

pickles = ["bert"]


def load_fixture(family, fixture):
    path = "tests/fixtures/" + family + "/" + fixture

    if family in pickles:
        with open(path, "rb") as file:
            return _pickle_serialise(file)

    if family == "tweets":
        with open(path, "r", encoding="utf8") as file:
            return FakeTweetResponse(file)

    with open(path, "r") as file:
        fixture_data = file.read()
        return json.loads(fixture_data)


class FakeTweetResponse:
    def __init__(self, fixture):
        self.data = json.load(fixture)

    def get_iterator(self):
        return [self.data]


def _pickle_serialise(fixture):
    return pickle.load(fixture)
