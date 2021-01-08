from typing import NoReturn

from syllable.connect import get_syllables


class Verse:
    text: str = ""
    syllables: list[str] = []
    stress: str = ""

    def __init__(self, text: str, syllables: list[str], stress: str):
        self.text = text
        self.syllables = syllables
        self.stress = stress

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return str(self)


class Paragraph:
    lines: list[str] = []
    syllables: list[str] = []
    stress: list[str] = []

    def __init__(self, contents: list[str]):
        self.lines = [" ".join(str(content).split()) for content in contents]
        self.syllables = []
        self.stress = []

    def __str__(self) -> str:
        return "\n".join(self.lines)

    def __repr__(self) -> str:
        return str(self)

    def add_syllable_verse(self, verse: list[str]) -> NoReturn:
        stress = [
            "1" if "strong" in syllable else "0"
            for syllable in verse
        ]
        self.stress.append("".join(stress))

        syllables_no_stress = [
            syllable.replace("<strong>", "").replace("</strong>", "")
            for syllable in verse
        ]
        self.syllables.append(syllables_no_stress)

    @property
    def verses(self) -> list[Verse]:
        if not hasattr(self, '_verses'):
            self._verses = [
                Verse(line, syllable, stress)
                for line, syllable, stress in zip(
                    self.lines,
                    self.syllables,
                    self.stress,
                )
            ]

        return self._verses


class Text:
    paragraphs: list[Paragraph] = []
    title: str = ""
    subtitle: str = ""

    def __init__(
        self,
        contents: list[str],
        title: str = "",
        subtitle: str = "",
    ):
        self.title = title.strip()
        self.subtitle = subtitle.strip()
        self.paragraphs = []

        br_count = 0

        lines_for_paragraph = []

        for content in contents:
            content = str(content)
            if content == '\n':
                continue

            if content == '<br/>':
                br_count += 1
            else:
                br_count = 0

            if br_count == 2:
                self.paragraphs.append(
                    Paragraph(lines_for_paragraph),
                )
                lines_for_paragraph.clear()
                continue

            if content != '<br/>':
                lines_for_paragraph.append(content)

            if "<font" in content:
                break

        syllables_set = get_syllables(str(self))
        syllables_index = 0

        for paragraph in self.paragraphs:
            for line in paragraph.lines:
                paragraph.add_syllable_verse(syllables_set[syllables_index])
                syllables_index += 1

    def __str__(self) -> str:
        return "\n\n".join(str(par) for par in self.paragraphs)

    def __repr__(self) -> str:
        return str(self)


class Liturgy:
    chants: list[Text] = []

    def __init__(self):
        self.chants = []
