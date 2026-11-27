
from .hand import Hand
from .tiles import Tile
from .shanten import calculate_shanten, get_ukeire

def analyze_discards(hand: Hand, visible_tiles=None) -> list[dict]:
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    hand.validate_hand_size(is_drawn=True)

    if visible_tiles is None:
        visible_tiles = []

    visible_tiles = list(visible_tiles)

    if not all(isinstance(tile, Tile) for tile in visible_tiles):
        raise TypeError("visible_tiles must contain Tile instances")

    results = []

    for tile in Tile:
        count = hand.get_count_of_a_tile(tile)

        if count == 0:
            continue

        red_count = hand.red_fives.get(tile, 0)
        normal_count = count - red_count

        if normal_count > 0:
            results.append(
                evaluate_discard(hand, tile, False, visible_tiles)
            )

        if red_count > 0:
            results.append(
                evaluate_discard(hand, tile, True, visible_tiles)
            )

    results.sort(
        key=lambda result: (
            result["shanten"],
            -result["total_ukeire"]
        )
    )

    return results

def evaluate_discard(
    hand: Hand,
    tile: Tile,
    is_red: bool,
    visible_tiles: list[Tile]
) -> dict:

    candidate = Hand()
    candidate.concealed_tiles = hand.get_hand()
    candidate.red_fives = hand.red_fives.copy()
    candidate.melds = hand.melds.copy()

    candidate.remove_tile(tile, is_red=is_red)

    shanten = calculate_shanten(candidate)
    ukeire = get_ukeire(candidate, visible_tiles)

    return {
        "discard": tile,
        "is_red": is_red,
        "shanten": shanten,
        "ukeire": ukeire,
        "total_ukeire": sum(ukeire.values())
    }

def get_best_discards(hand: Hand, visible_tiles=None) -> list[dict]:
    results = analyze_discards(hand, visible_tiles)

    if not results:
        return []

    best_shanten = results[0]["shanten"]
    best_ukeire = results[0]["total_ukeire"]

    return [
        result
        for result in results
        if (
            result["shanten"] == best_shanten
            and result["total_ukeire"] == best_ukeire
        )
    ]
