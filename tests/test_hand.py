import pytest

from mahjong_helper.hand import Hand
from mahjong_helper.tiles import Tile
from mahjong_helper.meld import Meld, MeldType

def test_add_tile():
    hand = Hand()

    hand.add_tile(Tile.M1)

    assert hand.get_count_of_a_tile(Tile.M1) == 1
    assert hand.get_total_tiles() == 1

def test_add_multiple_tiles():
    hand = Hand()

    hand.add_tile(Tile.M1)
    hand.add_tile(Tile.M2)
    hand.add_tile(Tile.M3)
    hand.add_tile(Tile.M3)

    assert hand.get_count_of_a_tile(Tile.M3) == 2
    assert hand.get_total_tiles() == 4

def test_remove_tile():
    hand = Hand()

    hand.add_tile(Tile.WHITE)
    hand.add_tile(Tile.WHITE)

    hand.remove_tile(Tile.WHITE)

    assert hand.get_count_of_a_tile(Tile.WHITE) == 1

def test_cannot_add_more_than_four_copies():
    hand = Hand()

    for _ in range(4):
        hand.add_tile(Tile.M1)

    with pytest.raises(ValueError):
        hand.add_tile(Tile.M1)

def test_cannot_remove_tile_not_in_hand():
    hand = Hand()

    with pytest.raises(ValueError):
        hand.remove_tile(Tile.M1)

def test_add_red_five():
    hand = Hand()

    hand.add_tile(Tile.M5)
    hand.add_tile(Tile.M5, is_red=True)
    hand.add_tile(Tile.M5)

    assert hand.get_count_of_a_tile(Tile.M5) == 3
    assert hand.red_fives[Tile.M5] == 1

def test_remove_red_five():
    hand = Hand()

    hand.add_tile(Tile.M5)
    hand.add_tile(Tile.M5, is_red=True)

    hand.remove_tile(Tile.M5, is_red=True)

    assert hand.get_count_of_a_tile(Tile.M5) == 1
    assert hand.red_fives[Tile.M5] == 0

def test_cannot_add_red_five_of_honour_tile():
    hand = Hand()

    with pytest.raises(ValueError):
        hand.add_tile(Tile.EAST, is_red=True)

def test_cannot_add_two_red_fives_of_same_suit():
    hand = Hand()

    hand.add_tile(Tile.M5, is_red=True)

    with pytest.raises(ValueError):
        hand.add_tile(Tile.M5, is_red=True)

def test_cannot_remove_red_five_that_is_not_in_hand():
    hand = Hand()

    hand.add_tile(Tile.M5)

    with pytest.raises(ValueError):
        hand.remove_tile(Tile.M5, is_red=True)

def test_clear_hand():
    hand = Hand()

    hand.add_tile(Tile.M5, is_red=True)
    hand.add_tile(Tile.EAST)

    hand.clear_hand()

    assert hand.get_total_tiles() == 0
    assert hand.red_fives[Tile.M5] == 0
    assert hand.melds == []

def test_get_hand_returns_copy():
    hand = Hand()

    hand.add_tile(Tile.M1)

    copied_hand = hand.get_hand()
    copied_hand[Tile.M1.value] = 0

    assert hand.get_count_of_a_tile(Tile.M1) == 1

def test_valid_drawn_hand_size():
    hand = Hand()

    for _ in range(4):
        hand.add_tile(Tile.M1)

    for _ in range(4):
        hand.add_tile(Tile.M2)

    for _ in range(4):
        hand.add_tile(Tile.M3)

    for _ in range(2):
        hand.add_tile(Tile.EAST)

    hand.validate_hand_size(is_drawn=True)

def test_invalid_hand_size():
    hand = Hand()
    hand.add_tile(Tile.M1)

    with pytest.raises(ValueError):
        hand.validate_hand_size()

def test_valid_hand_size():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M2, Tile.M3,
        Tile.P1, Tile.P2, Tile.P3,
        Tile.S1, Tile.S2, Tile.S3,
        Tile.S7, Tile.S8, Tile.S9,
        Tile.EAST
    ]

    for tile in tiles:
        hand.add_tile(tile)

    hand.validate_hand_size()

def test_hand_size_with_existing_meld():
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
        Tile.EAST
    ]

    for tile in tiles:
        hand.add_tile(tile)

    hand.validate_hand_size()

def test_drawn_hand_size_with_existing_meld():
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

    hand.validate_hand_size(is_drawn=True)
