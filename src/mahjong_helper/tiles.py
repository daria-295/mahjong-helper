from enum import IntEnum


class Tile(IntEnum):
    # Manzu
    M1 = 0
    M2 = 1
    M3 = 2
    M4 = 3
    M5 = 4
    M6 = 5
    M7 = 6
    M8 = 7
    M9 = 8

    # Pinzu
    P1 = 9
    P2 = 10
    P3 = 11
    P4 = 12
    P5 = 13
    P6 = 14
    P7 = 15
    P8 = 16
    P9 = 17

    # Souzu
    S1 = 18
    S2 = 19
    S3 = 20
    S4 = 21
    S5 = 22
    S6 = 23
    S7 = 24
    S8 = 25
    S9 = 26

    # Winds
    NORTH = 27
    EAST = 28
    SOUTH = 29
    WEST = 30

    # Dragons
    WHITE = 31
    GREEN = 32
    RED = 33

# 34 unique tiles, 136 total tiles (4 x 34)
TILE_COUNT = 34
MAX_COPIES = 4

RED_FIVES = (Tile.M5,Tile.P5,Tile.S5)

RED_FIVE_COPIES = 1
NORMAL_FIVE_COPIES = 3

def is_suit(tile: Tile) -> bool:
    return tile.value < 27

def is_honour(tile: Tile) -> bool:
    return tile.value >= 27

def is_five(tile: Tile) -> bool:
    return tile in RED_FIVES

def get_suit(tile: Tile) -> str | None:
    if tile.value < 9:
        return "manzu"
    elif tile.value < 18:
        return "pinzu"
    elif tile.value < 27:
        return "souzu"

    return None

def get_rank(tile: Tile) -> int | None:
    if not is_suit(tile):
        return None

    return (tile.value % 9) + 1

def to_string(tile: Tile) -> str:
    if is_suit(tile):
        suit_letter = {
            "manzu": "m","pinzu": "p","souzu": "s"
        }[get_suit(tile)]

        return f"{get_rank(tile)}{suit_letter}"

    return {
        Tile.NORTH: "N", Tile.EAST: "E",
        Tile.SOUTH: "S",Tile.WEST: "W",
        Tile.WHITE: "Wh",Tile.GREEN: "G",
        Tile.RED: "R"
    }[tile]

