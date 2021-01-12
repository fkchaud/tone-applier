from glob import glob
from subprocess import run
from typing import NoReturn

from divine_office.models import (
  Text,
  Verse,
)
from lilypond.lyrics import get_lyrics
from lilypond.notes import get_notes


DEFAULT_FILE_PATH = "file.ly"


DEFAULT_FILE_CONTENT = """
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


def build_file(
    notes: str,
    lyrics: str,
    title: str = "",
    subtitle: str = "",
    file_path: str = None,
) -> NoReturn:
    if file_path is None:
        file_path = DEFAULT_FILE_PATH

    notes = """
    \\cadenzaOff
    \\cadenzaOn
    """.join(notes)
    lyrics = " ".join(lyrics)

    final_content = DEFAULT_FILE_CONTENT.format(
        title=title,
        subtitle=subtitle,
        notes=notes,
        lyrics=lyrics,
    )
    encoded_content = final_content.encode("utf8")

    f = open(file_path, "wb")
    f.write(encoded_content)
    f.close()


def get_lilydata_for_pair(pair: list[Verse], tone: str, is_first: bool) -> dict[str, str]:
    lines = get_notes(pair, tone, is_first)

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


def build_pairs(lines: list[Verse]) -> list[list[Verse]]:
    pairs = []
    for i in range(0, len(lines) - 1, 2):
        pairs.append([lines[i], lines[i + 1]])

    if lines[-1] not in pairs[-1]:
        pairs[-1].append(lines[-1])
    return pairs


def build_chant(chant: Text, file_path: str, tone: str) -> dict:
    notes = []
    lyrics = []

    # not sure if it's per chant or per paragraph
    # if it's per paragraph, move inside the for
    is_first = True
    for paragraph in chant.paragraphs:
        pairs = build_pairs(paragraph.verses)

        for pair in pairs:
            lilydata = get_lilydata_for_pair(pair, tone, is_first)
            notes.append(lilydata["notes"])
            lyrics.append(lilydata["lyrics"])
            is_first = False

    build_file(
        notes,
        lyrics,
        title=chant.title,
        subtitle=chant.subtitle,
        file_path=file_path,
    )

    run(['lilypond', '--png', '-o', 'statics', file_path], check=True)
    file_path_no_ext = file_path.rsplit('.')[0]

    pngs = [
      file.replace('statics\\', '')
      for file in glob(f'statics/{file_path_no_ext}*.png')
    ]
    return {
      'files': pngs,
    }
