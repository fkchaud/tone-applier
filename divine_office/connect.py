from datetime import date

import requests
from bs4 import BeautifulSoup

from divine_office.models import (
    Liturgy,
    Text,
)


BASE_URL = 'https://liturgiadelashoras.github.io/sync'
USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
)
HEADERS = {'User-Agent': USER_AGENT}

MONTH_MAP = {
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


def _get_date_url(date: date) -> str:
    year = date.year
    month = MONTH_MAP[date.month]
    day = str(date.day).zfill(2)

    url = f'{BASE_URL}/{year}/{month}/{day}'
    return url


def get_liturgy(date: date, liturgy: str) -> Liturgy:
    url = _get_date_url(date)
    url = f'{url}/{liturgy}.htm'

    response = requests.get(url, headers=HEADERS)

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
            # todo
            pass
            # get_chant = True
            # first, second = child.text.split(": ")
            # chant_title, versicle = second.split(" - ")
            # chant_subtitle = f"Cántico - {versicle}"

    return lit
