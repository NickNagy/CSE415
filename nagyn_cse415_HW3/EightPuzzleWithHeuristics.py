""" Nick Nagy, 1564777
BasicEightPuzzle.py

A class to represent an Eight Puzzle, that includes heuristics and sample initial puzzles
"""

import sys

if sys.argv == [''] or len(sys.argv) < 3:
    puzzle_name = 'puzzle12a.py'
else:
    puzzle_name = sys.argv[3]

# <METADATA>
# QUIET_VERSION = "0.2"
PROBLEM_NAME = "Eight Puzzle With Heuristics"
# PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['N. Nagy']
PROBLEM_CREATION_DATE = "18-OCT-2017"
PROBLEM_DESC = \
    '''
    A class to represent an Eight Puzzle, that includes heuristics and sample initial puzzles
    '''


# </METADATA>

# <COMMON_CODE>


class State:
    def __init__(self, tiles):
        self.tiles = tiles

    def __eq__(self, s):
        # checks that every index of State s is equal to every index of self
        for i in range(9):
            if self.tiles[i] != s.tiles[i]:
                return False
        return True

    def __hash__(self):
        # hash function used for dictionary keys
        return (self.__str__()).__hash__()

    def __str__(self):
        # returns a string representation of self's indeces
        text_copy = "[" + str(self.tiles[0])
        i = 1
        while i < 9:
            text_copy += "," + str(self.tiles[i])
            i += 1
        text_copy += "]"
        return text_copy

    def copy(self):
        # returns a deep copy of self
        tiles_copy = [0] * 9
        for i in range(9):
            tiles_copy[i] = self.tiles[i]
        news = State(tiles_copy)
        return news

    def can_move(self, index, direction):
        # returns true if the tile at index can move in the given direction,
        # otherwise returns false
        # tile can be moved if the element at the index it's moving to is zero
        try:
            if direction == 0:
                return index % 3 > 0 and self.tiles[index - 1] == 0
            if direction == 1:
                return index % 3 < 2 and self.tiles[index + 1] == 0
            if direction == 2:
                return index > 2 and self.tiles[index - 3] == 0
            if direction == 3:
                return index < 6 and self.tiles[index + 3] == 0
        except Exception as e:
            print(e)

    def move(self, index, direction):
        # returns a deep copy state of self's value at index moved in the given direction
        news = self.copy()
        if direction == 0:
            news.tiles[index - 1] = news.tiles[index]
        if direction == 1:
            news.tiles[index + 1] = news.tiles[index]
        if direction == 2:
            news.tiles[index - 3] = news.tiles[index]
        if direction == 3:
            news.tiles[index + 3] = news.tiles[index]
        news.tiles[index] = 0
        return news


def goal_message(s):
    # if the value at each index of s is equal to the index, s is a goal state
    return "The puzzle is solved!"

def goal_test(s):
    return s.__eq__(State([0, 1, 2, 3, 4, 5, 6, 7, 8]))

# INCORRECT IMPLEMENTATION -> to be fixed
def h_euclidean(s):
    # calculates the euclidean distance from each index in s to its goal state index
    # returns a sum of all these calculations
    sum = 0
    for i in range(9):
        count = 0
        while s.tiles[count] != i:
            count += 1
        if count < i:
            sum += i - count
        else:
            sum += count - i
    return sum


def h_hamming(s):
    # returns the number of indeces of s that aren't at their goal state indeces
    off = 0
    for i in range(9):
        if s.tiles[i] != i:
            off += 1
    return off


def h_manhattan(s):
    # for each index i, calculates the number of rows and columns i is from its goal state index
    # returns a sum of all calculations
    sum = 0
    for i in range(9):
        count = 0
        while s.tiles[count] != i:
            count += 1
        if count > i:
            row_diff = int(count / 3) - int(i / 3)
            col_diff = count % 3 - i % 3
        else:
            row_diff = int(i / 3) - int(count / 3)
            col_diff = i % 3 - count % 3
        sum += row_diff + col_diff
    return sum

# returns a sum of euclidean heuristics and hamming heuristics of s
def h_custom(s):
    euclidean = h_euclidean(s)
    hamming = h_hamming(s)
    manhattan = h_manhattan(s)
    return euclidean + hamming


class Operator:
    def __init__(self, precond, state_transf):
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


# </COMMON_CODE>

# <COMMON_DATA>
# </COMMON_DATA>

# <INITIAL_STATE>
CREATE_INITIAL_STATE = lambda: PUZZLES[puzzle_name]
# </INITIAL_STATE>

# <OPERATORS>
LEFT_OPERATIONS = [Operator(lambda s, i1=i: s.can_move(i1, 0), lambda s, i1=i: s.move(i1, 0)) for i in range(9)]
RIGHT_OPERATIONS = [Operator(lambda s, i1=i: s.can_move(i1, 1), lambda s, i1=i: s.move(i1, 1)) for i in range(9)]
UP_OPERATIONS = [Operator(lambda s, i1=i: s.can_move(i1, 2), lambda s, i1=i: s.move(i1, 2)) for i in range(9)]
DOWN_OPERATIONS = [Operator(lambda s, i1=i: s.can_move(i1, 3), lambda s, i1=i: s.move(i1, 3)) for i in range(9)]

OPERATORS = LEFT_OPERATIONS + RIGHT_OPERATIONS + UP_OPERATIONS + DOWN_OPERATIONS

# </OPERATORS>

# <GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE>

# heuristics reference
HEURISTICS = {'h_euclidean': h_euclidean, 'h_hamming': h_hamming,
              'h_manhattan': h_manhattan, 'h_custom': h_custom}

# puzzle reference
PUZZLES = {'puzzle0.py': State([0, 1, 2, 3, 4, 5, 6, 7, 8]), 'puzzle1a.py': State([1, 0, 2, 3, 4, 5, 6, 7, 8]),
           'puzzle2a.py': State([3, 1, 2, 4, 0, 5, 6, 7, 8]), 'puzzle3a.py': State([1, 4, 2, 3, 7, 0, 6, 8, 5]),
           'puzzle10a.py': State([4, 5, 0, 1, 2, 3, 6, 7, 8]), 'puzzle12a.py': State([3, 1, 2, 6, 8, 7, 5, 4, 0]),
           'puzzle14a.py': State([4, 5, 0, 1, 2, 8, 3, 7, 6]), 'puzzle16a.py': State([0, 8, 2, 1, 7, 4, 3, 6, 5])}
