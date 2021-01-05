import requests
from bs4 import BeautifulSoup


url = 'https://www.separarensilabas.com/'
user_agent = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
)
headers = {'User-Agent': user_agent}


def fetch_syllable(text):
    body = {
        'fs': text,
        'vec': 'on',
    }

    response = requests.post(url, data=body, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    divs = soup.find_all('div', class_="g--third")
    div = divs[1]  # second column
    return div


def get_syllables(text):
    div = fetch_syllable(text)

    lines = []
    splitted_phrase = ""
    for child in div.children:
        str_child = str(child)
        if '\n' in str_child:
            continue
        if 'gramatical' in str_child:
            continue
        if '<br/>' in str_child:
            if splitted_phrase:
                lines.append(splitted_phrase)
            splitted_phrase = ""
            continue

        splitted_phrase += str_child

    syllables = [line.split('-') for line in lines]
    return syllables
