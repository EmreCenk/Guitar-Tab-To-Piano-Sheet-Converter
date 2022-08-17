from typing import *

class Note:
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

class Bar:
    def __init__(self, notes: List[Note]):
        self.notes = notes

class Piece:
    def __init__(self, bars: List[Bar]):
        self.bars = bars
        # self.time_signature = ...
        # todo: finding time signature and simplifying it is not as easy as it seems (i'm not even sure if time signature will be usefull at any point in time anyways)
