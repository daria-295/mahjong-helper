from mahjong_helper.tiles import *
from mahjong_helper.meld import *

class Hand():
    def __init__(self):
        self.concealed_tiles = [0] *TILE_COUNT
        self.red_fives={Tile.M5:0,Tile.P5:0,Tile.S5:0}
        self.melds=[]

    @property
    def is_open(self):
        return any(meld.is_open for meld in self.melds)

    def add_tile(self,tile,is_red=False):
        if not isinstance(tile,Tile):
            raise TypeError("tile must be an instance of Tile")

        if is_red and tile not in RED_FIVES:
            raise ValueError("Only suited fives can be red")

        if self.concealed_tiles[tile.value] >=4:
            raise ValueError("Cannot have more than four copies of a tile")

        if is_red and self.red_fives[tile]>= RED_FIVE_COPIES:
            raise ValueError("Cannot have more than one red five of each suit")

        self.concealed_tiles[tile.value] += 1

        if is_red:
            self.red_fives[tile] +=1

    def remove_tile(self,tile,is_red=False):
        if not isinstance(tile,Tile):
            raise TypeError("tile must be an instance of Tile")

        if is_red and tile not in RED_FIVES:
            raise ValueError("Only suited fives can be red")

        if self.concealed_tiles[tile.value] ==0:
            raise ValueError("Tile doesn't exist in hand")

        if is_red and self.red_fives[tile] == 0:
            raise ValueError("No red five of this suit exists in hand")

        self.concealed_tiles[tile.value] -= 1

        if is_red:
            self.red_fives[tile] -=1

    def clear_hand(self):
        self.concealed_tiles = [0] * TILE_COUNT

        for tile in self.red_fives:
            self.red_fives[tile] = 0

        self.melds.clear()

    def get_total_tiles(self):
        return sum(self.concealed_tiles)

    def get_count_of_a_tile(self,tile):
        if not isinstance(tile,Tile):
            raise TypeError("tile must be an instance of Tile")

        return self.concealed_tiles[tile.value]

    def get_hand(self):
        return self.concealed_tiles.copy()

    def get_hand_string(self):
        tiles=[]

        for tile in Tile:
            for _ in range(self.concealed_tiles[tile.value]):
                tiles.append(to_string(tile))

        return " ".join(tiles)

    def add_meld(self,meld):
        if not isinstance(meld,Meld):
            raise TypeError("meld must be an instance of Meld")
        self.melds.append(meld)

    def get_expected_tile_count(self,is_drawn=False):
        meld_count =len(self.melds)
        if is_drawn:
            return 14 - (3 * meld_count)

        return 13 - (3 * meld_count)

    def validate_hand_size(self, is_drawn=False):
        expected=self.get_expected_tile_count(is_drawn)

        if self.get_total_tiles() != expected:
            raise ValueError(
                f"Hand must contain {expected} concealed tiles, "
                f"but contains {self.get_total_tiles()}"
            )

        