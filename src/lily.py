DEFAULT_FILE_PATH = "file.ly"

file_content = """
\\version "2.12.3"

\\header {{
  title = "{title}"
  subtitle = "{subtitle}"
}}

\\layout {{
  indent = #0
}}

stemOff = {{ \\hide Staff.Stem }}

\\relative c' {{
  \\clef "treble"
  \\key f \\major
  \\stemOff
  \\omit Score.TimeSignature
  \\cadenzaOn
  {notes}
  \\cadenzaOff
}}

\\addlyrics {{
  {lyrics}
}}
"""

TONE_6 = {
    "entonatio": "f4 g4",
    "tenor": "a4",
    "flexa": {
        "100": "a4 g4 g2",
        "10": "a4 g2",
        "1": "a4( g2)",
    },
    "cadenza_med": {
        "100": "g4 a4 f4 f2",
        "10": "g4 a4 f2",
        "1": "g4 a4( f2)",
    },
    "cadenza_fin": {
        "100": "f4 g4( a4) g4 f4 f2",
        "10": "f4 g4( a4) g4 f2",
        "1": "f4 g4( a4) g4( f2)",
    },
    "amen": "d2 f2",
}

TONES = {
    'tone_6': TONE_6,
}

SPEC_CHARS = (' ', ',', '.', '!', '?', '¡', '¿')


def get_lyrics(pair):
    lyrics = ""

    for verse in pair:
        low_text = verse.text.lower()
        syllables = [s for s in verse.syllables]

        for i in range(len(verse.text)):
            first_syllable = syllables[0]

            if i == 0 and verse.text[i] in SPEC_CHARS:
                lyrics += verse.text[i]
                continue

            if not low_text[i: i + len(first_syllable)] == first_syllable:
                continue

            lyrics += verse.text[i: i + len(first_syllable)]

            # overflow
            if i + len(first_syllable) >= len(verse.text):
                break

            next_char = low_text[i + len(first_syllable)]
            if next_char in SPEC_CHARS:
                for char in low_text[i + len(first_syllable):]:
                    if char not in SPEC_CHARS:
                        break
                    lyrics += char
            else:
                lyrics += ' -- '

            syllables.pop(0)

            if not syllables:
                break

        lyrics += " "

    return lyrics


def get_notes(pair, tone):
    if len(pair) == 3:
        first_line = get_line_with_flexa(pair[0], tone)
        second_line = get_line_med_notes(pair[1], tone)
        third_line = get_second_line_notes(pair[2], tone)
    else:
        first_line = get_first_line_notes(pair[0], tone)
        second_line = get_second_line_notes(pair[1], tone)
        third_line = ""

    return [first_line, second_line, third_line]


def get_line_with_flexa(verse, tone):
    tone_data = TONES[tone]
    counts = {
        moment: values.count(' ') - values.count('(') + 1
        for moment, values in tone_data.items() if isinstance(values, str)
    }

    flexa = ""
    for stress, values in tone_data["flexa"].items():
        if verse.stress.endswith(stress):
            flexa = values
            break
    flexa_count = flexa.count(' ') - flexa.count('(') + 1

    tenor_count = (
        len(verse.syllables)
        - counts["entonatio"]
        - flexa_count
    )
    tenor = ' '.join([tone_data["tenor"]] * tenor_count)

    line = (
        tone_data["entonatio"] + " "
        + tenor + " "
        + flexa + " |"
    )

    return line


def get_first_line_notes(verse, tone):
    tone_data = TONES[tone]
    counts = {
        moment: values.count(' ') - values.count('(') + 1
        for moment, values in tone_data.items() if isinstance(values, str)
    }

    cadenza = ""
    for stress, values in tone_data["cadenza_med"].items():
        if verse.stress.endswith(stress):
            cadenza = values
            break
    cadenza_count = cadenza.count(' ') - cadenza.count('(') + 1

    first_tenor_count = (
        len(verse.syllables)
        - counts["entonatio"]
        - cadenza_count
    )
    first_tenor = ' '.join([tone_data["tenor"]] * first_tenor_count)

    first_line = (
        tone_data["entonatio"] + " "
        + first_tenor + " "
        + cadenza + " |"
    )

    return first_line


def get_line_med_notes(verse, tone):
    tone_data = TONES[tone]

    cadenza = ""
    for stress, values in tone_data["cadenza_med"].items():
        if verse.stress.endswith(stress):
            cadenza = values
            break
    cadenza_count = cadenza.count(' ') - cadenza.count('(') + 1

    tenor_count = (
        len(verse.syllables)
        - cadenza_count
    )
    tenor = ' '.join([tone_data["tenor"]] * tenor_count)

    line = (
        tenor + " "
        + cadenza + " |"
    )

    return line


def get_second_line_notes(verse, tone):
    tone_data = TONES[tone]
    verse_stress = verse.stress
    syllables = verse.syllables
    extra = ""

    if verse.text.endswith("Amén."):
        verse_stress = verse_stress[:-2]
        syllables = syllables[:-2]
        extra = f"""
        \\bar \"|\"
        {tone_data["amen"]}
        """

    cadenza = ""
    for stress, values in tone_data["cadenza_fin"].items():
        if verse_stress.endswith(stress):
            cadenza = values
            break
    cadenza_count = cadenza.count(' ') - cadenza.count('(') + 1

    second_tenor_count = len(syllables) - cadenza_count
    second_tenor = ' '.join([tone_data["tenor"]] * second_tenor_count)

    second_line = second_tenor + " " + cadenza + extra
    return second_line


def get_lilydata_for_pair(pair, tone):
    lines = get_notes(pair, tone)

    joined_lines = """
    \\bar \"|\"
    """.join(lines)

    full_notes = f"""{joined_lines}
    \\bar \"|\"
    \\break"""

    lyrics = get_lyrics(pair)

    return {
        "notes": full_notes,
        "lyrics": lyrics,
    }


def build_file(notes, lyrics, title="", subtitle="", file_path=None):
    if file_path is None:
        file_path = DEFAULT_FILE_PATH

    notes = """
    \\cadenzaOff
    \\cadenzaOn
    """.join(notes)
    lyrics = " ".join(lyrics)

    final_content = file_content.format(
        title=title,
        subtitle=subtitle,
        notes=notes,
        lyrics=lyrics,
    )
    encoded_content = final_content.encode("utf8")

    f = open(file_path, "wb")
    f.write(encoded_content)
    f.close()
