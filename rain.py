import time
import random
import os
import shutil

#     __________________________________________________________________________________________________________
#    /             Welcome to PyTrix, my version of the matrix code rain written in python.                    /
#   /   RECOMMENDED THAT YOU RUN THIS IN A NORMAL TERMINAL IDE, TERMINALS CANNOT ACCESS OS FUNCTIONS EASILY.  /
#  /    No other libraries are needed to run this (no packages are needed that aren't included by default.)  /
# /_________________________________________________________________________________________________________/
# This thing is an eyesore, so i left plenty of comments.

os.system("clear")


class Matrix:
    def __init__(self):
        # Initialize global variables and lists.
        global drops
        drops = {"drop type": [], "drop length": [], "drop position": [], "drop index": []}
        global three_dimensional
        three_dimensional = []

        global chars
        chars = []
        with open('list.txt') as f:
            lines = f.readlines()

        # Add the chinese characters to the list.
        for line in lines:
            line = line.replace("\n", "")
            line.strip()
            chars.append(line)

        self.chunks()

    def chunks(self):
        # Define height and column length
        global COLUMNS, ROWS
        COLUMNS, ROWS = shutil.get_terminal_size()

        # Chinese characters are twice the width of english characters
        # (Default width of a single instance of white space) this must be taken into account.
        COLUMNS = COLUMNS / 2
        if type(COLUMNS) == float:
            COLUMNS -= 0.5
        COLUMNS = int(COLUMNS)
        ROWS = ROWS

        # Create values for the first drops.
        for i in range(0, COLUMNS):
            ver, length = self.Igenerate()
            drops["drop type"].append(ver)
            drops["drop length"].append(length)
            drops["drop position"].append(length)
            drops["drop index"].append(i)
        # Start the loop.
        while True:
            self.memory()
            self.project()

    def memory(self):
        # Handle managing the lists of random characters and lengths.
        types = drops["drop type"]
        lengths = drops["drop length"]
        position = drops["drop position"]

        # Clear the last line from the list to keep it at the number of rows.
        if len(three_dimensional) == ROWS:
            three_dimensional.pop(ROWS - 1)

        spot = 0
        # If the drop runs out of length then replace with a blank type.
        for drop in drops["drop position"]:
            if drop == 0 and types[spot] == 0:
                # Invert it from character to white space.
                types.pop(spot)
                types.insert(spot, 1)
                # Generate new length
                leno = self.runtime_generate()
                # Replace old length
                lengths.pop(spot)
                lengths.insert(spot, leno)
                position.pop(spot)
                position.insert(spot, leno)

            elif drop == 0 and types[spot] == 1:
                # Invert it from white space to character.
                types.pop(spot)
                types.insert(spot, 0)
                # Generate new length
                lenl = self.runtime_generate()
                # Replace old length
                lengths.pop(spot)
                lengths.insert(spot, lenl)
                position.pop(spot)
                position.insert(spot, lenl)

            spot += 1

    def colorize(self, index):
        # Make it look like less of an eyesore.
        color = ""
        lengths = drops["drop length"]
        positions = drops["drop position"]
        if lengths[index] - positions[index] == 0:
            color = "255"
        elif lengths[index] - positions[index] == 1 or lengths[index] - positions[index] == 2:
            color = "250"
        elif lengths[index] - positions[index] == 3 or lengths[index] - positions[index] == 4:
            color = "245"
        elif lengths[index] - positions[index] == 5:
            color = "40"
        elif lengths[index] - positions[index] == 6 or lengths[index] - positions[index] == 7:
            color = "34"
        else:
            color = "28"
        # ... The inconsistency is killing me.
        if lengths[index] < 7:
            color = "28"

        return color

    def Igenerate(self):
        # create a rain drop
        rain_type = random.randint(0, 1)
        if random.randint(0, 5) != 3:
            rain_type = 1
        rain_length = random.randint(3, ROWS)
        return rain_type, rain_length

    def runtime_generate(self):
        rain_length = random.randint(3, ROWS)
        return rain_length

    def project(self):
        # Handle projecting the rain to bash (or whatever terminal you use).
        line = []

        types = drops["drop type"]
        positions = drops["drop position"]

        # Format the line that will be printed
        for k in range(0, COLUMNS):
            if types[k] == 0:
                color = self.colorize(k)
                line.append("\033[48;5;232m\033[38;5;{}m{}".format(color, chars[random.randint(0, len(chars) - 1)]))
            else:
                line.append("  ")

        timer = 0
        # Move the position down.
        for position in positions:
            position -= 1
            drops["drop position"].pop(timer)
            drops["drop position"].insert(timer, position)
            timer += 1

        three_dimensional.insert(0, line)
        result = ""
        for thing in three_dimensional:
            timer = 0
            for char in thing:
                # 1/6 chance to change a character:
                if len(char) == 22 and random.randint(0, 5) == 3:
                    char = char[:21] + char[22:]
                    char = char[:21] + chars[random.randint(0, len(chars) - 1)]
                    thing.pop(timer)
                    thing.insert(timer, char)
                elif len(char) == 23 and random.randint(0, 5) == 3:
                    char = char[:22] + char[23:]
                    char = char[:22] + chars[random.randint(0, len(chars) - 1)]
                    thing.pop(timer)
                    thing.insert(timer, char)
                result = result + char
                timer += 1
            # Clump it all together so you don't have *as bad* performance.
            result = result + "\n"

        print(result)

        time.sleep(0.06)
        os.system("clear")


Matrix()