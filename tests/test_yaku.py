from mahjong_helper.yaku import *
from mahjong_helper.tiles import Tile
from mahjong_helper.hand import Hand
from mahjong_helper.meld import Meld, MeldType

def make_tanyao_hand():
    hand = Hand()

    tiles = [
        Tile.M2, Tile.M3, Tile.M4,
        Tile.M5, Tile.M6, Tile.M7,
        Tile.P2, Tile.P3, Tile.P4,
        Tile.S3, Tile.S4, Tile.S5,
        Tile.P6, Tile.P6
    ]

    for tile in tiles:
        hand.add_tile(tile)

    return hand

def test_is_tanyao():
    hand = make_tanyao_hand()
    assert is_tanyao(hand) is True

def test_tanyao_rejects_terminal():
    hand = make_tanyao_hand()
    hand.remove_tile(Tile.M2)
    hand.add_tile(Tile.M1)

    assert is_tanyao(hand) is False

def test_tanyao_rejects_honour():
    hand = make_tanyao_hand()
    hand.remove_tile(Tile.M2)
    hand.add_tile(Tile.EAST)

    assert is_tanyao(hand) is False

def test_detect_tanyao():
    hand = make_tanyao_hand()
    context = HandContext(win_method=WinMethod.RON)

    assert detect_yaku(hand, context) == [Yaku.TANYAO]

def test_detect_riichi():
    hand = make_tanyao_hand()
    context = HandContext(
        win_method=WinMethod.RON,
        riichi=True
    )

    result = detect_yaku(hand, context)

    assert Yaku.RIICHI in result
    assert Yaku.TANYAO in result

def test_detect_menzen_tsumo():
    hand = make_tanyao_hand()
    context = HandContext(win_method=WinMethod.TSUMO)

    result = detect_yaku(hand, context)

    assert Yaku.MENZEN_TSUMO in result

def test_open_tanyao_disabled():
    hand = make_tanyao_hand()

    from mahjong_helper.meld import Meld, MeldType

    meld = Meld(
        [Tile.M2, Tile.M3, Tile.M4],
        MeldType.CHI
    )
    hand.add_meld(meld)

    assert is_tanyao(hand, allow_open=False) is False

def make_yakuhai_hand():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M2, Tile.M3,
        Tile.M4, Tile.M5, Tile.M6,
        Tile.P1, Tile.P2, Tile.P3,
        Tile.EAST, Tile.EAST, Tile.EAST,
        Tile.WHITE, Tile.WHITE
    ]

    for tile in tiles:
        hand.add_tile(tile)

    return hand

def test_seat_wind_yakuhai():
    hand = make_yakuhai_hand()

    context = HandContext(
        win_method=WinMethod.RON,
        seat_wind=Tile.EAST,
        round_wind=Tile.SOUTH
    )

    result = detect_yakuhai(hand, context)

    assert Yaku.SEAT_WIND in result

def test_round_wind_yakuhai():
    hand = make_yakuhai_hand()

    context = HandContext(
        win_method=WinMethod.RON,
        seat_wind=Tile.SOUTH,
        round_wind=Tile.EAST
    )

    result = detect_yakuhai(hand, context)

    assert Yaku.ROUND_WIND in result

def test_double_wind_yakuhai():
    hand = make_yakuhai_hand()

    context = HandContext(
        win_method=WinMethod.RON,
        seat_wind=Tile.EAST,
        round_wind=Tile.EAST
    )

    result = detect_yakuhai(hand, context)

    assert result.count(Yaku.SEAT_WIND) == 1
    assert result.count(Yaku.ROUND_WIND) == 1

def test_dragon_yakuhai():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M2, Tile.M3,
        Tile.M4, Tile.M5, Tile.M6,
        Tile.P1, Tile.P2, Tile.P3,
        Tile.RED, Tile.RED, Tile.RED,
        Tile.WHITE, Tile.WHITE
    ]

    for tile in tiles:
        hand.add_tile(tile)

    context = HandContext(win_method=WinMethod.RON)

    result = detect_yakuhai(hand, context)

    assert Yaku.DRAGON_YAKUHAI in result

def make_toitoi_hand():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M1, Tile.M1,
        Tile.M5, Tile.M5, Tile.M5,
        Tile.P3, Tile.P3, Tile.P3,
        Tile.S7, Tile.S7, Tile.S7,
        Tile.EAST, Tile.EAST
    ]

    for tile in tiles:
        hand.add_tile(tile)

    return hand

def test_is_toitoi():
    hand = make_toitoi_hand()
    assert is_toitoi(hand) is True

def test_is_not_toitoi_with_sequences():
    hand = make_tanyao_hand()
    assert is_toitoi(hand) is False

def test_detect_toitoi():
    hand = make_toitoi_hand()
    context = HandContext(win_method=WinMethod.RON)

    result = detect_yaku(hand, context)

    assert Yaku.TOITOI in result

def test_toitoi_with_open_pon():
    from mahjong_helper.meld import Meld, MeldType

    hand = Hand()

    meld = Meld(
        [Tile.M1, Tile.M1, Tile.M1],
        MeldType.PON
    )
    hand.add_meld(meld)

    tiles = [
        Tile.M5, Tile.M5, Tile.M5,
        Tile.P3, Tile.P3, Tile.P3,
        Tile.S7, Tile.S7, Tile.S7,
        Tile.EAST, Tile.EAST
    ]

    for tile in tiles:
        hand.add_tile(tile)

    assert is_toitoi(hand) is True

def make_honitsu_hand():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M2, Tile.M3,
        Tile.M4, Tile.M5, Tile.M6,
        Tile.M7, Tile.M8, Tile.M9,
        Tile.EAST, Tile.EAST, Tile.EAST,
        Tile.WHITE, Tile.WHITE
    ]

    for tile in tiles:
        hand.add_tile(tile)

    return hand

def make_chinitsu_hand():
    hand = Hand()

    tiles = [
        Tile.M1, Tile.M2, Tile.M3,
        Tile.M4, Tile.M5, Tile.M6,
        Tile.M7, Tile.M8, Tile.M9,
        Tile.M2, Tile.M3, Tile.M4,
        Tile.M5, Tile.M5
    ]

    for tile in tiles:
        hand.add_tile(tile)

    return hand

def test_is_honitsu():
    hand = make_honitsu_hand()
    assert is_honitsu(hand) is True

def test_is_not_honitsu_without_honours():
    hand = make_chinitsu_hand()
    assert is_honitsu(hand) is False

def test_is_chinitsu():
    hand = make_chinitsu_hand()
    assert is_chinitsu(hand) is True

def test_is_not_chinitsu_with_honours():
    hand = make_honitsu_hand()
    assert is_chinitsu(hand) is False

def test_detect_honitsu():
    hand = make_honitsu_hand()
    context = HandContext(win_method=WinMethod.RON)

    assert Yaku.HONITSU in detect_yaku(hand, context)

def test_detect_chinitsu():
    hand = make_chinitsu_hand()
    context = HandContext(win_method=WinMethod.RON)

    assert Yaku.CHINITSU in detect_yaku(hand, context)

def make_hand(tiles):
    hand = Hand()
    for tile in tiles:
        hand.add_tile(tile)
    return hand

def test_chanta():
    hand = make_hand([
        Tile.M1, Tile.M2, Tile.M3,
        Tile.P7, Tile.P8, Tile.P9,
        Tile.S1, Tile.S1, Tile.S1,
        Tile.EAST, Tile.EAST, Tile.EAST,
        Tile.WHITE, Tile.WHITE
    ])
    assert is_chanta(hand) is True

def test_junchan():
    hand = make_hand([
        Tile.M1, Tile.M2, Tile.M3,
        Tile.P7, Tile.P8, Tile.P9,
        Tile.S1, Tile.S1, Tile.S1,
        Tile.M9, Tile.M9, Tile.M9,
        Tile.P1, Tile.P1
    ])
    assert is_junchan(hand) is True

def test_iipeikou():
    hand = make_hand([
        Tile.M1, Tile.M2, Tile.M3,
        Tile.M1, Tile.M2, Tile.M3,
        Tile.P4, Tile.P5, Tile.P6,
        Tile.S7, Tile.S8, Tile.S9,
        Tile.EAST, Tile.EAST
    ])
    assert is_iipeikou(hand) is True

def test_ryanpeikou():
    hand = make_hand([
        Tile.M1, Tile.M2, Tile.M3,
        Tile.M1, Tile.M2, Tile.M3,
        Tile.P4, Tile.P5, Tile.P6,
        Tile.P4, Tile.P5, Tile.P6,
        Tile.EAST, Tile.EAST
    ])
    assert is_ryanpeikou(hand) is True
    assert is_iipeikou(hand) is False

def test_sanshoku_doujun():
    hand = make_hand([
        Tile.M1, Tile.M2, Tile.M3,
        Tile.P1, Tile.P2, Tile.P3,
        Tile.S1, Tile.S2, Tile.S3,
        Tile.M4, Tile.M5, Tile.M6,
        Tile.EAST, Tile.EAST
    ])
    assert is_sanshoku_doujun(hand) is True

def test_ittsu():
    hand = make_hand([
        Tile.M1, Tile.M2, Tile.M3,
        Tile.M4, Tile.M5, Tile.M6,
        Tile.M7, Tile.M8, Tile.M9,
        Tile.P1, Tile.P2, Tile.P3,
        Tile.EAST, Tile.EAST
    ])
    assert is_ittsu(hand) is True

def test_sanshoku_doukou():
    hand = make_hand([
        Tile.M5, Tile.M5, Tile.M5,
        Tile.P5, Tile.P5, Tile.P5,
        Tile.S5, Tile.S5, Tile.S5,
        Tile.EAST, Tile.EAST, Tile.EAST,
        Tile.WHITE, Tile.WHITE
    ])
    assert is_sanshoku_doukou(hand) is True

def make_honroutou_hand():
    return make_hand([
        Tile.M1, Tile.M1, Tile.M1,
        Tile.P9, Tile.P9, Tile.P9,
        Tile.S1, Tile.S1, Tile.S1,
        Tile.EAST, Tile.EAST, Tile.EAST,
        Tile.WHITE, Tile.WHITE
    ])

def test_honroutou():
    assert is_honroutou(make_honroutou_hand()) is True

def test_honroutou_chiitoitsu():
    hand = make_hand([
        Tile.M1, Tile.M1,
        Tile.M9, Tile.M9,
        Tile.P1, Tile.P1,
        Tile.P9, Tile.P9,
        Tile.S1, Tile.S1,
        Tile.EAST, Tile.EAST,
        Tile.WHITE, Tile.WHITE
    ])

    assert is_honroutou(hand) is True

def test_honroutou_rejects_simple_tiles():
    hand = make_hand([
        Tile.M1, Tile.M1, Tile.M1,
        Tile.P9, Tile.P9, Tile.P9,
        Tile.S1, Tile.S1, Tile.S1,
        Tile.EAST, Tile.EAST, Tile.EAST,
        Tile.M2, Tile.M2
    ])

    assert is_honroutou(hand) is False

def test_detect_honroutou():
    hand = make_honroutou_hand()
    context = HandContext(win_method=WinMethod.RON)

    assert Yaku.HONROUTOU in detect_yaku(hand, context)

def make_shousangen_hand():
    return make_hand([
        Tile.WHITE, Tile.WHITE, Tile.WHITE,
        Tile.RED, Tile.RED, Tile.RED,
        Tile.GREEN, Tile.GREEN,
        Tile.M1, Tile.M2, Tile.M3,
        Tile.P4, Tile.P5, Tile.P6
    ])

def test_shousangen():
    assert is_shousangen(make_shousangen_hand()) is True

def test_shousangen_rejects_one_dragon_triplet():
    hand = make_hand([
        Tile.WHITE, Tile.WHITE, Tile.WHITE,
        Tile.GREEN, Tile.GREEN,
        Tile.M1, Tile.M2, Tile.M3,
        Tile.P4, Tile.P5, Tile.P6,
        Tile.S1, Tile.S2, Tile.S3
    ])

    assert is_shousangen(hand) is False

def test_detect_shousangen():
    hand = make_shousangen_hand()
    context = HandContext(win_method=WinMethod.RON)

    assert Yaku.SHOUSANGEN in detect_yaku(hand, context)

def make_sanankou_hand():
    return make_hand([
        Tile.M1, Tile.M1, Tile.M1,
        Tile.P2, Tile.P2, Tile.P2,
        Tile.S3, Tile.S3, Tile.S3,
        Tile.M4, Tile.M5, Tile.M6,
        Tile.EAST, Tile.EAST
    ])

def test_sanankou_tsumo():
    hand = make_sanankou_hand()

    context = HandContext(
        win_method=WinMethod.TSUMO,
        winning_tile=Tile.M1
    )

    assert is_sanankou(hand, context) is True

def test_sanankou_ron_on_pair():
    hand = make_sanankou_hand()

    context = HandContext(
        win_method=WinMethod.RON,
        winning_tile=Tile.EAST
    )

    assert is_sanankou(hand, context) is True

def test_sanankou_ron_completing_triplet():
    hand = make_sanankou_hand()

    context = HandContext(
        win_method=WinMethod.RON,
        winning_tile=Tile.M1
    )

    assert is_sanankou(hand, context) is False

def test_sanankou_requires_winning_tile_for_ron():
    hand = make_sanankou_hand()

    context = HandContext(win_method=WinMethod.RON)

    assert is_sanankou(hand, context) is False

def test_detect_sanankou():
    hand = make_sanankou_hand()

    context = HandContext(
        win_method=WinMethod.TSUMO,
        winning_tile=Tile.M1
    )

    assert Yaku.SANANKOU in detect_yaku(hand, context)

def make_sankantsu_hand():
    hand = Hand()

    kans = [
        [Tile.M1] * 4,
        [Tile.P2] * 4,
        [Tile.S3] * 4
    ]

    for tiles in kans:
        hand.add_meld(Meld(tiles, MeldType.KAN))

    concealed_tiles = [
        Tile.M4, Tile.M5, Tile.M6,
        Tile.EAST, Tile.EAST
    ]

    for tile in concealed_tiles:
        hand.add_tile(tile)

    return hand

def test_sankantsu():
    hand = make_sankantsu_hand()

    assert is_sankantsu(hand) is True

def test_sankantsu_requires_three_kans():
    hand = Hand()

    hand.add_meld(
        Meld([Tile.M1] * 4, MeldType.KAN)
    )
    hand.add_meld(
        Meld([Tile.P2] * 4, MeldType.KAN)
    )

    assert is_sankantsu(hand) is False

def test_detect_sankantsu():
    hand = make_sankantsu_hand()
    context = HandContext(win_method=WinMethod.RON)

    assert Yaku.SANKANTSU in detect_yaku(hand, context)

def make_pinfu_hand():
    return make_hand([
        Tile.M1, Tile.M2, Tile.M3,
        Tile.M4, Tile.M5, Tile.M6,
        Tile.P2, Tile.P3, Tile.P4,
        Tile.S6, Tile.S7, Tile.S8,
        Tile.P5, Tile.P5
    ])

def test_pinfu_two_sided_wait():
    hand = make_pinfu_hand()

    context = HandContext(
        win_method=WinMethod.RON,
        winning_tile=Tile.P2,
        seat_wind=Tile.EAST,
        round_wind=Tile.SOUTH
    )

    assert is_pinfu(hand, context) is True

def test_pinfu_rejects_closed_wait():
    hand = make_pinfu_hand()

    context = HandContext(
        win_method=WinMethod.RON,
        winning_tile=Tile.P3,
        seat_wind=Tile.EAST,
        round_wind=Tile.SOUTH
    )

    assert is_pinfu(hand, context) is False

def test_pinfu_rejects_edge_wait():
    hand = make_pinfu_hand()

    context = HandContext(
        win_method=WinMethod.RON,
        winning_tile=Tile.M3,
        seat_wind=Tile.EAST,
        round_wind=Tile.SOUTH
    )

    assert is_pinfu(hand, context) is False

def test_pinfu_rejects_dragon_pair():
    hand = make_hand([
        Tile.M1, Tile.M2, Tile.M3,
        Tile.M4, Tile.M5, Tile.M6,
        Tile.P2, Tile.P3, Tile.P4,
        Tile.S6, Tile.S7, Tile.S8,
        Tile.WHITE, Tile.WHITE
    ])

    context = HandContext(
        win_method=WinMethod.RON,
        winning_tile=Tile.P2,
        seat_wind=Tile.EAST,
        round_wind=Tile.SOUTH
    )

    assert is_pinfu(hand, context) is False

def test_pinfu_requires_winning_tile():
    hand = make_pinfu_hand()

    context = HandContext(
        win_method=WinMethod.RON,
        seat_wind=Tile.EAST,
        round_wind=Tile.SOUTH
    )

    assert is_pinfu(hand, context) is False

def test_detect_pinfu():
    hand = make_pinfu_hand()

    context = HandContext(
        win_method=WinMethod.RON,
        winning_tile=Tile.P2,
        seat_wind=Tile.EAST,
        round_wind=Tile.SOUTH
    )

    assert Yaku.PINFU in detect_yaku(hand, context)

def make_daisuushi_hand():
    hand = Hand()

    for tile in (
        Tile.NORTH,
        Tile.EAST,
        Tile.SOUTH,
        Tile.WEST
    ):
        for _ in range(3):
            hand.add_tile(tile)

    hand.add_tile(Tile.M1)
    hand.add_tile(Tile.M1)

    return hand

def test_daisuushi():
    hand = make_daisuushi_hand()
    assert is_daisuushi(hand)

def test_detect_daisuushi():
    hand = make_daisuushi_hand()
    context = HandContext(win_method=WinMethod.TSUMO)

    assert Yaku.DAISUUSHI in detect_yaku(hand, context)

def test_tenhou():
    hand = make_tanyao_hand()
    context = HandContext(
        win_method=WinMethod.TSUMO,
        tenhou=True
    )

    assert is_tenhou(hand, context)

def test_chiihou():
    hand = make_tanyao_hand()
    context = HandContext(
        win_method=WinMethod.TSUMO,
        chiihou=True
    )

    assert is_chiihou(hand, context)

def test_tenhou_rejects_ron():
    hand = make_tanyao_hand()
    context = HandContext(
        win_method=WinMethod.RON,
        tenhou=True
    )

    assert not is_tenhou(hand, context)

def test_chiihou_rejects_ron():
    hand = make_tanyao_hand()
    context = HandContext(
        win_method=WinMethod.RON,
        chiihou=True
    )

    assert not is_chiihou(hand, context)
