from divine_office.models import Verse
from lilypond.tones import TONES


def get_notes(pair: tuple[Verse], tone: str) -> list[str]:
    if len(pair) == 3:
        first_line = get_line_with_flexa(pair[0], tone)
        second_line = get_line_med_notes(pair[1], tone)
        third_line = get_second_line_notes(pair[2], tone)
    else:
        first_line = get_first_line_notes(pair[0], tone)
        second_line = get_second_line_notes(pair[1], tone)
        third_line = ""

    return [first_line, second_line, third_line]


def get_line_with_flexa(verse: Verse, tone: str) -> str:
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


def get_first_line_notes(verse: Verse, tone: str) -> str:
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


def get_line_med_notes(verse: Verse, tone: str) -> str:
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


def get_second_line_notes(verse: Verse, tone: str) -> str:
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
