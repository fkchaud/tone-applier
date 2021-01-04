from datetime import datetime

from src.syllable import get_syllables
from src.divine_office import get_liturgy

text = (
    'Como era en el principio, ahora y siempre, '
    'por los siglos de los siglos. Amén.'
)

syllables = get_syllables(text)
print(syllables)

today = datetime.now()
today = today.replace(day=3)
print(get_liturgy(today, 'visperas'))
