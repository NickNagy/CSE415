""" Nick Nagy, 1564777
BasicEightPuzzle.py

A class to represent an Eight Puzzle
"""

# <METADATA>
# QUIET_VERSION = "0.2"
PROBLEM_NAME = "Basic Eight Puzzle"
# PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['N. Nagy']
PROBLEM_CREATION_DATE = "18-OCT-2017"
PROBLEM_DESC = \
    '''
    A class to represent an Eight Puzzle
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
CREATE_INITIAL_STATE = lambda: State([1, 4, 2, 3, 7, 0, 6, 8, 5])
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
