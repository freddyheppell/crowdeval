import json


def load_fixture(family, fixture):
    with open("tests/fixtures/" + family + "/" + fixture) as fixture:
        fixture_data = fixture.read()
        if family == "tweets":
            return FakeTweetResponse(fixture_data)
        return fixture_data


class FakeTweetResponse:
    def __init__(self, fake_json):
        self.data = json.loads(fake_json)

    def get_iterator(self):
        return [self.data]
