
from typing import *
# from parsing_svg.MusicAbstractions import Note, Bar
class PathCommandParser:

    commands = {"m", "M", "L", "l", "H", "h", "V", "v", "C", "c", "S", "s", "Z", "z"}
    def __init__(self):
        self.x = 0
        self.y = 0


    def path_command_to_beats(self, command: str) -> List[int]:
        """
        Converts a path command to a list of beats.
        :param command: The command to parse
        :return: A list of beats showing how long each note should last
        Note: look at Note class in parsing_svg/MusicAbstractions.py to see which beat length maps to which integer
        """
        if len(command) == 0: return None
        command_stopping_index = None

        for i in range(1, len(command)):
            if command[i] in self.commands:
                command_stopping_index = i
                break

        if command_stopping_index is None: return ""
        print(command[:command_stopping_index])
        print(self.path_command_to_beats(command[command_stopping_index:]))
        return ""
if __name__ == '__main__':
    example_path_command = """M106,74v18M150,74v18M185,74v18M106,90v2h79v-2zM150,85v2h35v-2zM220,74v18M255,74v18M220,90v2h35v-2zM220,85v2h35v-2zM289,74v18M351,74v18M351,90v2h7v-2z"""
    # example_path_command = "M106,74"
    s = PathCommandParser()
    print(
        s.path_command_to_beats(example_path_command)
    )
