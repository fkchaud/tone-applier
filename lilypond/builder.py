from typing import NoReturn

from divine_office.models import Verse
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


def get_lilydata_for_pair(pair: list[Verse], tone: str) -> dict[str, str]:
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
