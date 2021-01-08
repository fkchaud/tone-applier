from datetime import datetime
from typing import NoReturn

from django.http import HttpResponse

from divine_office.connect import get_liturgy
from divine_office.models import (
    Text,
    Verse,
)
from lilypond.builder import (
    build_file,
    get_lilydata_for_pair,
)


# Create your views here.
def index(request):
    today = datetime.now()
    liturgy = get_liturgy(today, 'visperas')
    file_idx = 0

    for chant in liturgy.chants:
        build_chant(chant, f"file_{file_idx}.ly")
        file_idx += 1

    return HttpResponse("Holis")


# temp here, move me
def build_pairs(lines: list[Verse]) -> list[list[Verse]]:
    pairs = []
    for i in range(0, len(lines) - 1, 2):
        pairs.append([lines[i], lines[i + 1]])

    if lines[-1] not in pairs[-1]:
        pairs[-1].append(lines[-1])
    return pairs


def build_chant(chant: Text, file_path: str) -> NoReturn:
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
        file_path=file_path,
    )
