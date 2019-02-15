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

	def over(self, player1, player2):
		return self.won(player1, player2) or self.tied(player1, player2)

	def checkMove(self, x, y):
		if [x,y] in self.valid:
			return True
		return False

	def move(self, x, y, s):
		self.board[x][y] = s
		print(self.buttons)
		self.buttons[x][y].configure(text=s) 
		self.valid.pop(self.valid.index([x,y]))
		self.turn += 1
		print(self.board)

	def randomMove(self, s):
		i = random.randint(0, len(self.valid) - 1)
		t = self.valid[i]
		x = t[0]
		y = t[1]
		self.move(x, y, s)

	def boardReset(self):
		for x in range(3):
			for y in range(3):
				game.buttons[x][y].configure(text='')

	def playAgain(self, player = None):
		if player == None:
			return messagebox.askyesno("Game Over", f"Tie game!  Would you like to play again?")
		else:
			return messagebox.askyesno("Game Over", f"{player.name} wins!  Would you like to play again?")

	def tkmove(self, x, y, player, computer, root):
		if (self.turn % 2 == 0 and player.text == 'X') or (self.turn % 2 and player.text == 'O'):
			if self.checkMove(x, y):
				self.move(x, y, player.text)
				win = self.won(player, computer)
				tie = self.tied(player, computer)
				player1 = None
				if win:
					player1 = player
				if win or tie:
					if self.playAgain(player1):
						self.reset()
						self.boardReset()
					else:
						root.destroy()
				else:
					self.randomMove(computer.text)
					win = self.won(computer, player)
					tie = self.tied(computer, player)
					player1 = None
					if win:
						player1 = computer
					if win or tie:
						if self.playAgain(player1):
							self.reset()
							self.boardReset()
						else:
							root.destroy()

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
	

