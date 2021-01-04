from src.syllable import get_syllables

text = (
    'Como era en el principio, ahora y siempre, '
    'por los siglos de los siglos. Amén.'
)

syllables = get_syllables(text)
print(syllables)
