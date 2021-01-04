import requests
from bs4 import BeautifulSoup

url = 'https://www.separarensilabas.com/'
user_agent = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
)
headers = {'User-Agent': user_agent}

body = {
    'fs': (
        'Como era en el principio, ahora y siempre, '
        'por los siglos de los siglos. Amén.'
    ),
}

title = "Separaci\\xc3\\xb3n de s\\xc3\\xadlabas gramatical"

response = requests.post(url, data=body, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')
tables = soup.find_all('table')
table = tables[1]  # second table
tds = table.find_all('td')
td = tds[0]

splitted_phrase = ""
for child in td.children:
    str_child = str(child)
    if '\n' in str_child:
        continue
    if 'gramatical' in str_child:
        continue
    if '<br/>' in str_child:
        break
    splitted_phrase += str_child

syllables = splitted_phrase.split('-')
print(syllables)
