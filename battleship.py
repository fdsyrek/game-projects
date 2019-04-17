import numpy as np
'''This file contains functions to build a battleship board lay the ships and play
against a CPU that randomly selects everything it does.'''

def build_board():
	a = np.zeros((10,10))
	b = np.zeros((10,10))
	return [a,b]

#Function takes player inputs from play function and lays down carrier ship. DOES NOT PROTECT AGAINST INVALID INPUT.
def lay_carrier(board, rank, file, vertical):
	player1 = board[0]
	player2 = board[1]
	player1[rank,file] = 1
	if not vertical:
		for i in range(1,5):
			player1[rank+i,file] = 1
	else:
		for i in range(1,5):
			player1[rank, file+i] = 1

	x = np.random.randint(2)

	if (x ==0):
		rank2 = np.random.randint(5)
		file2 = np.random.randint(10)
		for i in range(0,5):
			player2[rank2+i, file2] = 1
	else:
		rank2 = np.random.randint(10)
		file2 = np.random.randint(5)
		for i in range(0,5):
			player2[rank2, file2+i] = 1

	return [player1, player2]

''' The next few functions are nearly identical and take the input from the play function wrapper and use that to play down the ships 
for both the user and CPU but they do not protect user from invalid inputs.
'''
def lay_battleship(board, rank, file, vertical):
	player1 = board[0]
	player2 = board[1]

	if not vertical:
		for i in range(0,4):
			player1[rank+i,file] = 1
	else:
		for i in range(0,4):
			player1[rank,file+i] = 1
	x = 1
	if (x == 0):
		rank = np.random.randint(6)
		allowed = []
		for i in range(0,10):
			flag = True
			for j in range(0,4):
				if(player2[rank+j, i] == 1 or rank+j >9):
					flag = False

			if flag:
				allowed += [i]

		np.random.shuffle(allowed)
		file = allowed[0]
		for i in range(0,4):
			player2[rank+i,file] = 1

	else:
		file = np.random.randint(6)
		allowed = []
		for i in range(0,10):
			flag = True
			for j in range(0,4):
				print(file +j)
				if (player2[i,file+j] == 1) or (file+j >9):
					flag = False
			if flag:
				allowed+= [i]
		np.random.shuffle(allowed)
		rank = allowed[0]
		
		for i in range(0,4):
			player2[rank, file+i] = 1
	return [player1, player2]


def lay_sub(board, rank, file, vertical):
	player1 = board[0]
	player2 = board[1]
	if not vertical:
		for i in range(0,3):
			player1[rank+i, file] = 1
	else:
		for i in range(0,3):
			player1[rank, file+i] = 1

	x = np.random.randint(2)
	if (x == 0):
		rank = np.random.randint(6)
		allowed = []
		for i in range(0,10):
			flag = True
			for j in range(0,3):
				if(player2[rank+j, i] == 1 or rank +j >9):
					flag = False

			if flag:
				allowed += [i]
		np.random.shuffle(allowed)
		file = allowed[0]
		for i in range(0,3):
			player2[rank+i,file] = 1

	else:
		file = np.random.randint(6)
		allowed = []
		for i in range(0,10):
			flag = True
			for j in range(0,3):
				if(player2[i,file+j] == 1 or file+j >9):
					flag = False
			if flag:
				allowed+= [i]
		np.random.shuffle(allowed)
		rank = allowed[0]
		for i in range(0,3):
			player2[rank, file+i] = 1
	return [player1, player2]

def lay_destroyer(board, rank, file, vertical):
	player1 = board[0]
	player2 = board[1]
	if not vertical:
		for i in range(0,3):
			player1[rank+i, file] = 1
	else:
		for i in range(0,3):
			player1[rank, file+i] = 1

	x = np.random.randint(2)
	if (x == 0):
		rank = np.random.randint(6)
		allowed = []
		for i in range(0,10):
			flag = True
			for j in range(0,3):
				if (player2[rank+j, i] == 1 or rank +j >9):
					flag = False

			if flag:
				allowed += [i]
		np.random.shuffle(allowed)
		file = allowed[0]
		for i in range(0,3):
			player2[rank+i,file] = 1

	else:
		file = np.random.randint(6)
		allowed = []
		for i in range(0,10):
			flag = True
			for j in range(0,3):
				if (player2[i,file+j] == 1 or file+j >9):
					flag = False
			if flag:
				allowed+= [i]
		np.random.shuffle(allowed)
		rank = allowed[0]
		for i in range(0,3):
			player2[rank, file+i] = 1
	return [player1, player2]

def lay_cruiser(board, rank, file, vertical):
	player1 = board[0]
	player2 = board[1]
	if not vertical:
		for i in range(0,2):
			player1[rank+i, file] = 1
	else:
		for i in range(0,2):
			player1[rank, file+i] = 1

	x = np.random.randint(2)
	if (x == 0):
		rank = np.random.randint(6)
		allowed = []
		for i in range(0,10):
			flag = True
			for j in range(0,2):
				if(player2[rank+j, i] == 1 or rank+j >9):
					flag = False

			if flag:
				allowed += [i]
		np.random.shuffle(allowed)
		file = allowed[0]
		for i in range(0,2):
			player2[rank+i,file] = 1

	else:
		file = np.random.randint(6)
		allowed = []
		for i in range(0,10):
			flag = True
			for j in range(0,2):
				if(player2[i,file+j] == 1 or file+j >9):
					flag = False
			if flag:
				allowed+= [i]
		np.random.shuffle(allowed)
		rank = allowed[0]
		for i in range(0,2):
			player2[rank, file+i] = 1

	print(player1)
	print(player2)
	return [player1, player2]

'''This function wraps the previous functions and provides an interface for the player to lay down their ships, but does not protect against
invalid inputs. Then once the ships are laid the function allows gameplay against a CPU that picks its firing location at random. '''
def play():
	player1, player2 = build_board()
	print(player1)
	print("Where do you want to place your carrier?")
	print("Input top left corner position: RANK FILE VERTICAL")
	a = input().split()
	for i in range(0,3):
		a[i] = int(a[i])

	player1, player2 =lay_carrier([player1,player2], a[0], a[1], a[2])
	print(player1)
	print("Where do you want to place your battleship?")
	print("Input top left corner position: RANK FILE VERTICAL")
	a = input().split()
	for i in range(0,3):
		a[i] = int(a[i])

	player1, player2 = lay_battleship([player1,player2], a[0], a[1], a[2])
	print(player1)
	print("Where do you want to place your destroyer?")
	print("Input top left corner position: RANK FILE VERTICAL")
	a = input().split()
	for i in range(0,3):
		a[i] = int(a[i])

	player1, player2 = lay_destroyer([player1,player2], a[0], a[1], a[2])
	print(player1)
	print("Where do you want to place your submarine?")
	print("Input top left corner position: RANK FILE VERTICAL")
	a = input().split()
	for i in range(0,3):
		a[i] = int(a[i])

	player1, player2 = lay_sub([player1,player2], a[0], a[1], a[2])
	print(player1)
	print("Where do you want to place your cruiser?")
	print("Input top left corner position: RANK FILE VERTICAL")
	a = input().split()
	for i in range(0,3):
		a[i] = int(a[i])

	player1, player2 = lay_cruiser([player1,player2], a[0], a[1], a[2])
	print(player1)

	print("Entering battle mode")

	count1 = 17
	count2 = 17
	cover = np.zeros((10,10))
	cells = []
	for i in range(0,9):
		for j in range(0,9):
			cells += [[i,j]]
	while count1 >0  and count2 >0:
		print(cover)
		print(player1)
		print("ENTER MISSLE COORDINATES: RANK FILE")
		a = input().split()
		for i in range(0,2):
			a[i] =int(a[i])
		if player2[a[0], a[1]] == 1:
			cover[a[0], a[1]] = 1
			count2 -= 1
			print("HIT")
		else:
			cover[a[0],a[1]] = -1
			print("MISS")

		np.random.shuffle(cells)
		fired = cells[0]
		cells = cells[1:]
		if(player1[fired[0], fired[1]] == 1):
			count1 -= 1
			player1[fired[0], fired[1]] = -8
			print("CPU HIT YOU")
		else:
			player1[fired[0], fired[1]] = -1
			print("CPU MISS")

	if count1 == 0:
		return "GAME LOST"

	else:
		return "GAME WON"


print(play())

