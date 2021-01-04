import requests
from bs4 import BeautifulSoup


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


class Paragraph(object):
    lines = []

    def __init__(self, contents):
        self.lines = [" ".join(str(content).split()) for content in contents]

    def __str__(self):
        return "\n".join(self.lines)

    def __repr__(self):
        return str(self)


class Text(object):
    paragraphs = []

    def __init__(self, contents):
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

    def __str__(self):
        return "\n\n".join(str(par) for par in self.paragraphs)

    def __repr__(self):
        return str(self)


class Liturgy(object):
    hymn = []


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

    get_hymn = False
    for child in div.children:
        str_child = str(child)
        if '\n' == str_child:
            continue

        if get_hymn:
            lit.hymn = Text(child)
            get_hymn = False

        if 'Himno' in str_child:
            get_hymn = True

    return lit
