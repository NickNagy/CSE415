# -*- coding: utf-8 -*-
"""
Daniel Tran
CSE 415
8 November 2017
Assignment 5
This file is an implementation of KInARow using a minimax algorithm to determine where to place a
symbol for the best advantage.
"""
from __future__ import unicode_literals
from random import choice, randint
import copy
import time
import sys
# import IPython

def prepare(initial_state, k, what_side_I_play, opponent_nickname):
	""" Sets the variables that the program will use to determine moves in a game of KInARow
		Args:

		Returns:
			String OK

	"""
	global goal, init, symbol, opponent_symbol, m_rows, n_cols
	goal = k
	init = copy.deepcopy(initial_state)
	symbol = what_side_I_play
	opponent_symbol = 'O' if what_side_I_play is 'X' else 'X'
	m_rows = len(initial_state[0])
	n_cols = len(initial_state[0][0])
	opponent_name = opponent_nickname
	return "OK"

def introduce():
	return """This is Noughty MacCroix, who hails from Aberdeen, Scotland. UW Student danc88 created him to compete in this tournament. 
	He is known for being one of the most fearless players of this game and also a tough cookie."""

def nickname(): return "Noughty MacCroix"

def makeMove(currentState, currentRemark, timeLimit=10000):
	""" Implements a minimax algorithm to determine what move is the best

		Args:
			currentState
			currentRemark
			timeLimit (int): gives the 

		Returns:
	"""
	start_time = time.time()
	result = minimax(currentState, timeLimit, start_time, 2)
	score = result[0]
	new_state = copy.deepcopy(result[1])
	phrases = ["Bring it on, you wee scum", "Just who do you think you err?", "Yer bum's oot the windae!", "Yer aff yer heid!", "Gie it laldy!", "Tatties o wer the side, laddie!"]
	curr_board = currentState[0]

	# New board is same.
	new_board = copy.deepcopy(new_state[0])
	for row in range(m_rows):
		for col in range(n_cols):
			if curr_board[row][col] != new_board[row][col]:
				break
		else:
			continue
		break
	return [[[row, col], new_state], choice(phrases)]
	
def minimax(state, timeLimit, start_time, plyLeft):
	""" Implements a minimax algorithm to determine what move is the best

		Args:
			state
			timeLimit
			start_time
			plyLeft

		Returns:
	"""
	# If we have gone through enough layers or enough 
	if plyLeft == 0 or (time.time() - start_time >= timeLimit * 0.9): return [staticEval(state), state]
	# Check the piece and assign provisional value
	next_state = copy.deepcopy(state)
	# Person currently playing
	player = state[1]
	# Assigns dummy value
	if player == symbol: provisional = -sys.maxsize - 1
	else: provisional = sys.maxsize
	# Goes through a list of successors
	for successor in generate_next(state):
		new_val = minimax(successor, timeLimit, start_time, plyLeft - 1)
		if (player == symbol and new_val[0] > provisional) \
			or (player == opponent_symbol and new_val[0] < provisional):
			provisional = new_val[0]
			next_state = copy.deepcopy(successor)
	return [provisional, next_state]

def generate_next(state):
	""" Generates the possible placements of the piece on the current state of the board.

		Args:
			state

		Returns:
			List of possible successors to the state

	"""
	board = state[0]
	piece = state[1]
	next_piece = "X" if piece is "O" else "O"
	successors = []
	for row in list(range(m_rows)):
		for col in list(range(n_cols)):
			if board[row][col] == ' ':
				successor_board = copy.deepcopy(board)
				# Places mark on board as potential move
				successor_board[row][col] = piece
				successor_state = [copy.deepcopy(successor_board), next_piece]
				successors.append(successor_state)
	return successors

def staticEval(state):
	""" Calculates the advantage of the player in comparison to the opponent.

		Args:
			state:

		Returns:
			Score

	"""
	player_score = score(state[0], state[1])
	opp = "X" if state[1] is "O" else "O"
	opponent_score = score(state[0], opp)
	return player_score - opponent_score

def score(board, mark):
	""" Calculates the score advantage of a particular mark on the board

		Args:
			board ()
			mark (str):

		Returns:
			Int value representing the score
	"""
	eval_score = 0
	opp = "X" if mark is "O" else "O"
	# Generates the rows, columns and the diagonal arrangements on the board
	orientations = board + get_columns(board) + get_diagonals(board)
	# Goes through the various arrangements and calculates a score.
	for checks in orientations: 
		marks = 0
		opp_seen = 0
		in_row = 0
		for element in checks:
			if element == mark:
				marks += 1
				in_row += 1
			elif element == opp:
				opp_seen += 1
				in_row = 0
			elif in_row == goal:
				eval_score += 100**goal
			else:
				if in_row != 0:
					eval_score += 5**in_row
					in_row = 0
		if in_row > 1:
			eval_score += 5**in_row
		if opp_seen > 0:
			eval_score += 10**opp_seen + 100**(max(m_rows, n_cols) - marks)
		
	return eval_score 

def get_diagonals(board):
	""" Generates the diagonal representations of the board

		Args:
			board
			
		Returns:
			List of the colums of the board.
	"""
	diags = []
	for r0 in range(m_rows + n_cols - 1):
		top_l_bottom_r = []
		bottom_l_top_r = []
		for c0 in range(max(r0 - m_rows +1,0), min(r0+1, n_cols)):
			top_l_bottom_r.append(board[m_rows - r0 + c0 - 1][c0])
			bottom_l_top_r.append(board[r0 - c0][c0])
		diags.append(top_l_bottom_r)
		diags.append(bottom_l_top_r)
	return diags

def get_columns(board):
	""" Obtains representation of the boards of the columns

		Args:
			board

		Returns:
			List of the colums of the board.
	"""
	retlist = []
	for col in range(0, m_rows):
		col_arr = []
		for row in board:
			col_arr.append(row[col])
		retlist.append(col_arr)
	return retlist