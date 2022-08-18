from typing import *

class PianoNote:
    def __init__(self, beat_length: int, note: int):
        """
        :param beat_length: How long the note lasts for
        :param note: which note to play
        Todo: figure out how you actually want to store a pitch (an integer should probably do?)

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
            5: 5 + 15,
            4: 10 + 15,
            3: 15 + 15,
            2: 20 + 15,
            1: 24 + 15,
            0: 29 + 15, #middle E
        }


        return PianoNote(self.beat_length, guitar_string_index_to_piano_key[self.string_index] + self.fret_number)

class Bar:
    def __init__(self, notes: List[PianoNote]):
        self.notes = notes

class Piece:
    def __init__(self, bars: List[Bar]):
        self.bars = bars
        # self.time_signature = ...
        # todo: finding time signature and simplifying it is not as easy as it seems (i'm not even sure if time signature will be usefull at any point in time anyways)
