""" Nick Nagy, 1564777
"""

# Astar.py, April 2017
# Based on ItrDFS.py, Ver 0.4a, October 14, 2017.

# A* Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.
# See the TowerOfHanoi.py example file for details.
# Examples of Usage:

# A small change was made on Oct. 14, so that backtrace
# uses None as the BACKLINK value for the initial state,
# just as in ItrDFS.py, rather than using -1 as it did
# in an earlier version.

# python3 AStar.py EightPuzzleWithHeuristics h_manhattan

import sys
from priorityq import PriorityQ

# DO NOT CHANGE THIS SECTION
if sys.argv == [''] or len(sys.argv) < 2:
    import EightPuzzleWithHeuristics as Problem
    heuristics = lambda s: Problem.HEURISTICS['h_custom'](s)

else:
    import importlib

    Problem = importlib.import_module(sys.argv[1])
    heuristics = lambda s: Problem.HEURISTICS[sys.argv[2]](s)


print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}


# DO NOT CHANGE THIS SECTION
def runAStar():
    # initial_state = Problem.CREATE_INITIAL_STATE(keyVal)
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    path, name = AStar(initial_state)
    print(str(COUNT) + " states examined.")
    return path, name


# A star search algorithm
def AStar(initial_state):
    global COUNT, BACKLINKS
    # priority queue with respective priority
    # add any auxiliary data structures as needed
    OPEN = PriorityQ()
    # inserts the initial state with a priority of 0 (priority for initial state is irrelevant to algorithm)
    OPEN.insert(initial_state, 0)
    CLOSED = []
    BACKLINKS[initial_state] = None

    while OPEN.__len__() > 0:
        # S = min-priority state (priority value gets discarded, only state is looked at)
        S = OPEN.deletemin()[0]
        while S in CLOSED:
            S = OPEN.deletemin()
        CLOSED.append(S)

        # DO NOT CHANGE THIS SECTION: beginning
        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            path = backtrace(S)
            return path, Problem.PROBLEM_NAME
            # DO NOT CHANGE THIS SECTION: end

        COUNT += 1
        # if (COUNT % 32)==0:
        if True:
            # print(".",end="")
            # if (COUNT % 128)==0:
            if True:
                print("COUNT = " + str(COUNT))
                print("len(OPEN)=" + str(len(OPEN)))
                print("len(CLOSED)=" + str(len(CLOSED)))

        L = []
        # looks at all possible new states from operations on S
        # if the new state has not already been put on CLOSED, append to L
        for op in Problem.OPERATORS:
            if op.precond(S):
                new_state = op.state_transf(S)
                #print(new_state.__str__())
                if not occurs_in(new_state, CLOSED):
                    L.append(new_state)
                    BACKLINKS[new_state] = S

        # adds new states in L into OPEN with their priorities
        # if any state already occurs in OPEN...
        #   if L's state has a lower priority, change OPEN's state priority to L's
        #   otherwise, keep OPEN's state in OPEN, ignore L's
        for state in L:
            g_state = G(state)
            if OPEN.__contains__(state):
                if g_state < OPEN.getpriority(state):
                    OPEN.remove(state)
                else: break
            OPEN.insert(state, g_state)


        #print("OPEN is now: " + OPEN.__str__())

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

# returns true if s occurs in list
def occurs_in(s, list):
    for state in list:
        if state == s:
            return True
    return False

# priority function, a sum of the number of states S is from the initial state,
# plus the heuristic function for S
def G(S):
    global BACKLINKS
    h_s = heuristics(S)
    path_length = 0
    while S:
        S = BACKLINKS[S]
        path_length += 1
    return path_length + h_s

if __name__ == '__main__':
    path, name = runAStar()