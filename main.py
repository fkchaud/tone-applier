from datetime import datetime

from src.divine_office import get_liturgy
from src.lily import get_lilydata_for_pair, build_file
# from src.syllable import get_syllables


def build_pairs(lines):
    pairs = []
    for i in range(0, len(lines), 2):
        pairs.append((lines[i], lines[i + 1]))
    return pairs


today = datetime.now()
today = today.replace(day=4)
liturgy = get_liturgy(today, 'visperas')

idx = 0
for paragraph in liturgy.hymn.paragraphs:
    if len(paragraph.lines) % 2:
        print("I don't know how to parse this yet, sorry")
        break

    pairs = build_pairs(paragraph.lines)

    for pair in pairs:
        lilydata = get_lilydata_for_pair(pair, 'tone_6')
        build_file(lilydata, f"file_{idx}.ly")
        idx += 1
