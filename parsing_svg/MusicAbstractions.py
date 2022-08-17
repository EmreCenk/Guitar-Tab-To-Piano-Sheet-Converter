from typing import *

class Note:
    def __init__(self, beat_length: int, note: int):
        """
        :param beat_length: How long the note lasts for
        :param note: which note to play
        Todo: figure out how you actually want to store a pitch (an integer should probably do?)
        """
        self.beat_length = beat_length
        self.note = note

class Bar:
    def __init__(self, notes: List[Note]):
        self.notes = notes

class Piece:
    def __init__(self, bars: List[Bar]):
        self.bars = bars
