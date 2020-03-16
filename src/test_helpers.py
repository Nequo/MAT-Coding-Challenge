import pytest
from helpers import *

@pytest.mark.parametrize(
    "sectors, laps, expected_order",
    [
        ([100, 90, 110, 130, 104, 96], [0, 0, 0, 0, 0, 0], [3, 2, 4, 0, 5, 1]),
        ([2, 90, 110, 130, 104, 96], [1, 0, 0, 0, 0, 0], [0, 3, 2, 4, 5, 1]),
        ([104, 90, 104, 130, 104, 96], [0, 0, 0, 0, 0, 0], [3, 4, 2, 0, 5, 1])
    ])
def test_car_positions_same_lap(sectors, laps, expected_order):
    assert car_positions(sectors, laps) == expected_order
