import numpy as np
#This file builds a minesweeper puzzle that can be played in the terminal using numpy arrays.

#this function creates the numpy board array and randomly lays 10 mines
def build_board():
	a = np.zeros((10,10))
	count = 0 
	while count < 10:
		i = np.random.randint(0,10)
		j = np.random.randint(0,10)
		if(a[i,j] == 0):
			a[i,j] = -1
			count += 1

	return a

'''This function takes a board created by build board and places numbers on a copy of the board corresponding
to the number of mines adjacent to each cell.'''
def lay_warnings(a):
	b = a.copy()
	for i in range(0,10):
		for j in range(0,10):
			if a[i,j] != -1:
				if(i >0):
					b[i,j] -= a[i-1,j]
					if(j>0):
						b[i,j] -= a[i-1, j-1]
					if(j<9):
						b[i,j] -= a[i-1, j+1]
				if(j>0):
					b[i,j] -= a[i,j-1]
				if(j <9):
					b[i,j] -= a[i,j+1]
				if(i <9):
					b[i,j] -= a[i+1,j]
					if(j>0):
						b[i,j] -= a[i+1, j-1]
					if(j<9):
						b[i,j] -= a[i+1, j+1]
	return b

#This function tests a guess against the key then updates the puzzle.
def update_puzzle(puzzle, key, a, b):
	if(key[a,b] == -1): #game is lost landed on mine
		return 0,puzzle
	if(key[a,b] > 0):
		puzzle[a,b] = key[a,b]
		return 1,puzzle
	if(key[a,b] == 0):
		queue = []
		queue += [[a,b]]
		while (len(queue) != 0):
			i = queue[0][0]
			j = queue[0][1]
			if(i >0):
				if(key[i-1,j] == 0 and puzzle[i-1,j]!= 0):
					queue += [[i-1,j]] 
				if(j>0):
					if(key[i-1, j-1] == 0 and puzzle[i-1,j-1] != 0):
						queue += [[i-1,j-1]]
				if(j<9):
					if(key[i-1, j+1] == 0 and puzzle[i-1,j+1]!= 0):
						queue += [[i-1, j+1]]
			if(j>0):
				if(key[i,j-1] == 0 and puzzle[i,j-1]!= 0):
					queue += [[i, j-1]]
			if(j <9):
				if(key[i,j+1] == 0 and puzzle[i,j+1]!= 0):
					queue += [[i, j+1]]
			if(i <9):
				if(key[i+1,j] == 0 and puzzle[i+1,j]!= 0):
					queue += [[i+1,j]]
				if(j>0):
					if(key[i+1, j-1]== 0 and puzzle[i+1,j-1]!=0):
						queue += [[i+1, j-1]]
				if(j<9):
					if(key[i+1, j+1] == 0 and puzzle[i+1,j+1]!= 0):
							queue += [[i+1, j+1]]
			puzzle[i,j] = key[i,j]
			if(i >0):
				puzzle[i-1, j] = key[i-1,j]
				if(j>0):
					puzzle[i-1, j-1] = key[i-1,j-1]
				if(j<9):
					puzzle[i-1, j+1] = key[i-1, j+1]
			if(j > 0):
				puzzle[i,j-1] = key[i,j-1]
			if(j <9):
				puzzle[i,j+1] = key[i, j+1]
			if(i <9):
				puzzle[i+1,j] = key[i+1,j]
				if(j >0):
					puzzle[i+1, j-1] = key[i+1,j-1]
				if(j<9):
					puzzle[i+1,j+1] = key[i+1,j+1]
			queue = queue[1:]
		return 1, puzzle

#This function applies all previous functions to play a classic 10X10 game of minesweeper
def play():
	key = lay_warnings(build_board())
	puzzle =-1* np.ones((10,10))
	count = 100
	while(count > 10):
		print(str(count) + " tiles remaining")
		print(puzzle)
		print("Enter ROW COL with 0 based indexing.")
		guess = input().split()
		for i in range(0,2):
			guess[i] = int(guess[i])
		print(guess[0], guess[1])
		x, puzzle = update_puzzle(puzzle, key, guess[0], guess[1])

		if(x == 0):
			return "Ka - Boom"
		count = 0
		for i in range(0,10):
			for j in range(0,10):
				if(puzzle[i,j] == -1):
					count +=1
		
			
	return "SOLVED SAFELY"




print(play())




