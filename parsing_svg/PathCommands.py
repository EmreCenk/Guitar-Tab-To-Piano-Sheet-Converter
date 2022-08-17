
from typing import *
# from parsing_svg.MusicAbstractions import Note, Bar
class PathCommandParser:

    def __init__(self):
        pass

    @staticmethod
    def path_command_to_beats(command: str) -> List[int]:
        """
        Converts a path command to a list of beats.
        :param command: The command to parse
        :return: A list of beats showing how long each note should last
        Note: look at Note class in parsing_svg/MusicAbstractions.py to see which beat length maps to which integer
        """
        pass