# Author: Bob Young
# Original Date: 1/20/2019
# Description: TicTacToe written in Python 3 with Tkinter GUI
#
# Thoughts: I read that TripleByte had asked some developers to write a TicTacToe program during interviews.
# So I decided to give it a shot.  Originally, I decided to use the console for input from the user, 
# and the computer would make moves randomly.  I had components of the program working within 30 minutes
# or so, but did not have an full solution for over an hour.  Anyhow, after completing this, I decided 
# to put a GUI front end on the program to make it more visually pleasing and easier to use.  
# I used Tkinter for this.  At this point, I am somewhat intrigued by the prospect of
# adding greater intelligence to the moves by the computer (AI of sorts).
# After seeing what was typically done by other programmers who wrote TicTacToe programs, I see that a
# simple list with indexes 0-8 is often used to keep track of the moves.  I opted to use a 3x3 matrix.
# It was just the decision I made at the time.  Perhaps the simple list is somewhat easier, but really,
# neither option offers much complexity.
# Other possible changes for the future are allowing the user to go first or second (Be X's or O's).
# Reporting stats on the GUI.  Note: I had stats (wins, losses, ties) reported to console originally.
# The framework for keeping stats remains.
# Also note however that if I decide to add AI to the computer moves, the computer should never lose 
# and the reporting of stats gets a lot less interesting.


import random
from tkinter import *
from tkinter import font
from tkinter import messagebox
from functools import partial

class Player:
	def __init__(self, name, text):
		self.name = name
		self.text = text
		self.wins = 0
		self.losses = 0
		self.ties = 0

	def win(self):
		self.wins += 1

	def loss(self):
		self.losses += 1

	def tie(self):
		self.ties += 1

	def stats(self):
		return [self.wins, self.ties, self.losses]

class Game:
	def reset(self):
		self.board = [[' ' for _ in range(3)] for _ in range(3)]
		self.valid = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
		self.turn = 0
		self.s = ['X', 'O']

	def __init__(self):
		self.reset()

	def printBoard(self):
		for i in range(3):
			print(self.board[i])

	def won(self, player1, player2):
		txt = player1.text * 3
		if f"{self.board[0][0]}{self.board[0][1]}{self.board[0][2]}" == txt or \
			f"{self.board[1][0]}{self.board[1][1]}{self.board[1][2]}" == txt or \
			f"{self.board[2][0]}{self.board[2][1]}{self.board[2][2]}" == txt or \
			f"{self.board[0][0]}{self.board[1][0]}{self.board[2][0]}" == txt or \
			f"{self.board[0][1]}{self.board[1][1]}{self.board[2][1]}" == txt or \
			f"{self.board[0][2]}{self.board[1][2]}{self.board[2][2]}" == txt or \
			f"{self.board[0][0]}{self.board[1][1]}{self.board[2][2]}" == txt or \
			f"{self.board[2][0]}{self.board[1][1]}{self.board[0][2]}" == txt:
			player1.win()
			player2.loss()
			self.printBoard()
			print(f"**** {player1.name} wins!! ****")
			return True
		return False

	def tied(self, player1, player2):
		if len(self.valid) == 0:
			player1.tie()
			player2.tie()
			self.printBoard()
			print('*** Tie ***')			
			return True
		return False

	# The game is over if somebody won or there is a tie
	def over(self, player1, player2):
		return self.won(player1, player2) or self.tied(player1, player2)

	# Check our list of valid remaining moves to see if the move is valid
	def checkMove(self, x, y):
		if [x,y] in self.valid:
			return True
		return False

    # Process the move by setting the board, the matrix and GUI, plus updating remaining valid moves
	def move(self, x, y, s):
		self.board[x][y] = s
		print(self.buttons)
		self.buttons[x][y].configure(text=s) 
		self.valid.pop(self.valid.index([x,y]))
		self.turn += 1
		print(self.board)

	# Generates a random integer to determine the move by the computer
	# This is the function that I would like to change to add intelligence to the computer moves.
	def randomMove(self, s):
		i = random.randint(0, len(self.valid) - 1)
		t = self.valid[i]
		x = t[0]
		y = t[1]
		self.move(x, y, s)

	# Resets the GUI board
	def boardReset(self):
		for x in range(3):
			for y in range(3):
				game.buttons[x][y].configure(text='')

    # Prompts user in the GUI.  Returns True if the user wants to play again, otherwise False
	def playAgain(self, player = None):
		if player == None:
			return messagebox.askyesno("Game Over", f"Tie game!  Would you like to play again?")
		else:
			return messagebox.askyesno("Game Over", f"{player.name} wins!  Would you like to play again?")

    # A move was made from our GUI
	def tkmove(self, x, y, player, computer, root):
		def winOrTie(player1, player2):
			win = self.won(player1, player2)
			tie = self.tied(player1, player2)
			winner = None
			if win:
				winner = player
				if win or tie:
					if self.playAgain(winner):
						self.reset()
						self.boardReset()
					else:
						root.destroy()

		if (self.turn % 2 == 0 and player.text == 'X') or (self.turn % 2 and player.text == 'O'):
			if self.checkMove(x, y):
				self.move(x, y, player.text)
				winOrTie(player, computer)
			else:
				self.randomMove(computer.text)
				winOrTie(computer, player)

# GUI interface, clicking a button triggers an event calling tkmove of the Game class
if __name__ == '__main__':
	player = Player("Player", "X")
	computer = Player("Computer", "O")
	root = Tk()
	helv36 = font.Font(family='Helvetica', size=10, weight='bold')
	game = Game()
	game.buttons = []
	s = 'X'
	for x in range(3):
		game.buttons += [[]]
		for y in range(3):
			game.buttons[x] += [Button(root, text="", width=30, height=10, borderwidth=5, font=helv36, command=partial(game.tkmove, x, y, player, computer, root))]
			game.buttons[x][y].grid(row=x,column=y)
	root.mainloop()


