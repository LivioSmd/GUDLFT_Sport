import copy
from .fixtures import client, MockData
from server import get_place_required


def test_get_place_required(client):
    """Test that the get_place_required function returns the required places."""
    place_required = get_place_required(10)

    assert place_required is not None
    assert place_required == 10
    assert isinstance(place_required, int)  # place_required should be an integer


def test_not_get_place_required(client):
    """Test that the get_place_required function returns 0 in case of invalid data."""
    place_required = get_place_required(copy.deepcopy(MockData.invalid_place_required))

    assert place_required is not None
    assert place_required == 0
    assert isinstance(place_required, int)  # place_required should be an integer
