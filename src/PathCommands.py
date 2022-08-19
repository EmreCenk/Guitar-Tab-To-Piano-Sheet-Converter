
from collections import defaultdict
from typing import *
from src.MusicAbstractions import PianoNote, Bar

#TODO: THE DOTS AREN'T DETECTED (BC YOU DID NOT ACCOUNT FOR THEM IN THE CODE LOL)
class Command:
    def __init__(self, command: str):
        # print(command, len(command))
        self.command_letter = command[0]
        self.inputs = []

        if "," in command:
            # there are two inputs as numbers
            k = command[1:].split(",")
            self.inputs.append(int(k[0]))
            self.inputs.append(int(k[1]))

        elif len(command) > 1:
            self.inputs.append(int(command[1:]))

    def __str__(self):
        w = self.command_letter
        if len(self.inputs) == 0: return w + ": ()"
        else: w += ": ("
        for i in self.inputs: w += str(i) + ", "
        w = w[:-2] + ")"
        return w

class PathCommandParser:

    commands = {"m", "M", "L", "l", "H", "h", "V", "v", "C", "c", "S", "s", "Z", "z"}
    def __init__(self):
        self.x = 0
        self.y = 0


    def convert_string_to_command_list(self, command: str) -> List[Command]:
        """
        :param command: command to parse
        :return: List of parsed commands
        """
        commands = []

        while len(command) > 1:
            command_stopping_index = 0
            for i in range(1, len(command)):
                if command[i] in self.commands:
                    command_stopping_index = i
                    break
            # print('comstop', command_stopping_index)
            if command_stopping_index > 0:
                current_command = Command(command[:command_stopping_index])
                commands.append(current_command)
            else: command_stopping_index += 1
            command = command[command_stopping_index:]
        if len(command) == 1: commands.append(Command(command))

        return commands


    def execute_command(self, command: Command):
        """
        Parses a command and moves the self.x and self.y variables accordingly
        :param command:
        :return:
        """
        if command.command_letter == "M":
            self.x = command.inputs[0]
            self.y = command.inputs[1]
        elif command.command_letter == "m":
            self.x += command.inputs[0]
            self.y += command.inputs[1]


        elif command.command_letter == "V":
            self.y = command.inputs[0]
        elif command.command_letter == "v":
            self.y += command.inputs[0]

        elif command.command_letter == "H":
            self.x = command.inputs[0]
        elif command.command_letter == "h":
            self.x += command.inputs[0]

    def get_vertical_and_horizontal_lines(self, commands: List[Command]) -> Tuple[List[int], List[Tuple[int, int]]]:
        """
        :param commands:
        :return: [x coordinates of vertical lines, x intervals of horizontal lines]
        """
        verticals = [] # a list of x coordinates where there are vertical lines
        horizontals = [] # A list of x intervals showing where the horizontal lines are

        for i in range(len(commands)):
            if commands[i].command_letter.lower() == "v":
                if commands[i].inputs[0] == 18:
                # if commands[i-1].command_letter == "M":
                    verticals.append(self.x) # x coordinate of where we last moved
                # else:
                #     print("ew", commands[i].inputs[0], self.x)

            elif commands[i].command_letter == "h":
                horizontals.append(tuple(sorted((self.x, self.x + commands[i].inputs[0]))))

            elif commands[i].command_letter == "H":
                horizontals.append(tuple(sorted((self.x, commands[i].inputs[0]))))
            self.execute_command(commands[i])
        return verticals, horizontals

    def dot_correction(self, lengths: List[float], verticals: List[int], horizontals: List[Tuple[int, int]]) -> List[float]:
        """
        Note: mutates the lengths array in place fyi
        :param lengths: beat lengths obtained from regular line intersection algorithm
        :param verticals: coordinates of the verticals obtained from regular line intersection algorithm
        :param horizontals: coordinates of the horizontals obtained from regular line intersection algorithm
        :return: the lengths array, accounting for the dots that multiply the beat length by 1.5
        """
        for h0, h1 in horizontals:
            length = abs(h1 - h0) #i'm pretty sure h1>h0, but better be safe than sorry with the abs()
            if length >= 3: continue
            closest_vertical = min(verticals, key = lambda v: abs(v-h0))
            lengths[verticals.index(closest_vertical)] *= 1.5
        return lengths

    def path_command_to_beats(self, command: str) -> List[float]:
        """
        Converts a path command to a list of beat lengths.
        :param command: The command to parse
        :return: A list of beats showing how long each note should last
        Note: look at Note class in src/MusicAbstractions.py to see which beat length maps to which integer
        """

        commands = self.convert_string_to_command_list(command)
        # for c in commands: print(c)
        verticals, horizontals = self.get_vertical_and_horizontal_lines(commands)

        number_of_intersections = {v: 0 for v in verticals}
        # print(sorted(set(verticals)), horizontals)
        #finding the number of times each vertical line intersects with a horizontal line:
        for i in range(len(verticals)):
            for h0, h1 in horizontals:
                if h0 <= verticals[i] <= h1:
                    number_of_intersections[verticals[i]] += 1
        # print(number_of_intersections)
        lengths = []
        for k in sorted(number_of_intersections):
            lengths.append(1/2**number_of_intersections[k])
            # todo: notes can't last longer than a single beat (i've never seen 1+ beats before so when i encounter them, i'll have to fix this)
        self.dot_correction(lengths, verticals, horizontals)
        return lengths

if __name__ == '__main__':
    # example_path_command="M106,74v18M150,74v18M185,74v18M106,90v2h79v-2zM150,85v2h35v-2zM220,74v18M255,74v18M220,90v2h35v-2zM220,85v2h35v-2zM289,74v18M351,74v18M351,90v2h7v-2z"
    # example_path_command = "M427,74v18M462,74v18M427,85v2h35v-2zM497,74v18M427,90v2h70v-2zM541,74v18M585,74v18M629,74v18M673,74v18M541,90v2h132v-2z"
    # e2 = "M106,74v18M150,74v18M185,74v18M106,90v2h79v-2zM150,85v2h35v-2zM220,74v18M255,74v18M220,90v2h35v-2zM220,85v2h35v-2zM289,74v18M351,74v18M351,90v2h7v-2z"
    # e3 = "M31,74v18M76,74v18M121,74v18M31,90v2h90v-2zM166,74v18M170,90v2h2v-2z" #test case with dots next to note beats, output should be [0.5, 0.5, 0.5, 1.5]
    # this one is sus don't worry about it e4 = "M570,74v18M598,74v18M626,74v18M570,85v2h56v-2zM654,74v18M570,90v2h84v-2zM693,74v18M732,74v18M771,74v18M809,74v18M693,90v2h116v-2z" # should be [0.25, 0.25
    s4 = "M316,74v18M352,74v18M316,90v2h36v-2zM388,83v9M462,74v18"
    s = PathCommandParser()
    print(
        s.path_command_to_beats(s4)
    )


