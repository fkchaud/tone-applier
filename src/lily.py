file_path = "file.ly"

file_content = """
\\version "2.12.3"

stemOff = {{ \\hide Staff.Stem }}

\\relative c' {{
  \\clef "treble"
  \\key f \\major
  \\stemOff
  \\cadenzaOn
  {notes}
  \\cadenzaOff
}}

\\addlyrics {{
  {lyrics}
}}
"""

introito = "f4 g4"
introito_count = introito.count(' ') + 1
tenor = "a4"
# flexa = "g4"
cierre = "g4 a4 f2"
cierre_count = cierre.count(' ') + 1

syllables = ["Te", "di", "ré", "mi", "a", "mor,", "Rey", "mí", "o"]

lyrics = " ".join(syllables)

tenor_count = len(syllables) - introito_count - cierre_count

tenor_total = ' '.join([tenor] * tenor_count)

notes = f"{introito} {tenor_total} {cierre}"

final_content = file_content.format(notes=notes, lyrics=lyrics)
encoded_content = final_content.encode("utf8")

f = open(file_path, "wb")
f.write(encoded_content)
f.close()
