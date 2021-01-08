from unittest.mock import Mock

from django.test import TestCase

from lilypond.notes import (
    get_first_line_notes,
    get_second_line_notes,
)


class TestFirstLineNotes(TestCase):

    tone = 'tone_6'

    def test_aguda(self):
        verse = Mock(
            text='Oráculo del Señor a mi Señor:',
            syllables=['o', 'rá', 'cu', 'lo', 'del',
                       'se', 'ñor', 'a', 'mi', 'se', 'ñor'],
            stress="01000010001",
        )
        notes = get_first_line_notes(verse, self.tone)
        expected_notes = 'f4 g4 a4 a4 a4 a4 a4 a4 a4 g4 a4( f2) |'
        self.assertEqual(notes, expected_notes)

    def test_grave(self):
        verse = Mock(
            text='y haré de tus enemigos',
            syllables=['y', 'ha', 'ré', 'de', 'tus',
                       'e', 'ne', 'mi', 'gos'],
            stress="001000010",
        )
        notes = get_first_line_notes(verse, self.tone)
        expected_notes = 'f4 g4 a4 a4 a4 a4 g4 a4 f2 |'
        self.assertEqual(notes, expected_notes)

    def test_esdrujula(self):
        verse = Mock(
            text='Gloria al Padre, y al Hijo, y al Espíritu',
            syllables=['glo', 'ria', 'al', 'pa', 'dre', 'y',
                       'al', 'hi', 'jo', 'y', 'al', 'es', 'pí', 'ri', 'tu'],
            stress="100100010000100",
        )
        notes = get_first_line_notes(verse, self.tone)
        expected_notes = 'f4 g4 a4 a4 a4 a4 a4 a4 a4 a4 a4 g4 a4 f4 f2 |'
        self.assertEqual(notes, expected_notes)


class TestSecondLineNotes(TestCase):

    tone = 'tone_6'

    def test_aguda(self):
        verse = Mock(
            text='Oráculo del Señor a mi Señor:',
            syllables=['o', 'rá', 'cu', 'lo', 'del',
                       'se', 'ñor', 'a', 'mi', 'se', 'ñor'],
            stress="01000010001",
        )
        notes = get_second_line_notes(verse, self.tone)
        expected_notes = 'a4 a4 a4 a4 a4 a4 a4 a4 f4 g4( a4) g4( f2)'
        self.assertEqual(notes, expected_notes)

    def test_grave(self):
        verse = Mock(
            text='y haré de tus enemigos',
            syllables=['y', 'ha', 'ré', 'de', 'tus',
                       'e', 'ne', 'mi', 'gos'],
            stress="001000010",
        )
        notes = get_second_line_notes(verse, self.tone)
        expected_notes = 'a4 a4 a4 a4 a4 f4 g4( a4) g4 f2'
        self.assertEqual(notes, expected_notes)

    def test_esdrujula(self):
        verse = Mock(
            text='Gloria al Padre, y al Hijo, y al Espíritu',
            syllables=['glo', 'ria', 'al', 'pa', 'dre', 'y',
                       'al', 'hi', 'jo', 'y', 'al', 'es', 'pí', 'ri', 'tu'],
            stress="100100010000100",
        )
        notes = get_second_line_notes(verse, self.tone)
        expected_notes = 'a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 f4 g4( a4) g4 f4 f2'
        self.assertEqual(notes, expected_notes)
