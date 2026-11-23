from mahjong_helper.tiles import *

print(to_string(Tile.M1))
print(to_string(Tile.P5))
print(to_string(Tile.EAST))

print(is_suit(Tile.S5))
print(is_honour(Tile.RED))
print(is_five(Tile.P5))

print(get_suit(Tile.P5))
print(get_rank(Tile.P5))