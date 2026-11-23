from mahjong_helper.tiles import *

class Hand():
    def __init__(self):
        self.tiles = []

    def add_tile(self,tile):
        self.tiles.append(tile)

    def remove_tile(self,tile):
        self.tiles.remove(tile)

    def remove_tile_at(self, position):
        return self.tiles.pop(position)

    def clear_hand(self):
        self.tiles = []

    def get_hand(self):
        return self.tiles

    def get_hand_string(self):
        return " ".join(to_string(tile) for tile in self.tiles)