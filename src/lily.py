DEFAULT_FILE_PATH = "file.ly"

file_content = """
\\version "2.12.3"

\\layout {{
  indent = #0
}}

stemOff = {{ \\hide Staff.Stem }}

\\relative c' {{
  \\clef "treble"
  \\key f \\major
  \\stemOff
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
    "flexa": "g4",
    "cadenza_med": {
        "0100": "g4 a4 f4 f2",
        "010": "g4 a4 f2",
        "01": "g4 a4( f2)",
    },
    "cadenza_fin": "f4 g4( a4) g4 f2",
    "cadenza_fin_stress": "0 0 1 0",
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
    first_line = get_first_line_notes(pair[0], tone)
    second_line = get_second_line_notes(pair[1], tone)

    return first_line, second_line


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


def get_second_line_notes(verse, tone):
    tone_data = TONES[tone]
    counts = {
        moment: values.count(' ') - values.count('(') + 1
        for moment, values in tone_data.items()
    }

    second_tenor_count = len(verse.syllables) - counts["cadenza_fin"]
    second_tenor = ' '.join([tone_data["tenor"]] * second_tenor_count)

    second_line = (
        second_tenor + " "
        + tone_data["cadenza_fin"]
    )
    return second_line


def get_lilydata_for_pair(pair, tone):
    first_line, second_line = get_notes(pair, tone)

    full_notes = f"""{first_line}
    \\bar \"|\"
    {second_line}
    \\bar \"|\"
    \\break"""

    lyrics = get_lyrics(pair)

    return {
        "notes": full_notes,
        "lyrics": lyrics,
    }


def build_file(notes, lyrics, file_path=None):
    if file_path is None:
        file_path = DEFAULT_FILE_PATH

    notes = """
    \\cadenzaOff
    \\cadenzaOn
    """.join(notes)
    lyrics = " ".join(lyrics)

    final_content = file_content.format(
        notes=notes,
        lyrics=lyrics,
    )
    encoded_content = final_content.encode("utf8")

    f = open(file_path, "wb")
    f.write(encoded_content)
    f.close()
