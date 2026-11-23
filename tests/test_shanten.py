from mahjong_helper.shanten import *


def test_find_first_tile():
    tile_counts = [0, 0, 2, 1, 0]

    assert find_first_tile(tile_counts) == 2

def test_find_first_tile_empty():
    tile_counts = [0] * 34

    assert find_first_tile(tile_counts) is None

def test_calculate_groups_triplet():
    tile_counts = [0] * 34
    tile_counts[0] = 3  # 3 copies of M1
    results = calculate_groups(tile_counts)

    assert (1, 0, 0) in results


def test_calculate_groups_sequence():
    tile_counts = [0] * 34
    tile_counts[0] = 1
    tile_counts[1] = 1
    tile_counts[2] = 1
    results = calculate_groups(tile_counts)

    assert (1, 0, 0) in results
