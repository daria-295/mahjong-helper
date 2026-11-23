from mahjong_helper.hand import *

hand = Hand()
hand.add_tile(Tile.M1)
hand.add_tile(Tile.M2)
hand.add_tile(Tile.WHITE)
hand.add_tile(Tile.M3)
hand.add_tile(Tile.M3)
hand.add_tile(Tile.S7)
hand.add_tile(Tile.EAST)
hand.add_tile(Tile.EAST)
hand.add_tile(Tile.WHITE)

print(f"Initial hand: {hand.get_hand_string()}")

print("\nRemoving 1 WHITE tile...\n")
hand.remove_tile(Tile.WHITE)
#hand.remove_tile_at(8)

print(hand.get_hand_string())