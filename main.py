from datetime import datetime

from src.divine_office import get_liturgy
from src.lily import get_lilydata_for_pair, build_file


def build_pairs(lines):
    pairs = []
    for i in range(0, len(lines), 2):
        pairs.append((lines[i], lines[i + 1]))
    return pairs


today = datetime.now()
today = today.replace(day=4)
liturgy = get_liturgy(today, 'visperas')

notes = []
lyrics = []

for paragraph in liturgy.hymn.paragraphs:
    if len(paragraph.lines) % 2:
        print("I don't know how to parse this yet, sorry")
        break

    pairs = build_pairs(paragraph.verses)

    for pair in pairs:
        lilydata = get_lilydata_for_pair(pair, 'tone_6')
        notes.append(lilydata["notes"])
        lyrics.append(lilydata["lyrics"])

build_file(
    notes,
    lyrics,
    title=liturgy.hymn.title,
    subtitle="Himno",
    file_path="file_done.ly",
)
