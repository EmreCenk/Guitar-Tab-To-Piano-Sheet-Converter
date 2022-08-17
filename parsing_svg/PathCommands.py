
from typing import *
# from parsing_svg.MusicAbstractions import Note, Bar


class Command:
    def __init__(self, command: str):
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

            current_command = Command(command[:command_stopping_index])
            commands.append(current_command)

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
    def path_command_to_beats(self, command: str) -> List[int]:
        """
        Converts a path command to a list of beats.
        :param command: The command to parse
        :return: A list of beats showing how long each note should last
        Note: look at Note class in parsing_svg/MusicAbstractions.py to see which beat length maps to which integer
        """

        commands = self.convert_string_to_command_list(command)
        for c in commands: print(c)
        verticals = [] # a list of y coordinates where there are vertical lines
        horizontals = [] # A list of x intervals showing where the horizontal lines are

        for i in range(len(commands)):
            print(commands[i], type(commands[i]))
            if commands[i].command_letter.lower() == "v":
                verticals.append(self.y) # y coordinate of where we last moved

            elif commands[i].command_letter == "h":
                horizontals.append((self.x, self.x + commands[i].inputs[0]))

            elif commands[i].command_letter == "H":
                horizontals.append((self.x, commands[i].inputs[0]))
            self.execute_command(commands[i])

        print(verticals)
        print(horizontals)


if __name__ == '__main__':
    example_path_command = """M106,74v18M150,74v18M185,74v18M106,90v2h79v-2zM150,85v2h35v-2zM220,74v18M255,74v18M220,90v2h35v-2zM220,85v2h35v-2zM289,74v18M351,74v18M351,90v2h7v-2z"""
    # example_path_command = "M106,74"
    s = PathCommandParser()
    print(
        s.path_command_to_beats(example_path_command)
    )


