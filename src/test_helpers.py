import pytest
from helpers import *
from scipy import spatial
import csv

def test_closest_sector():
    track_points = list(csv.reader(open("./track.csv"), quoting=csv.QUOTE_NONNUMERIC))
    track_tree = spatial.KDTree(track_points)
    assert closest_sector(track_tree, track_points[0][0], track_points[0][1]) == 0
    assert closest_sector(track_tree, track_points[454][0], track_points[454][1]) == 454
    

@pytest.mark.parametrize(
    "sectors, laps, expected_order",
    [
        ([100, 90, 110, 130, 104, 96], [0, 0, 0, 0, 0, 0], [3, 2, 4, 0, 5, 1]),
        ([2, 90, 110, 130, 104, 96], [1, 0, 0, 0, 0, 0], [0, 3, 2, 4, 5, 1]),
        ([104, 90, 104, 130, 104, 96], [0, 0, 0, 0, 0, 0], [3, 4, 2, 0, 5, 1])
    ])
def test_car_positions(sectors, laps, expected_order):
    assert car_positions(sectors, laps) == expected_order


def test_ms_to_time():
    minutes, seconds, milliseconds = ms_to_time(60000)
    assert minutes == 1
    assert seconds == 0
    assert milliseconds == 0
    minutes, seconds, milliseconds = ms_to_time(78300)
    assert minutes == 1
    assert seconds == 18
    assert milliseconds == 300
