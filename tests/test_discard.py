
import pytest

from mahjong_helper.hand import Hand
from mahjong_helper.tiles import Tile
from mahjong_helper.meld import Meld, MeldType
from mahjong_helper.discard import analyze_discards, get_best_discards


def make_test_hand():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M2, Tile.M3,
        Tile.P1, Tile.P2, Tile.P3,
        Tile.S1, Tile.S2, Tile.S3,
        Tile.S7, Tile.S8,
        Tile.EAST, Tile.EAST,
        Tile.RED
    ]

    for tile in tiles:
        hand.add_tile(tile)

    return hand

def test_analyze_discards_returns_results():
    hand = make_test_hand()

    results = analyze_discards(hand)

    assert len(results) > 0

def test_analyze_discards_checks_every_unique_tile():
    hand = make_test_hand()

    results = analyze_discards(hand)

    discarded_tiles = {
        result["discard"] for result in results
    }

    assert discarded_tiles == set(Tile[tile.name] for tile in hand_tiles(hand))

def hand_tiles(hand):
    return [
        tile
        for tile in Tile
        if hand.get_count_of_a_tile(tile) > 0
    ]

def test_discard_results_are_ranked():
    hand = make_test_hand()

    results = analyze_discards(hand)

    rankings = [
        (result["shanten"], -result["total_ukeire"])
        for result in results
    ]

    assert rankings == sorted(rankings)

def test_discard_results_include_ukeire():
    hand = make_test_hand()

    results = analyze_discards(hand)

    for result in results:
        assert isinstance(result["ukeire"], dict)
        assert result["total_ukeire"] == sum(
            result["ukeire"].values()
        )

def test_analyze_discards_distinguishes_red_fives():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M2, Tile.M3,
        Tile.P1, Tile.P2, Tile.P3,
        Tile.S1, Tile.S2, Tile.S3,
        Tile.S7, Tile.S8,
        Tile.EAST, Tile.EAST,
        Tile.M5
    ]

    for tile in tiles:
        hand.add_tile(tile)

    # Replace the ordinary five with a red five.
    hand.remove_tile(Tile.M5)
    hand.add_tile(Tile.M5, is_red=True)

    results = analyze_discards(hand)

    five_discards = [
        result for result in results
        if result["discard"] == Tile.M5
    ]

    assert len(five_discards) == 1
    assert five_discards[0]["is_red"] is True

def test_analyze_discards_rejects_wrong_hand_size():
    hand = Hand()
    hand.add_tile(Tile.M1)

    with pytest.raises(ValueError):
        analyze_discards(hand)

def test_analyze_discards_with_existing_meld():
    hand = Hand()

    hand.add_meld(
        Meld(
            [Tile.M1, Tile.M2, Tile.M3],
            MeldType.CHI
        )
    )

    tiles = [
        Tile.P1, Tile.P2, Tile.P3,
        Tile.S1, Tile.S2, Tile.S3,
        Tile.S7, Tile.S8,
        Tile.EAST, Tile.EAST,
        Tile.RED
    ]

    for tile in tiles:
        hand.add_tile(tile)

    results = analyze_discards(hand)

    assert len(results) > 0

def test_analyze_discards_accounts_for_visible_tiles():
    hand = make_test_hand()

    results = analyze_discards(
        hand,
        visible_tiles=[Tile.S9, Tile.S9]
    )

    assert len(results) > 0

def test_get_best_discards_returns_results():
    hand = make_test_hand()

    results = get_best_discards(hand)

    assert len(results) > 0

def test_get_best_discards_only_returns_best_ranked():
    hand = make_test_hand()

    all_results = analyze_discards(hand)
    best_results = get_best_discards(hand)

    best_shanten = min(
        result["shanten"] for result in all_results
    )

    best_ukeire = max(
        result["total_ukeire"]
        for result in all_results
        if result["shanten"] == best_shanten
    )

    for result in best_results:
        assert result["shanten"] == best_shanten
        assert result["total_ukeire"] == best_ukeire

def test_get_best_discards_does_not_modify_hand():
    hand = make_test_hand()

    original_tiles = hand.get_hand()
    original_red_fives = hand.red_fives.copy()

    get_best_discards(hand)

    assert hand.get_hand() == original_tiles
    assert hand.red_fives == original_red_fives
