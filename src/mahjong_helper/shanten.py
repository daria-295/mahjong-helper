# Shanten measures how many tile improvements a hand needs before reaching Tenpai
# -1: complete winning hand
# 0: Tenpai (1 tile away from winning)
# 1: One improvement from Tenpai
# 2: Two improvements from Tenpai

# Shanten formula: S = 8 - 2M - T - P
# M = n.o. complete melds, meld
# T = n.o. incomplete melds, taatsu
# P = 1 if we have a pair, otherwise 0

from .hand import Hand

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

def calculate_groups(tile_counts,melds=0,taatsu=0,pairs=0):
    tile_index=find_first_tile(tile_counts)

    if tile_index is None:
        return [(melds,taatsu,pairs)]

    results=[]
    # finding triplets
    if tile_counts[tile_index] >=3:
        tile_counts[tile_index] -=3

        results.extend(calculate_groups(tile_counts,melds+1,taatsu,pairs))
        tile_counts[tile_index] +=3

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

    return results