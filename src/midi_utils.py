

from typing import*

from src.midi import MIDICreator
from src.MusicAbstractions import Piece, PianoNote, Bar

def find_index(array: List, elem: object):
    for i in range(len(array)):
        if array[i] == elem:
            return i
    return -1

def merge_identical_ids(piece: Piece) -> Piece:
    bars = [Bar([[PianoNote(1000, 1000, (float("inf"), float("inf")))]])]

    for i, bar in enumerate(piece.bars):
        print(i+1, "/", len(piece.bars))
        note_groups = [bars[-1].notes[-1]]
        # for asdf in note_groups: print("LA", len(asdf))

        print()
        for j in range(len(bar.notes)):
            print("bar.note:", j+1, "/", len(bar.notes))
            n_group = bar.notes[j]
            new_n_group = []

            for k, note in enumerate(n_group):
                print("n_group:", k+1, "/", len(n_group), f"will loop over length: {len(note_groups[j])}")

                for kk, previous_note in enumerate(note_groups[j]): #the i is i and not i-1 intentionally. (since we start with an empty list in note_groups)
                    if previous_note.coordinate == note.coordinate:
                        previous_note.beat_length += note.beat_length
                        # note_groups[j][kk] = previous_note
                        break

                    else:
                        new_n_group.append(note)
                        break

            note_groups.append(new_n_group)


        bars.append(Bar(note_groups[1:]))

    return Piece(bars[1:])
# new_p1 = merge_identical_ids(p1)


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
                        midi.add_note(n.note + 20, current_time + time_displacement_due_to_rests,
                                      n.beat_length,
                                      track_num=j,
                                      volume=round(pieces[j].volume_percentage * n.volume)
                                      ) #the +20 is there to convert the piano number to midi number
                current_time += a[0].beat_length
    midi.save(file_name_to_save)
    return midi