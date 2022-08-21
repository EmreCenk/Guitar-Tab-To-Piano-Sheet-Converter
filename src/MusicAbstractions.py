from typing import *
from src.midi import MIDICreator
class PianoNote:
    def __init__(self, beat_length: int, note: int):
        """
        :param beat_length: How long the note lasts for
        :param note: which note to play (a note of -1 indicates a rest)

        Note: Mapping notes to beat lengths is shown below:
        Whole note -> 4
        Half Note -> 2
        Quarter Note -> 1
        Eight Note -> 0.5
        Sixteenth Note -> 0.25
        As shown here: https://www.soundbrenner.com/wp-content/uploads/2020/09/note-values.png
        """
        self.beat_length = beat_length
        self.note = note

class GuitarTabNote:
    def __init__(self, beat_length: int, guitar_fret_number: int, guitar_string_index: int):
        self.beat_length = beat_length
        self.fret_number = guitar_fret_number
        self.string_index = guitar_string_index

    def convert_to_piano_note(self) -> PianoNote:
        """
        Returns a PianoNote object where the note is a number from 0-87 (for which key should be played)
        :return: PianoNote
        """

        # Used the following image to see how guitar strings convert to piano: https://www.get-tuned.com/images/tune-w-paino.png
        guitar_string_index_to_piano_key = { #maps fret number to which number key on the piano
            #source: https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
            #note: to convert to midi, just add 20 to the piano key number
            5: 5 + 15,
            4: 10 + 15,
            3: 15 + 15,
            2: 20 + 15,
            1: 24 + 15,
            0: 29 + 15, #middle E
        }



        return PianoNote(self.beat_length, guitar_string_index_to_piano_key[self.string_index] + self.fret_number)

class Bar:
    def __init__(self, notes: List[List[PianoNote]]):
        self.notes = notes

class Piece:
    def __init__(self, bars: List[Bar], tempo_bpm: int = 60):
        self.bars = bars
        self.tempo_bpm = tempo_bpm
        # self.time_signature = ...
        # todo: finding time signature and simplifying it is not as easy as it seems (i'm not even sure if time signature will be usefull at any point in time anyways)

    def save_as_midi(self, name_to_save: str) -> MIDICreator:
        from src.midi_utils import convert_multiple_pieces_to_midi

        midi = convert_multiple_pieces_to_midi([self], name_to_save)
        return midi