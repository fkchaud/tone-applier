from divine_office.models import Verse


SPEC_CHARS = (' ', ',', '.', '!', '?', '¡', '¿', ':', '-', ';', '«', '»')


def get_lyrics(pair: tuple[Verse]) -> str:
    lyrics = ""

    for verse in pair:
        low_text = verse.text.lower()
        normal_text = verse.text
        syllables = [s for s in verse.syllables]

        while normal_text:
            if normal_text[0] in SPEC_CHARS:
                lyrics += normal_text[0]
                normal_text = normal_text[1:]
                low_text = low_text[1:]
                continue

            syl = syllables[0]

            if low_text.startswith(syl):
                lyrics += normal_text[0: len(syl)]
                normal_text = normal_text[len(syl):]
                low_text = low_text[len(syl):]
                syllables.pop(0)

                if normal_text and normal_text[0] not in SPEC_CHARS:
                    lyrics += ' -- '

        lyrics += " "

    return lyrics
