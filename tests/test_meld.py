import pytest
from mahjong_helper.hand import Hand
from mahjong_helper.meld import Meld, MeldType
from mahjong_helper.tiles import Tile

def test_create_chi():
    chi = Meld(
        [Tile.S3, Tile.S4, Tile.S5],
        MeldType.CHI,
        is_open=True
    )

    assert chi.meld_type == MeldType.CHI
    assert chi.is_open is True
    assert len(chi.tiles) == 3


def test_create_pon():
    pon = Meld(
        [Tile.EAST, Tile.EAST, Tile.EAST],
        MeldType.PON
    )

    assert pon.meld_type == MeldType.PON
    assert len(pon.tiles) == 3


def test_create_kan():
    kan = Meld(
        [Tile.RED, Tile.RED, Tile.RED, Tile.RED],
        MeldType.KAN,
        is_open=False
    )

    assert kan.meld_type == MeldType.KAN
    assert len(kan.tiles) == 4
    assert kan.is_open is False


def test_add_meld_to_hand():
    hand = Hand()

    chi = Meld(
        [Tile.S3, Tile.S4, Tile.S5],
        MeldType.CHI,
        is_open=True
    )

    hand.add_meld(chi)

    assert len(hand.melds) == 1
    assert hand.is_open is True


def test_closed_kan_does_not_make_hand_open():
    hand = Hand()

    kan = Meld(
        [Tile.EAST, Tile.EAST, Tile.EAST, Tile.EAST],
        MeldType.KAN,
        is_open=False
    )

    hand.add_meld(kan)

    assert hand.is_open is False

def test_valid_chi():
    meld = Meld([Tile.M1, Tile.M2, Tile.M3], MeldType.CHI)
    assert meld.meld_type == MeldType.CHI


def test_invalid_chi_not_consecutive():
    with pytest.raises(ValueError):
        Meld([Tile.M1, Tile.M2, Tile.M4], MeldType.CHI)


def test_invalid_chi_honours():
    with pytest.raises(ValueError):
        Meld([Tile.EAST, Tile.SOUTH, Tile.WEST], MeldType.CHI)


def test_valid_pon():
    meld = Meld([Tile.P5, Tile.P5, Tile.P5], MeldType.PON)
    assert meld.meld_type == MeldType.PON


def test_invalid_pon():
    with pytest.raises(ValueError):
        Meld([Tile.P5, Tile.P5, Tile.P6], MeldType.PON)


def test_valid_kan():
    meld = Meld([Tile.RED] * 4, MeldType.KAN)
    assert meld.meld_type == MeldType.KAN


def test_invalid_kan():
    with pytest.raises(ValueError):
        Meld([Tile.RED, Tile.RED, Tile.RED, Tile.WHITE], MeldType.KAN)


def test_invalid_meld_tile_count():
    with pytest.raises(ValueError):
        Meld([Tile.M1, Tile.M2], MeldType.CHI)
