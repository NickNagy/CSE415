""" Nick Nagy, 1564777
"""

# ItrBreadthFS.py, Mar 2017
# Based on ItrDFS.py, Ver 0.4, Oct, 2017.

# Iterative Breadth-First Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.
# See the TowersOfHanoi.py example file for details.
# Examples of Usage:
# python3 ItrBFS.py TowersOfHanoi
# python3 ItrBFS.py EightPuzzle

import sys

if sys.argv == [''] or len(sys.argv) < 2:
    import BasicEightPuzzle as Problem
    # import TowerOfHanoi as Problem
else:
    import importlib

    Problem = importlib.import_module(sys.argv[1])

print("\nWelcome to ItrBFS")
COUNT = None
BACKLINKS = {}


# DO NOT CHANGE THIS FUNCTION
def runBFS():
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    path, name = IterativeBFS(initial_state)
    print(str(COUNT) + " states examined.")
    return path, name


# DO NOT CHANGE THE NAME OR THE RETURN VALUES
# TODO: implement the core BFS algorithm
def IterativeBFS(initial_state):
    global COUNT, BACKLINKS

    OPEN = [initial_state]
    CLOSED = []
    BACKLINKS[initial_state] = None

    while OPEN != []:
        S = OPEN.pop(0)
        CLOSED.append(S)

        # DO NOT CHANGE THIS SECTION
        # the goal test, return path if reached goal
        if Problem.GOAL_TEST(S):
            print("\n" + Problem.GOAL_MESSAGE_FUNCTION(S))
            backtrace(S)
            path = backtrace(S)
            return path, Problem.PROBLEM_NAME

        COUNT += 1

        print("COUNT = " + str(COUNT))
        print("len(OPEN)=" + str(len(OPEN)))
        print("len(CLOSED)=" + str(len(CLOSED)))

        L = []
        # looks at all possible new states from operations on S
        # if the new state has not already been put on CLOSED, append to L
        for op in Problem.OPERATORS:
            if op.precond(S):
                new_state = op.state_transf(S)
                if not occurs_in(new_state, CLOSED):
                    L.append(new_state)
        # removes any occurrences of L found in OPEN
        # only updates backlink of next_state to S if next_state was not in OPEN
        for next_state in L:
            update_backlink = True
            for i in range(len(OPEN)):
                if next_state == OPEN[i]:
                    update_backlink = False
                    del OPEN[i]
                    break
            if update_backlink:
                BACKLINKS[next_state] = S

        # appends L to the back of OPEN
        OPEN = OPEN + L
        print_state_list("OPEN", OPEN)

# returns a list of states
# DO NOT CHANGE
def backtrace(S):
    global BACKLINKS
    path = []
    while S:
        path.append(S)
        S = BACKLINKS[S]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(s)
    print("\nPath length = " + str(len(path) - 1))
    return path

def print_state_list(name, list):
    print(name + " is now: ", end='')
    for s in list[:-1]:
        print(str(s), end=', ')
    print(str(list[-1]))

# returns true if s1 occurs in list
def occurs_in(s1, list):
    for s2 in list:
        if s1==s2:
            return True
    return False

if __name__ == '__main__':
    path, name = runBFS()