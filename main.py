from datetime import datetime

from src.divine_office import get_liturgy
from src.lily import get_lilydata_for_pair, build_file


def build_pairs(lines):
    pairs = []
    for i in range(0, len(lines) - 1, 2):
        pairs.append([lines[i], lines[i + 1]])

    if lines[-1] not in pairs[-1]:
        pairs[-1].append(lines[-1])
    return pairs


today = datetime.now()
liturgy = get_liturgy(today, 'visperas')
file_idx = 0


def build_chant(chant):
    notes = []
    lyrics = []

    for paragraph in chant.paragraphs:
        pairs = build_pairs(paragraph.verses)

        for pair in pairs:
            lilydata = get_lilydata_for_pair(pair, 'tone_6')
            notes.append(lilydata["notes"])
            lyrics.append(lilydata["lyrics"])

    build_file(
        notes,
        lyrics,
        title=chant.title,
        subtitle=chant.subtitle,
        file_path=f"file_{file_idx}.ly",
    )


for chant in liturgy.chants:
    build_chant(chant)
    file_idx += 1
