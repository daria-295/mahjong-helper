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
