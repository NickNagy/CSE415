""" nagynKInARow.py

Nick Nagy
CSE 415 Assignment 5: K-in-a-Row

Use this class as an agent in K-in-a-row
Assumptions: this agent is always max; opponent is always min

"""

from random import randint
import math
import copy
import time

"""state has the form:

[[[' ', ' ', ' ',],
[' ', ' ', ' ',]], "X"]

state[0] = board
state[1] = whose_move

"""


# sets up agent
def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    global k_num
    global n_rows
    global n_cols
    global my_side
    global opponent_side
    global opponent_name
    global zobristnum
    global state_map
    k_num = k
    state_map = {}
    n_cols = len(initial_state[0][0])  # j
    n_rows = len(initial_state[0])  # i
    if n_cols < k_num and n_rows < k_num:
        return "ERROR: Board is too small."
    my_side = what_side_I_play
    opponent_name = opponent_nickname
    if my_side == 'X':
        opponent_side = 'O'
    else:
        opponent_side = 'X'
    # zobrist init
    S = n_cols * n_rows
    P = 2
    zobristnum = [[0] * P for i in range(S)]
    for i in range(S):
        for j in range(P):
            zobristnum[i][j] = randint(0, 2 ** 32)
    return "OK"


# introduces the agent and the creator
def introduce():
    return """Greetings, I am """ + nickname() + """. I am an agent 
    designed by Nick Nagy (nagyn@uw.edu) to play games of K-in-a-Row.
    If I come off at all condescending, it's because I already know 
    I'm better than you.
    """


# return's the agent's nickname
def nickname():
    return "Nuzzle"


# runs minimax search on currentState with iterative deepening 
# within the given timeLimit
# returns [[index of next placement, next state chosen], remark]
def makeMove(currentState, currentRemark, timeLimit=10000):
    alpha = -math.inf
    beta = math.inf
    root_successors = successors(currentState, my_side)
    num_plies = 1
    # iterative deepening while time limit hasn't run out
    # each loop, puts best successor at beginning of root_successors
    # and number of plies increases by 1
    while timeLimit - time.time() > 0:
        next_root_successors = []
        for s in root_successors:
            val = minimax(s[0], alpha, beta, num_plies)
            if val > alpha:
                alpha = val
                next_root_successors.insert(0, s)
            else:
                next_root_successors.append(s)
        root_successors = next_root_successors
        num_plies += 1
    best_state = root_successors[0]
    return [best_state[1], best_state[0]], remarks(currentRemark, best_state[0])


# returns a mathematical evaluation of all rows, columns, and diagonals in a state
# will be a high number if in favor of max (my_side); low number if in favor of min (opponent_side)
def staticEval(state):
    # checks first if static evaluation of state has already been calculated/saved in state_map
    if zobrist_hash(state) in state_map:
        return state_map[zobrist_hash(state)]
    board = state[0]
    total_eval_score = 0
    # horizontal:
    for i in range(n_rows):
        h_score = segment_eval(board[i][0], my_side) - segment_eval(board[i][0], opponent_side)
        if h_score > 0:
            total_eval_score += h_score ** h_score
        else:
            total_eval_score -= h_score ** h_score
    # vertical:
    for j in range(n_cols):
        h_score = segment_eval(board[0][j], my_side) - segment_eval(board[0][j], opponent_side)
        if h_score > 0:
            total_eval_score += h_score ** h_score
        else:
            total_eval_score -= h_score ** h_score
    # diagonal:
    total_eval_score += diag_eval(state)
    # stores state in state_map with corresponding static evaluation score
    state_map[zobrist_hash(state)] = total_eval_score
    return total_eval_score


# segment is a row or column
# adds the number of side pieces in the segment
def segment_eval(segment, side):
    sum = 0
    for i in range(len(segment)):
        if segment[i] == side:
            sum += 1
    return sum


# evaluates every diagonal in the board
# for each diagonal, sums my_side pieces - opponent_side pieces, then signed & squared
# returns a sum of all diagonal evaluations
def diag_eval(state):
    board = state[0]
    diag_eval_score = 0
    for j in range(n_cols):  # tR -> bR corner, bR -> tL orientation
        sum = 0
        i = n_rows - 1
        j1 = j
        while i > -1 and j1 > -1:
            if board[i][j1] == my_side:
                sum += 1
            if board[i][j1] == opponent_side:
                sum -= 1
            i -= 1
            j1 -= 1
        if sum > 0:
            diag_eval_score += sum ** sum
        else:
            diag_eval_score -= sum ** sum
    for i in range(n_rows):  # bL -> bR corner, bR -> tL orientation
        sum = 0
        j = n_cols - 1
        i1 = i
        while i1 > -1 and j > -1:
            if board[i1][j] == my_side:
                sum += 1
            if board[i1][j] == opponent_side:
                sum -= 1
            i1 -= 1
            j -= 1
        if sum > 0:
            diag_eval_score += sum ** sum
        else:
            diag_eval_score -= sum ** sum
    for j in range(n_cols):  # tL -> bL corner, bL -> tR orientation
        i = 0
        j1 = j
        while j1 > -1 and i < n_rows:
            if board[i][j1] == my_side:
                sum += 1
            if board[i][j1] == opponent_side:
                sum -= 1
            i += 1
            j1 -= 1
        if sum > 0:
            diag_eval_score += sum ** sum
        else:
            diag_eval_score -= sum ** sum
    for i in range(n_rows):  # bL -> bR corner, bL -> tR orientation
        j = n_cols - 1
        i1 = i
        while i1 < n_rows and j > -1:
            if board[i1][j] == my_side:
                sum += 1
            if board[i1][j] == opponent_side:
                sum -= 1
            i1 += 1
            j -= 1
        if sum > 0:
            diag_eval_score += sum ** sum
        else:
            diag_eval_score -= sum ** sum
    return diag_eval_score


# minimax search
def minimax(state, alpha, beta, plyLeft):
    # print("minimax: " + str(state[0]))
    whose_move = state[1]
    if plyLeft == 0:
        return staticEval(state)
    for s in successors(state, whose_move):
        # pruning step
        if alpha > beta:
            break
        val = minimax(s[0], alpha, beta, plyLeft - 1)
        if whose_move == my_side and val > alpha:
            alpha = val
        elif whose_move == opponent_side and val < beta:
            beta = val
    if whose_move == my_side:
        return alpha
    return beta


# returns a list of successor states & corresponding move descriptors [[[board, other(whose_move)], description], ...]
def successors(state, whose_move):
    successor_list = []
    for i in range(n_rows):
        for j in range(n_cols):
            if state[0][i][j] == ' ':
                new_state = copy_board(state[0], i, j, whose_move), other(whose_move)
                # print("NEW STATE: " + str(new_state))
                if len(successor_list) > 0:
                    new_val = staticEval(new_state)
                    # print("SUCC LIST: " + str(successor_list[0][0]))
                    first_val = staticEval(successor_list[0][0])
                    if (whose_move == my_side and new_val > first_val) or (
                                    whose_move == opponent_side and new_val < first_val):
                        successor_list.insert(0, [new_state, [i, j]])
                else:
                    successor_list.append(
                        [new_state, [i, j]])
    return successor_list


# returns a deep copy of the board with an update of whose_move placed at tile [i,j]
def copy_board(board, i, j, whose_move):
    # print(str(board))
    new_board = copy.deepcopy(board)
    # print("deep copy before changes: " + str(new_board))
    new_board[i][j] = whose_move
    # print("WHOSE MOVE = " + whose_move + "; BOARD = " + str(new_board))
    return new_board


# returns the side of the opposite player of whose_move
def other(whose_move):
    if whose_move == my_side:
        return opponent_side
    return my_side


# from the in-class code
# returns a value for hashing purposes
def zobrist_hash(state):
    val = 0
    board = state[0]
    for i in range(n_rows):
        for j in range(n_cols):
            piece = None
            if board[i][j] == my_side:
                piece = 1
            if board[i][j] == opponent_side:
                piece = 0
            if piece is not None:
                val ^= zobristnum[i * j][piece]
    return val


# returns a remark to the opponent
def remarks(currentRemark, state):
    # beginning of the game
    if currentRemark == "The game is starting.":
        return "Well, I guess I'll start things off! Won't make a difference who does!"
    # likely loss
    if staticEval(state) < 0:
        return "Hm... looks like you're getting lucky, " + \
               opponent_name + "... obviously this won't happen again, so enjoy."
    return "Cute, " + opponent_name + "... but check THIS out."
