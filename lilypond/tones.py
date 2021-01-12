TONE_1Da = {
    "entonatio": "f'4 g'4( a'4)",
    "tenor": "a'4",
    "flexa": {
        "100": "a4 g4 g2",
        "10": "a4 g2",
        "1": "a4( g2)",
    },
    "cadenza_med": {
        "1000100": "bes'4 bes'4 bes'4 a'4 g'4 a'4 a'2",
        "100010": "bes'4 bes'4 bes'4 a'4 g'4 a'2",
        "10001": "bes'4 bes'4 bes'4 a'4 g'4( a'2)",
        "100100": "bes'4 bes'4 a'4 g'4 a'4 a'2",
        "10010": "bes'4 bes'4 a'4 g'4 a'2",
        "1001": "bes'4 bes'4 a'4 g'4( a'2)",
        "10100": "bes'4 a'4 g'4 a'4 a'2",
        "1010": "bes'4 a'4 g'4 a'2",
        "101": "bes'4 a'4 g'4( a'2)",
    },
    "cadenza_fin": {
        # 100 is it good?
        "100": "g'4 f'4 g'4 g'4( f'4) d'2",
        "10": "g'4 f'4 g'4( f'4) d'2",
        "1": "g'4 f'4 g'4( f'4)( d'2)",
    },
    "amen": "d'2 f'2",
}

TONE_6 = {
    "entonatio": "f'4 g'4",
    "tenor": "a'4",
    "flexa": {
        "100": "a'4 g'4 g'2",
        "10": "a'4 g'2",
        "1": "a'4( g'2)",
    },
    "cadenza_med": {
        "100": "g'4 a'4 f'4 f'2",
        "10": "g'4 a'4 f'2",
        "1": "g'4 a'4( f'2)",
    },
    "cadenza_fin": {
        "100": "f'4 g'4( a'4) g'4 f'4 f'2",
        "10": "f'4 g'4( a'4) g'4 f'2",
        "1": "f'4 g'4( a'4) g'4( f'2)",
    },
    "amen": "d'2 f'2",
}

TONE_2 = {
    "entonatio": "c'4 d'4",
    "tenor": "f'4",
    "flexa": {
        "100": "f'4 d'4 d'2",
        "10": "f'4 d'2",
        "1": "f'4( d'2)",
    },
    "cadenza_med": {
        "100": "g'4 f'4 f'2",
        "10": "g'4 f'2",
        "1": "g'4( f'2)",
    },
    "cadenza_fin": {
        "100": "e'4 c'4 d'4 d'2",
        "10": "e'4 c'4( d'4) d'2",
        "1": "e'4 c'4( d'2)",
    },
    "amen": "c'4( d'4) d'2",
}

TONES = {
    'tone_1da': TONE_1Da,
    'tone_2': TONE_2,
    'tone_6': TONE_6,
}
