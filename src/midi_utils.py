

from typing import*

from src.midi import MIDICreator
from src.MusicAbstractions import Piece


def merge_identical_ids(piece: Piece):
    pass

def convert_multiple_pieces_to_midi(pieces: List[Piece], file_name_to_save: str):

    midi = MIDICreator(pieces[0].tempo_bpm)
    time_displacement_due_to_rests = 0
    for j in range(len(pieces)):
        current_time = 0
        for i in range(len(pieces[j].bars)):
            for a in pieces[j].bars[i].notes:
                for n in a:
                    if n.note == -1:
                        time_displacement_due_to_rests += n.beat_length
                    else:
                        midi.add_note(n.note + 20, current_time + time_displacement_due_to_rests, n.beat_length, track_num=j) #the +20 is there to convert the piano number to midi number
                current_time += a[0].beat_length
    midi.save(file_name_to_save)
    return midi