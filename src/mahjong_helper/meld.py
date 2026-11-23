from enum import Enum
from mahjong_helper.tiles import *

class MeldType(Enum):
    CHI ="chi"
    PON ="pon"
    KAN = "kan"

class Meld:
    def __init__(self,tiles,meld_type,is_open=True):
        if not isinstance(meld_type, MeldType):
            raise TypeError("meld_type must be a MeldType")

        if not all(isinstance(tile, Tile) for tile in tiles):
            raise TypeError("All meld tiles must be Tile instances")
        
        self.tiles=list(tiles)
        self.meld_type=meld_type # e.g. chi/pon/kan
        self.is_open=is_open