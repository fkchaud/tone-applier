import requests
from bs4 import BeautifulSoup

from .syllable import get_syllables


base_url = 'https://liturgiadelashoras.github.io/sync'
user_agent = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
)
headers = {'User-Agent': user_agent}

month_map = {
    1: 'ene',
    2: 'feb',
    3: 'mar',
    4: 'abr',
    5: 'may',
    6: 'jun',
    7: 'jul',
    8: 'ago',
    9: 'sep',
    10: 'oct',
    11: 'nov',
    12: 'dec',
}


class Verse(object):
    text = ""
    syllables = []
    stress = []

    def __init__(self, text, syllables, stress):
        self.text = text
        self.syllables = syllables
        self.stress = stress

    def __str__(self):
        return self.text

    def __repr__(self):
        return str(self)


class Paragraph(object):
    lines = []
    syllables = []
    stress = []

    def __init__(self, contents):
        self.lines = [" ".join(str(content).split()) for content in contents]
        self.syllables = []
        self.stress = []

    def __str__(self):
        return "\n".join(self.lines)

    def __repr__(self):
        return str(self)

    def add_syllable_verse(self, verse):
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
    def verses(self):
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


class Text(object):
    paragraphs = []
    title = ""
    subtitle = ""

    def __init__(self, contents, title="", subtitle=""):
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

        syllables_set = get_syllables(str(self))
        syllables_index = 0

        for paragraph in self.paragraphs:
            for line in paragraph.lines:
                paragraph.add_syllable_verse(syllables_set[syllables_index])
                syllables_index += 1

    def __str__(self):
        return "\n\n".join(str(par) for par in self.paragraphs)

    def __repr__(self):
        return str(self)


class Liturgy(object):
    chants = []

    def __init__(self):
        self.chants = []


def get_date_url(date):
    year = date.year
    month = month_map[date.month]
    day = str(date.day).zfill(2)

    url = f'{base_url}/{year}/{month}/{day}'
    return url


def get_liturgy(date, liturgy):
    url = get_date_url(date)
    url = f'{url}/{liturgy}.htm'

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find_all('div')[1]

    lit = Liturgy()

    get_chant = False
    chant_title = ""
    chant_subtitle = ""
    for child in div.children:
        str_child = str(child)
        if '\n' == str_child:
            continue

        if get_chant:
            lit.chants.append(
                Text(child, chant_title, chant_subtitle),
            )
            get_chant = False

        if 'Himno' in str_child:
            get_chant = True
            chant_subtitle, chant_title = child.text.split(": ")

        elif 'Salmo' in str_child:
            get_chant = True
            if " - " in str_child:
                chant_subtitle, chant_title = child.text.split(" - ")
            else:
                chant_subtitle = chant_title = child.text

        elif 'EVANGÉLICO' in str_child:
            # todo
            pass

        elif 'ntico' in str_child:
            get_chant = True
            first, second = child.text.split(": ")
            chant_title, versicle = second.split(" - ")
            chant_subtitle = f"Cántico - {versicle}"

    return lit
