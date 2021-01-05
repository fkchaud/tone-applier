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
    "cadenza_med": "g4 a4 f2",
    "cadenza_fin": "f4 g4( a4) g4 f2",
}

TONES = {
    'tone_6': TONE_6,
}


def remove_strong(syllables):
    return [
        [
            syl.replace("<strong>", "").replace("</strong>", "")
            for syl in syl_set
        ]
        for syl_set in syllables
    ]


def get_lilydata_for_pair(pair, tone):
    tone_data = TONES[tone]

    counts = {
        moment: values.count(' ') - values.count('(') + 1
        for moment, values in tone_data.items()
    }

    syllables = [
        line.syllables
        for line in pair
    ]
    syllables = remove_strong(syllables)

    first_tenor_count = (
        len(syllables[0])
        - counts["entonatio"]
        - counts["cadenza_med"]
    )
    first_tenor = ' '.join([tone_data["tenor"]] * first_tenor_count)

    first_line = (
        tone_data["entonatio"] + " "
        + first_tenor + " "
        + tone_data["cadenza_med"] + " |"
    )

    second_tenor_count = len(syllables[1]) - counts["cadenza_fin"]
    second_tenor = ' '.join([tone_data["tenor"]] * second_tenor_count)

    second_line = (
        second_tenor + " "
        + tone_data["cadenza_fin"]
    )

    full_notes = f"""{first_line}
    \\bar \"|\"
    \\cadenzaOff
    \\cadenzaOn
    {second_line}
    \\bar \"|\"
    \\break"""

    lyrics = " ".join(syllables[0]) + " " + " ".join(syllables[1])

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
