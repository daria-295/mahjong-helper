from enum import Enum
from dataclasses import dataclass
from collections import Counter

from .tiles import Tile
from .hand import Hand
from .meld import MeldType
from .shanten import is_complete_hand, is_chiitoitsu, is_kokushi, find_hand_decompositions

class Yaku(Enum):
    RIICHI = "Riichi"
    DOUBLE_RIICHI = "Double Riichi"
    IPPATSU = "Ippatsu"
    MENZEN_TSUMO = "Menzen Tsumo"
    TANYAO = "Tanyao"
    RINSHAN_KAIHOU = "Rinshan Kaihou"
    CHANKAN = "Chankan"
    HAITEI = "Haitei"
    HOUTEI = "Houtei"
    DRAGON_YAKUHAI = "Dragon Yakuhai"
    SEAT_WIND = "Seat Wind"
    ROUND_WIND = "Round Wind"
    TOITOI = "Toitoi"
    HONITSU = "Honitsu"
    CHINITSU = "Chinitsu"
    CHANTA = "Chanta"
    JUNCHAN = "Junchan"
    IIPEIKOU = "Iipeikou"
    RYANPEIKOU = "Ryanpeikou"
    SANSHOKU_DOUJUN = "Sanshoku Doujun"
    ITTSU = "Ittsu"
    SANSHOKU_DOUKOU = "Sanshoku Doukou"
    HONROUTOU = "Honroutou"
    SHOUSANGEN = "Shousangen"
    SANANKOU = "Sanankou"
    SANKANTSU = "Sankantsu"
    PINFU = "Pinfu"
    CHIITOITSU = "Chiitoitsu"
    SUUANKOU = "Suuankou"
    SUUKANTSU = "Suukantsu"
    RYUUIISOU = "Ryuuiisou"
    CHUUREN_POUTOU = "Chuuren Poutou"
    KOKUSHI_MUSOU = "Kokushi Musou"

    # Yakuman
    DAISANGEN = "Daisangen"
    SHOUSUUSHI = "Shousuushi"
    TSUUIISOU = "Tsuuiisou"
    CHINROUTOU = "Chinroutou"
    DAISUUSHI = "Daisuushi"
    TENHOU = "Tenhou"
    CHIIHOU = "Chiihou"

class WinMethod(Enum):
    RON = "ron"
    TSUMO = "tsumo"

@dataclass
class HandContext:
    win_method: WinMethod

    riichi: bool = False
    double_riichi: bool = False
    ippatsu: bool = False

    rinshan: bool = False
    chankan: bool = False
    haitei: bool = False
    houtei: bool = False

    seat_wind: Tile | None = None
    round_wind: Tile | None = None
    winning_tile: Tile | None = None

    tenhou: bool = False
    chiihou: bool = False

def is_tanyao(hand: Hand, allow_open=True) -> bool:
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    if hand.is_open and not allow_open:
        return False

    all_tiles = []

    # concealed tiles
    for tile in Tile:
        all_tiles.extend(
            [tile] * hand.get_count_of_a_tile(tile)
        )

    # tiles in declared melds
    for meld in hand.melds:
        all_tiles.extend(meld.tiles)

    # simple tiles are suited tiles numbered 2-8.
    for tile in all_tiles:
        if tile.value >= 27:
            return False

        rank = tile.value % 9 + 1

        if rank == 1 or rank == 9:
            return False

    return True

def detect_yaku(hand: Hand, context: HandContext, allow_open_tanyao=True) -> list[Yaku]:
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    if not isinstance(context, HandContext):
        raise TypeError("context must be a HandContext instance")

    if not isinstance(context.win_method, WinMethod):
        raise TypeError("win_method must be a WinMethod")

    if not is_complete_hand(hand):
        raise ValueError("Cannot detect yaku for an incomplete hand")

    yaku = []

    # Tanyao
    if is_tanyao(hand, allow_open_tanyao):
        yaku.append(Yaku.TANYAO)

    # Yakuhai
    yaku.extend(detect_yakuhai(hand, context))

    # Toitoi
    if is_toitoi(hand):
        yaku.append(Yaku.TOITOI)

    # Honitsu and Chinitsu
    if is_chinitsu(hand):
        yaku.append(Yaku.CHINITSU)
    elif is_honitsu(hand):
        yaku.append(Yaku.HONITSU)

    # Chanta and Junchan
    if is_junchan(hand):
        yaku.append(Yaku.JUNCHAN)
    elif is_chanta(hand):
        yaku.append(Yaku.CHANTA)

    # Iipeikou and Ryanpeikou
    if is_ryanpeikou(hand):
        yaku.append(Yaku.RYANPEIKOU)
    elif is_iipeikou(hand):
        yaku.append(Yaku.IIPEIKOU)

    # Sequence-based Yaku
    if is_sanshoku_doujun(hand):
        yaku.append(Yaku.SANSHOKU_DOUJUN)

    if is_ittsu(hand):
        yaku.append(Yaku.ITTSU)

    # Triplet-based Yaku
    if is_sanshoku_doukou(hand):
        yaku.append(Yaku.SANSHOKU_DOUKOU)

    # Triplet and terminal/honour-based Yaku
    if is_honroutou(hand):
        yaku.append(Yaku.HONROUTOU)

    if is_shousangen(hand):
        yaku.append(Yaku.SHOUSANGEN)

    if is_sanankou(hand, context):
        yaku.append(Yaku.SANANKOU)

    if is_sankantsu(hand):
        yaku.append(Yaku.SANKANTSU)

    if is_pinfu(hand, context):
        yaku.append(Yaku.PINFU)

    # Seven pairs
    if is_chiitoitsu(hand):
        yaku.append(Yaku.CHIITOITSU)

    # Yakuman
    if is_daisangen(hand):
        yaku.append(Yaku.DAISANGEN)

    if is_shousuushi(hand):
        yaku.append(Yaku.SHOUSUUSHI)

    if is_tsuuiisou(hand):
        yaku.append(Yaku.TSUUIISOU)

    if is_chinroutou(hand):
        yaku.append(Yaku.CHINROUTOU)

    if is_suuankou(hand, context):
        yaku.append(Yaku.SUUANKOU)

    if is_suukantsu(hand):
        yaku.append(Yaku.SUUKANTSU)

    if is_ryuuiisou(hand):
        yaku.append(Yaku.RYUUIISOU)

    if is_chuuren_poutou(hand):
        yaku.append(Yaku.CHUUREN_POUTOU)

    if is_kokushi_musou(hand):
        yaku.append(Yaku.KOKUSHI_MUSOU)

    if is_daisuushi(hand):
        yaku.append(Yaku.DAISUUSHI)

    if is_tenhou(hand, context):
        yaku.append(Yaku.TENHOU)

    if is_chiihou(hand, context):
        yaku.append(Yaku.CHIIHOU)

    # Riichi-related yaku
    if not hand.is_open:
        if context.double_riichi:
            yaku.append(Yaku.DOUBLE_RIICHI)
        elif context.riichi:
            yaku.append(Yaku.RIICHI)

        if context.ippatsu and (context.riichi or context.double_riichi):
            yaku.append(Yaku.IPPATSU)

        if context.win_method == WinMethod.TSUMO:
            yaku.append(Yaku.MENZEN_TSUMO)

    # Situational yaku
    if context.rinshan and context.win_method == WinMethod.TSUMO:
        yaku.append(Yaku.RINSHAN_KAIHOU)

    if context.chankan and context.win_method == WinMethod.RON:
        yaku.append(Yaku.CHANKAN)

    if context.haitei and context.win_method == WinMethod.TSUMO:
        yaku.append(Yaku.HAITEI)

    if context.houtei and context.win_method == WinMethod.RON:
        yaku.append(Yaku.HOUTEI)

    return yaku

def get_all_tile_counts(hand: Hand) -> list[int]:
    counts = hand.get_hand()

    for meld in hand.melds:
        for tile in meld.tiles:
            counts[tile.value] += 1

    return counts

def detect_yakuhai(hand: Hand, context: HandContext) -> list[Yaku]:
    counts = get_all_tile_counts(hand)
    result = []

    # dragon triplets
    for dragon in [Tile.WHITE, Tile.GREEN, Tile.RED]:
        if counts[dragon.value] >= 3:
            result.append(Yaku.DRAGON_YAKUHAI)

    # seat wind triplet
    if context.seat_wind is not None:
        if context.seat_wind not in [
            Tile.EAST, Tile.SOUTH, Tile.WEST, Tile.NORTH
        ]:
            raise ValueError("seat_wind must be a wind tile")

        if counts[context.seat_wind.value] >= 3:
            result.append(Yaku.SEAT_WIND)

    # round wind triplet
    if context.round_wind is not None:
        if context.round_wind not in [
            Tile.EAST, Tile.SOUTH, Tile.WEST, Tile.NORTH
        ]:
            raise ValueError("round_wind must be a wind tile")

        if counts[context.round_wind.value] >= 3:
            result.append(Yaku.ROUND_WIND)

    return result

def can_form_triplets(tile_counts: list[int]) -> bool:
    # finding the first tile still remaining.
    tile_index = next(
        (i for i, count in enumerate(tile_counts) if count > 0),
        None
    )

    if tile_index is None:
        return True

    # trying to remove a triplet.
    if tile_counts[tile_index] >= 3:
        tile_counts[tile_index] -= 3

        if can_form_triplets(tile_counts):
            tile_counts[tile_index] += 3
            return True

        tile_counts[tile_index] += 3

    return False

def is_toitoi(hand: Hand) -> bool:
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    hand.validate_hand_size(is_drawn=True)

    if any(meld.meld_type == MeldType.CHI for meld in hand.melds):
        return False

    tile_counts = hand.get_hand()

    # trying every possible pair.
    for index, count in enumerate(tile_counts):
        if count >= 2:
            tile_counts[index] -= 2

            if can_form_triplets(tile_counts):
                tile_counts[index] += 2
                return True

            tile_counts[index] += 2

    return False

def is_honitsu(hand: Hand) -> bool:
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    counts = get_all_tile_counts(hand)

    suits = {
        tile.value // 9
        for tile in Tile
        if tile.value < 27 and counts[tile.value] > 0
    }

    has_honours = any(
        counts[tile.value] > 0
        for tile in Tile
        if tile.value >= 27
    )

    return len(suits) == 1 and has_honours

def is_chinitsu(hand: Hand) -> bool:
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    counts = get_all_tile_counts(hand)

    suits = {
        tile.value // 9
        for tile in Tile
        if tile.value < 27 and counts[tile.value] > 0
    }

    has_honours = any(
        counts[tile.value] > 0
        for tile in Tile
        if tile.value >= 27
    )

    return len(suits) == 1 and not has_honours

def get_decomposition_groups(decomposition):
    sequences = list(decomposition["sequences"])
    triplets = list(decomposition["triplets"])

    # include declared melds.
    for meld in decomposition["declared_melds"]:
        indices = tuple(sorted(int(tile) for tile in meld.tiles))

        if meld.meld_type == MeldType.CHI:
            sequences.append(indices)
        else:
            triplets.append(indices)

    return sequences, triplets

def is_terminal_or_honour(index):
    return index >= 27 or index % 9 in (0, 8)

def is_terminal(index):
    return index < 27 and index % 9 in (0, 8)

def has_chanta_structure(decomposition, junchan=False):
    sequences, triplets = get_decomposition_groups(decomposition)

    if not sequences:
        return False

    pair_index = decomposition["pair"][0]

    # checking pair
    if junchan:
        if not is_terminal(pair_index):
            return False
    else:
        if not is_terminal_or_honour(pair_index):
            return False

    # every sequence must contain a terminal
    for sequence in sequences:
        if sequence[0] % 9 not in (0, 6):
            return False

    # every triplet must be a terminal or honour
    for triplet in triplets:
        index = triplet[0]

        if junchan:
            if not is_terminal(index):
                return False
        else:
            if not is_terminal_or_honour(index):
                return False

    return True

def is_chanta(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")
    counts = get_all_tile_counts(hand)

    # Chanta must contain at least one honour
    if not any(counts[index] > 0 for index in range(27, 34)):
        return False

    return any(
        has_chanta_structure(decomposition)
        for decomposition in find_hand_decompositions(hand)
    )

def is_junchan(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    # junchan cannot contain honour tiles
    counts = get_all_tile_counts(hand)

    if any(counts[index] > 0 for index in range(27, 34)):
        return False

    return any(
        has_chanta_structure(decomposition, junchan=True)
        for decomposition in find_hand_decompositions(hand)
    )

def is_iipeikou(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    if hand.is_open:
        return False

    for decomposition in find_hand_decompositions(hand):
        sequences, _ = get_decomposition_groups(decomposition)
        sequence_counts = Counter(sequences)

        duplicate_pairs = sum(
            count // 2 for count in sequence_counts.values()
        )

        # Ryanpeikou takes precedence over Iipeikou.
        if duplicate_pairs == 1:
            return True

    return False

def is_ryanpeikou(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    if hand.is_open:
        return False

    for decomposition in find_hand_decompositions(hand):
        sequences, _ = get_decomposition_groups(decomposition)
        sequence_counts = Counter(sequences)

        duplicate_pairs = sum(
            count // 2 for count in sequence_counts.values()
        )

        if duplicate_pairs >= 2:
            return True

    return False

def is_sanshoku_doujun(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    for decomposition in find_hand_decompositions(hand):
        sequences, _ = get_decomposition_groups(decomposition)

        sequence_starts = {
            sequence[0] % 9
            for sequence in sequences
        }

        for start in sequence_starts:
            suits = {
                sequence[0] // 9
                for sequence in sequences
                if sequence[0] % 9 == start
            }

            if len(suits) == 3:
                return True

    return False

def is_ittsu(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    for decomposition in find_hand_decompositions(hand):
        sequences, _ = get_decomposition_groups(decomposition)

        for suit in range(3):
            starts = {
                sequence[0] % 9
                for sequence in sequences
                if sequence[0] // 9 == suit
            }

            if {0, 3, 6}.issubset(starts):
                return True

    return False

def is_sanshoku_doukou(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    for decomposition in find_hand_decompositions(hand):
        _, triplets = get_decomposition_groups(decomposition)

        triplet_starts = {
            triplet[0] % 9
            for triplet in triplets
            if triplet[0] < 27
        }

        for start in triplet_starts:
            suits = {
                triplet[0] // 9
                for triplet in triplets
                if triplet[0] < 27 and triplet[0] % 9 == start
            }

            if len(suits) == 3:
                return True

    return False

def is_honroutou(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    counts = get_all_tile_counts(hand)

    if any(
        count > 0 and not is_terminal_or_honour(index)
        for index, count in enumerate(counts)
    ):
        return False

    if is_chiitoitsu(hand):
        return True

    for decomposition in find_hand_decompositions(hand):
        sequences, _ = get_decomposition_groups(decomposition)

        if not sequences:
            return True

    return False

def is_shousangen(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    for decomposition in find_hand_decompositions(hand):
        _, triplets = get_decomposition_groups(decomposition)
        pair_index = decomposition["pair"][0]

        dragon_triplets = sum(
            triplet[0] in (31, 32, 33)
            for triplet in triplets
        )

        if dragon_triplets >= 2 and pair_index in (31, 32, 33):
            return True

    return False

def is_sanankou(hand, context):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    if not isinstance(context, HandContext):
        raise TypeError("context must be a HandContext instance")

    for decomposition in find_hand_decompositions(hand):
        _, triplets = get_decomposition_groups(decomposition)

        concealed_triplets = len(decomposition["triplets"])

        concealed_triplets += sum(
            not meld.is_open and meld.meld_type in (
                MeldType.PON,
                MeldType.KAN
            )
            for meld in hand.melds
        )

        if context.win_method == WinMethod.RON:
            if context.winning_tile is None:
                continue

            if any(
                triplet[0] == context.winning_tile.value
                for triplet in decomposition["triplets"]
            ):
                concealed_triplets -= 1

        if concealed_triplets >= 3:
            return True

    return False

def is_sankantsu(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    kan_count = sum(
        meld.meld_type == MeldType.KAN
        for meld in hand.melds
    )

    return kan_count >= 3

def is_pinfu(hand, context):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    if not isinstance(context, HandContext):
        raise TypeError("context must be a HandContext instance")

    if hand.is_open or context.winning_tile is None:
        return False

    pair_winds = (Tile.EAST, Tile.SOUTH, Tile.WEST, Tile.NORTH)

    for decomposition in find_hand_decompositions(hand):
        sequences, triplets = get_decomposition_groups(decomposition)

        if len(sequences) != 4 or triplets:
            continue

        pair_index = decomposition["pair"][0]

        if pair_index in (31, 32, 33):
            continue

        if pair_index >= 27:
            if (
                context.seat_wind is None
                or context.round_wind is None
            ):
                continue

            if pair_index in (
                context.seat_wind.value,
                context.round_wind.value
            ):
                continue

        for sequence in sequences:
            if context.winning_tile.value not in sequence:
                continue

            offset = sequence.index(context.winning_tile.value)
            start_rank = sequence[0] % 9

            if offset == 1:
                continue

            if offset == 2 and start_rank == 0:
                continue

            if offset == 0 and start_rank == 6:
                continue

            return True

    return False

def is_daisangen(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    for decomposition in find_hand_decompositions(hand):
        _, triplets = get_decomposition_groups(decomposition)

        dragon_triplets = sum(
            triplet[0] in (31, 32, 33)
            for triplet in triplets
        )

        if dragon_triplets == 3:
            return True

    return False

def is_shousuushi(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    for decomposition in find_hand_decompositions(hand):
        _, triplets = get_decomposition_groups(decomposition)

        wind_triplets = sum(
            triplet[0] in (27, 28, 29, 30)
            for triplet in triplets
        )

        pair_index = decomposition["pair"][0]

        if wind_triplets == 3 and pair_index in (27, 28, 29, 30):
            return True

    return False

def is_tsuuiisou(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    counts = get_all_tile_counts(hand)

    return all(
        count == 0 or index >= 27
        for index, count in enumerate(counts)
    )

def is_chinroutou(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    terminal_indices = {0, 8, 9, 17, 18, 26}
    counts = get_all_tile_counts(hand)

    return all(
        count == 0 or index in terminal_indices
        for index, count in enumerate(counts)
    )

def is_suuankou(hand, context):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    if not isinstance(context, HandContext):
        raise TypeError("context must be a HandContext instance")

    for decomposition in find_hand_decompositions(hand):
        concealed_triplets = len(decomposition["triplets"])

        concealed_triplets += sum(
            not meld.is_open and meld.meld_type in (
                MeldType.PON,
                MeldType.KAN
            )
            for meld in hand.melds
        )

        if context.win_method == WinMethod.RON:
            if context.winning_tile is None:
                continue

            if any(
                triplet[0] == context.winning_tile.value
                for triplet in decomposition["triplets"]
            ):
                concealed_triplets -= 1

        if concealed_triplets == 4:
            return True

    return False

def is_suukantsu(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    kan_count = sum(
        meld.meld_type == MeldType.KAN
        for meld in hand.melds
    )

    return kan_count == 4

def is_ryuuiisou(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    green_tiles = {19, 20, 21, 23, 25, 32}
    counts = get_all_tile_counts(hand)

    return all(
        count == 0 or index in green_tiles
        for index, count in enumerate(counts)
    )

def is_chuuren_poutou(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    if hand.is_open or hand.melds:
        return False

    counts = hand.get_hand()

    if sum(counts) != 14:
        return False

    base_pattern = [3, 1, 1, 1, 1, 1, 1, 1, 3]

    for suit_start in (0, 9, 18):
        suit_counts = counts[suit_start:suit_start + 9]

        if all(
            suit_counts[i] >= base_pattern[i]
            for i in range(9)
        ):
            if sum(suit_counts) == 14:
                return True

    return False

def is_kokushi_musou(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    if hand.melds:
        return False

    return is_kokushi(hand)

def is_daisuushi(hand):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    for decomposition in find_hand_decompositions(hand):
        _, triplets = get_decomposition_groups(decomposition)

        wind_triplets = sum(
            triplet[0] in (27, 28, 29, 30)
            for triplet in triplets
        )

        if wind_triplets == 4:
            return True

    return False

def is_tenhou(hand, context):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    if not isinstance(context, HandContext):
        raise TypeError("context must be a HandContext instance")

    return (
        context.tenhou
        and context.win_method == WinMethod.TSUMO
        and not hand.melds
    )

def is_chiihou(hand, context):
    if not isinstance(hand, Hand):
        raise TypeError("hand must be a Hand instance")

    if not isinstance(context, HandContext):
        raise TypeError("context must be a HandContext instance")

    return (
        context.chiihou
        and context.win_method == WinMethod.TSUMO
        and not hand.melds
    )
