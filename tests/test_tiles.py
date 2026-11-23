from mahjong_helper.tiles import *

def test_to_string():
    assert to_string(Tile.M1) == "1m"
    assert to_string(Tile.P5) == "5p"
    assert to_string(Tile.EAST) == "E"
    assert to_string(Tile.WHITE) == "Wh"

def test_is_suit():
    assert is_suit(Tile.S5)
    assert is_suit(Tile.M1)
    assert not is_suit(Tile.EAST)

def test_is_honour():
    assert is_honour(Tile.RED)
    assert is_honour(Tile.EAST)
    assert not is_honour(Tile.S5)

def test_is_red():
    assert is_red(Tile.P5)
    assert is_red(Tile.M5)
    assert not is_red(Tile.M4)

def test_get_suit():
    assert get_suit(Tile.P5) == "pinzu"
    assert get_suit(Tile.M1) == "manzu"
    assert get_suit(Tile.S9) == "souzu"
    assert get_suit(Tile.EAST) is None

def test_get_rank():
    assert get_rank(Tile.P5) == 5
    assert get_rank(Tile.M1) == 1
    assert get_rank(Tile.S9) == 9
    assert get_rank(Tile.EAST) is None
