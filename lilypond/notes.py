from divine_office.models import Verse
from lilypond.tones import TONES


def get_notes(pair: tuple[Verse], tone: str, is_first: bool = False) -> list[str]:
    if len(pair) == 3:
        first_line = get_line_notes(pair[0], "flexa", tone, is_first)
        second_line = get_line_notes(pair[1], "cadenza_med", tone)
        third_line = get_line_notes(pair[2], "cadenza_fin", tone)
    else:
        first_line = get_line_notes(pair[0], "cadenza_med", tone, is_first)
        second_line = get_line_notes(pair[1], "cadenza_fin", tone)
        third_line = ""

    return [first_line, second_line, third_line]


VALID_ENDING_TYPES = ("flexa", "cadenza_med", "cadenza_fin")


def get_line_notes(
    verse: Verse,
    ending_type: str,
    tone: str,
    has_entonatio: bool = False,
) -> str:
    if ending_type not in VALID_ENDING_TYPES:
        raise ValueError("Not a valid ending type")

    tone_data = TONES[tone]
    verse_stress = verse.stress
    syllables = verse.syllables
    counts = {
        moment: values.count(' ') - values.count('(') + 1
        for moment, values in tone_data.items() if isinstance(values, str)
    }

    extra = ""
    if verse.text.endswith("Amén."):
        verse_stress = verse_stress[:-2]
        syllables = syllables[:-2]
        extra = f"""
        \\bar \"|\"
        {tone_data["amen"]}
        """

    opening = ""
    opening_count = 0
    if has_entonatio:
        opening = tone_data["entonatio"]
        opening_count = counts["entonatio"]

    ending = ""
    for stress, values in tone_data[ending_type].items():
        if verse_stress.endswith(stress):
            ending = values
            break
    ending_count = ending.count(' ') - ending.count('(') + 1

    tenor_count = len(syllables) - ending_count - opening_count
    tenor = ' '.join([tone_data["tenor"]] * tenor_count)

    line = opening + " " + tenor + " " + ending + extra + " |"

    return line
