from enum import Enum
from collections import Counter
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

        self.validate()

    def validate(self):
        expected_count = {
            MeldType.CHI: 3,
            MeldType.PON: 3,
            MeldType.KAN: 4
        }

        if len(self.tiles) != expected_count[self.meld_type]:
            raise ValueError("Incorrect number of tiles for meld type")

        if self.meld_type == MeldType.CHI:
            self.validate_chi()

        elif self.meld_type == MeldType.PON:
            self.validate_pon()

        elif self.meld_type == MeldType.KAN:
            self.validate_kan()

    def validate_chi(self):
        indices=sorted(int(tile) for tile in self.tiles)

        if indices[0] >= 27:
            raise ValueError("Chi cannot contain honour tiles")

        if not (
            indices[0] // 9 == indices[2] // 9
            and indices[1] == indices[0] + 1
            and indices[2] == indices[0] + 2
        ):
            raise ValueError("Chi must contain three consecutive suited tiles")
    
    def validate_pon(self):
        if len(set(self.tiles)) != 1:
            raise ValueError("Pon must contain three identical tiles")

    def validate_kan(self):
        if len(set(self.tiles)) != 1:
            raise ValueError("Kan must contain four identical tiles")