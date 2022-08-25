from midiutil import MIDIFile


class MIDICreator(MIDIFile):
    """
    Wrapper class to simplify some arguments in the midifile
    """
    def __init__(self, tempo_bmp: int):
        super().__init__(5)
        self.current_track = 0
        self.addTempo(self.current_track, 0, tempo_bmp)

    def add_note(self, note_number: int, starting_time: float, duration: float, volume: int = 100, track_num: int = 0):
        self.addNote(track_num, track_num, note_number, starting_time, duration, volume)

    def save(self, save_name: str):
        if save_name[:4] != ".mid": save_name += ".mid"
        with open(save_name, "wb") as output_file:
            self.writeFile(output_file)

# track = 0
# channel = 0
# time = 0  # In beats
# tempo = 60  # In BPM
# volume = 100  # 0-127, as per the MIDI standard

# MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
# automatically)
# MyMIDI.addTempo(track, time, tempo)

# MyMIDI.addNote(track, channel, 60, time + 0, 3, volume)
# MyMIDI.addNote(track, channel, 64, time + 0, 3, volume)
# MyMIDI.addNote(track, channel, 67, time + 0, 3, volume)

