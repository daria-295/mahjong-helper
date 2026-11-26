import pytest
from mahjong_helper.shanten import *
from mahjong_helper.tiles import Tile
from mahjong_helper.meld import Meld, MeldType

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

def test_calculate_groups_pair():
    tile_counts = [0] * 34
    tile_counts[0] = 2

    results = calculate_groups(tile_counts)

    assert (0, 0, 1) in results

def test_calculate_groups_skip_tile():
    tile_counts = [0] * 34
    tile_counts[0] = 1

    results = calculate_groups(tile_counts)

    assert (0, 0, 0) in results

def test_calculate_groups_adjacent_taatsu():
    tile_counts = [0] * 34
    tile_counts[1] = 1
    tile_counts[2] = 1

    results = calculate_groups(tile_counts)

    assert (0, 1, 0) in results

def test_calculate_groups_gapped_taatsu():
    tile_counts = [0] * 34
    tile_counts[1] = 1
    tile_counts[3] = 1

    results = calculate_groups(tile_counts)

    assert (0, 1, 0) in results

def test_calculate_groups_taatsu_does_not_cross_suits():
    tile_counts = [0] * 34
    tile_counts[7] = 1  # 8m
    tile_counts[9] = 1  # 1p

    results = calculate_groups(tile_counts)

    assert (0, 1, 0) not in results

def test_calculate_shanten_complete_hand():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M2, Tile.M3,
        Tile.P1, Tile.P2, Tile.P3,
        Tile.S1, Tile.S2, Tile.S3,
        Tile.S7, Tile.S8, Tile.S9,
        Tile.EAST, Tile.EAST
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert calculate_shanten(hand) == -1

def test_calculate_shanten_tenpai():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M2, Tile.M3,
        Tile.P1, Tile.P2, Tile.P3,
        Tile.S1, Tile.S2, Tile.S3,
        Tile.S7, Tile.S8,
        Tile.EAST, Tile.EAST
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert calculate_shanten(hand) == 0

def test_calculate_shanten_one_away():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M2, Tile.M3,
        Tile.P1, Tile.P2, Tile.P3,
        Tile.S1, Tile.S2, Tile.S3,
        Tile.EAST, Tile.EAST,
        Tile.M4, Tile.P9
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert calculate_shanten(hand) == 1

def test_calculate_shanten_multiple_pairs():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M1,
        Tile.M2, Tile.M2,
        Tile.P1, Tile.P2, Tile.P3,
        Tile.S1, Tile.S2, Tile.S3,
        Tile.EAST, Tile.EAST,
        Tile.RED
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert calculate_shanten(hand) == 1

def test_calculate_shanten_four_pairs():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M1,
        Tile.M3, Tile.M3,
        Tile.P5, Tile.P5,
        Tile.S7, Tile.S7,
        Tile.EAST, Tile.SOUTH,
        Tile.WEST, Tile.NORTH,
        Tile.RED
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert calculate_shanten(hand) == 4

def test_is_complete_standard_hand():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M2, Tile.M3,
        Tile.P1, Tile.P2, Tile.P3,
        Tile.S1, Tile.S2, Tile.S3,
        Tile.S7, Tile.S8, Tile.S9,
        Tile.EAST, Tile.EAST
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert is_complete_standard_hand(hand) is True

def test_is_not_complete_standard_hand():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M2, Tile.M3,
        Tile.P1, Tile.P2, Tile.P3,
        Tile.S1, Tile.S2, Tile.S3,
        Tile.S7, Tile.S8,
        Tile.EAST, Tile.EAST, Tile.RED
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert is_complete_standard_hand(hand) is False

def test_complete_standard_hand_with_existing_meld():
    hand = Hand()

    meld = Meld(
        [Tile.M1, Tile.M2, Tile.M3],
        MeldType.CHI
    )
    hand.add_meld(meld)

    tiles = [
        Tile.P1, Tile.P2, Tile.P3,
        Tile.S1, Tile.S2, Tile.S3,
        Tile.S7, Tile.S8, Tile.S9,
        Tile.EAST, Tile.EAST
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert is_complete_standard_hand(hand) is True

def test_standard_hand_rejects_wrong_tile_count():
    hand = Hand()

    hand.add_tile(Tile.M1)

    with pytest.raises(ValueError):
        is_complete_standard_hand(hand)

def test_is_chiitoitsu():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M1,
        Tile.M3, Tile.M3,
        Tile.P2, Tile.P2,
        Tile.P5, Tile.P5,
        Tile.S4, Tile.S4,
        Tile.S7, Tile.S7,
        Tile.EAST, Tile.EAST
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert is_chiitoitsu(hand) is True

def test_is_not_chiitoitsu():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M1,
        Tile.M3, Tile.M3,
        Tile.P2, Tile.P2,
        Tile.P5, Tile.P5,
        Tile.S4, Tile.S4,
        Tile.S7, Tile.S8,
        Tile.EAST, Tile.EAST
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert is_chiitoitsu(hand) is False

def test_chiitoitsu_rejects_open_hand():
    hand = Hand()

    meld = Meld(
        [Tile.M1, Tile.M2, Tile.M3],
        MeldType.CHI
    )
    hand.add_meld(meld)

    assert is_chiitoitsu(hand) is False

def test_chiitoitsu_rejects_four_of_a_kind():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M1, Tile.M1, Tile.M1,
        Tile.M3, Tile.M3,
        Tile.P2, Tile.P2,
        Tile.P5, Tile.P5,
        Tile.S4, Tile.S4,
        Tile.EAST, Tile.EAST
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert is_chiitoitsu(hand) is False

def test_is_kokushi():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M9,
        Tile.P1, Tile.P9,
        Tile.S1, Tile.S9,
        Tile.EAST, Tile.SOUTH, Tile.WEST, Tile.NORTH,
        Tile.WHITE, Tile.GREEN, Tile.RED,
        Tile.M1
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert is_kokushi(hand) is True

def test_is_not_kokushi_missing_orphan():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M9,
        Tile.P1, Tile.P9,
        Tile.S1, Tile.S9,
        Tile.EAST, Tile.SOUTH, Tile.WEST, Tile.NORTH,
        Tile.WHITE, Tile.GREEN,
        Tile.M1, Tile.M1
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert is_kokushi(hand) is False

def test_is_not_kokushi_with_non_orphan():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M9,
        Tile.P1, Tile.P9,
        Tile.S1, Tile.S9,
        Tile.EAST, Tile.SOUTH, Tile.WEST, Tile.NORTH,
        Tile.WHITE, Tile.GREEN, Tile.RED,
        Tile.M2
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert is_kokushi(hand) is False

def test_kokushi_rejects_meld():
    hand = Hand()
    meld = Meld([Tile.M1, Tile.M2, Tile.M3], MeldType.CHI)
    hand.add_meld(meld)

    assert is_kokushi(hand) is False

def test_is_complete_hand_standard():
    hand = Hand()
    tiles = [
        Tile.M1, Tile.M2, Tile.M3,
        Tile.M4, Tile.M5, Tile.M6,
        Tile.P1, Tile.P2, Tile.P3,
        Tile.S1, Tile.S2, Tile.S3,
        Tile.EAST, Tile.EAST
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert is_complete_hand(hand) is True

def test_is_complete_hand_chiitoitsu():
    hand = Hand()
    tiles = [
        Tile.M1, Tile.M1, Tile.M3, Tile.M3,
        Tile.P2, Tile.P2, Tile.P5, Tile.P5,
        Tile.S4, Tile.S4, Tile.S7, Tile.S7,
        Tile.EAST, Tile.EAST
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert is_complete_hand(hand) is True

def test_is_complete_hand_kokushi():
    hand = Hand()
    tiles = KOKUSHI_TILES + [Tile.M1]

    for tile in tiles:
        hand.add_tile(tile)

    assert is_complete_hand(hand) is True

def test_find_hand_decompositions():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M2, Tile.M3,
        Tile.M4, Tile.M5, Tile.M6,
        Tile.P1, Tile.P2, Tile.P3,
        Tile.S1, Tile.S2, Tile.S3,
        Tile.EAST, Tile.EAST
    ]

    for tile in tiles:
        hand.add_tile(tile)

    decompositions = find_hand_decompositions(hand)
    assert len(decompositions) >= 1
    decomposition = decompositions[0]
    assert len(decomposition["sequences"]) == 4
    assert len(decomposition["triplets"]) == 0
    assert decomposition["pair"] is not None
    