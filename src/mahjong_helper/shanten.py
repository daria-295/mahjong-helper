# Shanten measures how many tile improvements a hand needs before reaching Tenpai
# -1: complete winning hand
# 0: Tenpai (1 tile away from winning)
# 1: One improvement from Tenpai
# 2: Two improvements from Tenpai

# Shanten formula: S = 8 - 2Mt - min(T, 4-mt) - P
# Mt = total complete melds, meld
# T = n.o. incomplete melds, taatsu
# P = 1 if we have a pair, otherwise 0

from .hand import Hand
from .tiles import Tile


def find_first_tile(tile_counts):
    # finds, returns the index of the first tile with a count greater than zero, or None if no tiles remain.
    for index, count in enumerate(tile_counts):
        if count > 0:
            return index

    return None

def calculate_shanten(hand:Hand)->int:
    if not isinstance(hand,Hand):
        raise TypeError("hand must be a Hand instance")

    tile_counts=hand.get_hand()
    existing_meld_count=len(hand.melds)

    groupings=calculate_groups(tile_counts)
    best_shanten=8

    for melds,taatsu,pairs in groupings:
        total_melds= melds + existing_meld_count

        if total_melds > 4:
            continue

        effective_taatsu=taatsu + max(0, pairs - 1)
        available_slots = 4 - total_melds
        useful_taatsu = min(effective_taatsu, available_slots)

        has_pair = 1 if pairs > 0 else 0
        shanten = 8 - (2 * total_melds) - useful_taatsu - has_pair
        best_shanten = min(best_shanten, shanten)

    return best_shanten

def is_complete_standard_hand(hand: Hand) -> bool:
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    hand.validate_hand_size(is_drawn=True)

    groupings= calculate_groups(hand.get_hand())
    existing_meld_count= len(hand.melds)

    for melds, taatsu, pairs in groupings:
        total_melds= melds + existing_meld_count

        if total_melds == 4 and pairs >= 1:
            return True

    return False

def calculate_groups(tile_counts,melds=0,taatsu=0,pairs=0):
    tile_index=find_first_tile(tile_counts)

    if tile_index is None:
        return [(melds,taatsu,pairs)]

    results=[]
    # finding triplets
    if tile_counts[tile_index] >= 3:
        tile_counts[tile_index] -= 3

        results.extend(calculate_groups(tile_counts, melds + 1, taatsu, pairs))
        tile_counts[tile_index] += 3

    # finding sequences
    if (
        tile_index < 27 # exclude honours
        and tile_index % 9 <= 6 # prevents crossing suit
        and tile_counts[tile_index + 1] > 0
        and tile_counts[tile_index + 2] > 0
    ):
        tile_counts[tile_index] -= 1
        tile_counts[tile_index + 1] -= 1
        tile_counts[tile_index + 2] -= 1

        results.extend(calculate_groups(tile_counts, melds + 1, taatsu, pairs))

        tile_counts[tile_index] += 1
        tile_counts[tile_index + 1] += 1
        tile_counts[tile_index + 2] += 1

    # finding pairs
    if tile_counts[tile_index] >= 2:
        tile_counts[tile_index] -=2
        
        results.extend(calculate_groups(tile_counts, melds, taatsu, pairs + 1))
            
        tile_counts[tile_index] += 2

    # skipping a tile
    tile_counts[tile_index] -= 1
    results.extend(
    calculate_groups(tile_counts, melds, taatsu, pairs))
    tile_counts[tile_index] += 1

    # finding adjacent taatsu (incomplete melds)
    if (tile_index < 27
        and tile_index % 9 <= 7
        and tile_counts[tile_index + 1] > 0):

        tile_counts[tile_index] -=1
        tile_counts[tile_index+1] -=1

        results.extend(calculate_groups(tile_counts,melds,taatsu+1,pairs))
        tile_counts[tile_index] += 1
        tile_counts[tile_index + 1] += 1
        

    # finding gapped taatsu
    if (tile_index < 27
        and tile_index % 9 <= 6
        and tile_counts[tile_index + 2] > 0):

        tile_counts[tile_index] -=1
        tile_counts[tile_index+2] -=1

        results.extend(calculate_groups(tile_counts,melds,taatsu+1,pairs))
        tile_counts[tile_index] += 1
        tile_counts[tile_index + 2] += 1



    return results

def find_hand_decompositions(hand: Hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    hand.validate_hand_size(is_drawn=True)

    tile_counts = hand.get_hand()
    existing_melds = list(hand.melds)
    decompositions = []

    def recurse(counts, melds, pair, sequences, triplets):
        if not any(counts):
            if melds == 4 and pair:
                decompositions.append({
                    "sequences": sequences.copy(),
                    "triplets": triplets.copy(),
                    "pair": pair
                })
            return

        index = find_first_tile(counts)

        # trying a pair
        if not pair and counts[index] >= 2:
            counts[index] -= 2
            recurse(counts, melds, (index, index), sequences, triplets)
            counts[index] += 2

        # trying a triplet
        if counts[index] >= 3 and melds < 4:
            counts[index] -= 3
            triplets.append((index, index, index))
            recurse(counts, melds + 1, pair, sequences, triplets)
            triplets.pop()
            counts[index] += 3

        # trying a sequence
        if (
            index < 27
            and index % 9 <= 6
            and counts[index + 1] > 0
            and counts[index + 2] > 0
            and melds < 4
        ):
            counts[index] -= 1
            counts[index + 1] -= 1
            counts[index + 2] -= 1

            sequences.append((index, index + 1, index + 2))
            recurse(counts, melds + 1, pair, sequences, triplets)
            sequences.pop()

            counts[index] += 1
            counts[index + 1] += 1
            counts[index + 2] += 1

    recurse(
        tile_counts,
        len(existing_melds),
        None,
        [],
        []
    )

    for decomposition in decompositions:
        decomposition["declared_melds"] = existing_melds.copy()

    return decompositions


# tests for seven pairs format
def is_chiitoitsu(hand: Hand) -> bool:
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    if hand.melds:
        return False

    hand.validate_hand_size(is_drawn=True)
    tile_counts = hand.get_hand()
    pairs = sum(1 for count in tile_counts if count == 2)

    return pairs == 7

# Thirteen Orphans
KOKUSHI_TILES = [
    Tile.M1, Tile.M9,
    Tile.P1, Tile.P9,
    Tile.S1, Tile.S9,
    Tile.EAST, Tile.SOUTH, Tile.WEST, Tile.NORTH,
    Tile.WHITE, Tile.GREEN, Tile.RED
]

def is_kokushi(hand: Hand) -> bool:
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    if hand.melds:
        return False

    hand.validate_hand_size(is_drawn=True)
    tile_counts = hand.get_hand()

    if not all(tile_counts[tile.value] >= 1 for tile in KOKUSHI_TILES):
        return False

    return sum(tile_counts[tile.value] for tile in KOKUSHI_TILES) == 14

def is_complete_hand(hand: Hand) -> bool:
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    return (
        is_complete_standard_hand(hand)
        or is_chiitoitsu(hand)
        or is_kokushi(hand)
    )

