#!/usr/bin/env python3
#James March - 8/12/2020 Python Text Battleships. 
import os
import time
def boardcreate():
	#creates blank boards
	board = []
	for j in range(10):
	    column = []
	    for i in range(10):
	        column.append("o")
	    board.append(column)
	return board

def prettyprinter(board):
	#prints single board 
	for column in range(10):
		if column != 0:
			print("")
		print(column, end = " | ")
		for rows in range(10):
			print(board[column][rows], end =" ")
	print("\n    -------------------")
	print("    0 1 2 3 4 5 6 7 8 9\n")


def boardcreationscreen(player, orient, col, row, board):
	#prints board creation screen. Is player specific and dynamic
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Player " + str(player) + "'s Board Creation:\n")
	prettyprinter(board)
	#current placement parameters
	if orient == "H":
		print("Horizontal Ship")
	if orient == "V":
		print("Vertical Ship")
	if col != "blank":
		print("Column Number: " + str(col))
	if row != "blank":
		print("Row Number: " + str(row))

def orientation(ship):
	#orientation finder. Returns H or V depending on input.
	orient = input("Horizontal or vertical " + ship + " (H/V)? ")
	while orient != "H" and orient != "V":
		print("Incorrect input. Retry.")
		orient = input("Horizontal or vertical " + ship + " (H/V)? ")
	return orient

def numver(low, upr, rorc):
	#used to find the column/row input. Limits the input to a particular range
	#and forces type integer
	out = -1
	while low > out or upr < out:
	    try:
	        out = int(input(rorc + " Number (" + str(low) + "-" + str(upr) + ")? "))
	        if int(out) < low or int(out) > upr:
	        	print("Invalid input. Retry.")
	    except ValueError:
	        print("Invalid input. Retry.")
	return out

def placeship(ship, board, player):
	#places ship on board. is player specific. Returns the board with a new ship on it.
	#checks for overlaps, overflows and underflows. 
	p1placement = boardcreate()
	if ship == "Carrier":
		length = 5
		typechar = "C"
	elif ship == "Battleship":
		length = 4
		typechar = "B"
	elif ship == "Cruiser":
		length = 3
		typechar = "c"
	elif ship == "Submarine":
		length = 3
		typechar = "S"
	elif ship == "Destroyer":
		length = 2
		typechar = "D"
	else:
		length = input("Unknown ship type. Indicate size: ")
		length = int(length)
		typechar = "U"
	maxlength = 10-length
	#dead checks for overlaps. default is to run, changes when the overlap is non existent.
	dead = 1
	unhappy = 0
	while dead == 1:
		boardcreationscreen(player, "blank", "blank", "blank", board)
		dead = 0
		unhappy = 0
		#orientation
		orient = orientation(ship)
		#column selection and bounds checking
		#For horizontal ships, column must be less than 6
		if orient == "H":
			columnnum = numver(0, maxlength, "Column")		
			for i in range(10):
				p1placement[i][columnnum] = "X"
			boardcreationscreen(player, orient, columnnum, "blank", p1placement)

		else:
			columnnum = numver(0, 9, "Column")	
			for i in range(10):
				p1placement[i][columnnum] = "X"
			boardcreationscreen(player, orient, columnnum, "blank", p1placement)

		#row selection and bounds checking
		#for vertical ships row must be less than 6
		if orient == "V":
			rownum = numver(0, maxlength, "Row")	
			p1placement = boardcreate()
			for i in range(length):
				p1placement[rownum+i][columnnum] = typechar
			#rewrites whole screen
			boardcreationscreen(player, orient, columnnum, rownum, p1placement)

		else:
			rownum = numver(0, 9, "Row")
			p1placement = boardcreate()
			for i in range(length):
				p1placement[rownum][columnnum+i] = typechar

			#rewrites whole screen
			boardcreationscreen(player, orient, columnnum, rownum, p1placement)

		#test for empty water and player confirmation
		confirm = input("Correct Placement (Y/N)? ")
		while confirm != "Y" and confirm != "N":
			print("Invalid input. Try again.")
			confirm = input("Correct Placement (Y/N)? ")

		if confirm == "Y":
			for i in range(length):
				if orient == "H":
					if board[rownum][columnnum+i] != "o":
						dead = 1
				else:
					if board[rownum+i][columnnum] != "o":
						dead = 1
			if dead != 1:
				for i in range(length):
					if orient == "H":
						board[rownum][columnnum+i] = typechar
					else:
						board[rownum+i][columnnum] = typechar
		else:
			unhappy = 1
			dead = 1

		if dead == 1:
			if unhappy == 1:
				throw = input("Player is unhappy with the placement. Please attempt again.")
			else:
				throw = input("Ship is overlapped with another. Please attempt again.")
				boardcreationscreen(player, orient, columnnum, rownum, p1placement)
	return(board)

def gamePrettyPrinter(playerboard, attackboard):
	#printer for gameplay. prints two boards side by side. 
	print("\n         My Board                  Attack Board")
	for column in range(10):
		print(column, end = " | ")
		for rows in range(10):
			print(playerboard[column][rows], end =" ")
		print("    " + str(column), end = " | ")
		for rows in range(10):
			print(attackboard[column][rows], end =" ")
			if rows == 9:
				print("")
	print("    -------------------         --------------------")
	print("    0 1 2 3 4 5 6 7 8 9         0 1 2 3 4 5 6 7 8 9\n")

def shooting(row, column, attackboard):
	#checks if the shot connects. returns 1 if hit
	if attackboard[column][row] == "o":
		return 0
	else:
		return 1
	
def gettarget(playerboard, attackboard, player):
	#targetting screen. Checks for repeated shots and valid inputs
	while True:
		os.system('cls' if os.name == 'nt' else 'clear')
		if player == 1:
			print("Player 1's Turn!")
		else:
			print("Player 2's Turn!")
		gamePrettyPrinter(playerboard, attackboard)
		x = numver(0, 9, "Column")
		for i in range(10):
			if attackboard[i][x] == "o":
				attackboard[i][x] = "X"
		os.system('cls' if os.name == 'nt' else 'clear')
		if player == 1:
			print("Player 1's Turn!")
		else:
			print("Player 2's Turn!")
		gamePrettyPrinter(playerboard, attackboard)
		print("Column: " + str(x))
		y = numver(0, 9, "Row")
		if attackboard[y][x] == "X":
			for i in range(10):
				if attackboard[i][x] == "X":
					attackboard[i][x] = "o"
			return y, x
		throw = input("Invalid Shot. Already shot here!")
		for i in range(10):
			if attackboard[i][x] == "X":
				attackboard[i][x] = "o"

#Blank Board Creation
p1board = boardcreate()
p2board = boardcreate()
attackboard1 = boardcreate()
attackboard2 = boardcreate()

#Creation type (Dev mode selector)
creation = input("Do you want to manually enter ships? (Y/N) ")
while creation != "Y" and creation != "N":
	print("Invalid. Try again.")
	creation = input("Do you want to manually enter ships? (Y/N) ")
if creation == "Y":
	#manual creation
	board1 = placeship("Carrier", p1board, 1)
	board1 = placeship("Battleship", p1board, 1)
	board1 = placeship("Cruiser", p1board, 1)
	board1 = placeship("Submarine", p1board, 1)
	board1 = placeship("Destroyer", p1board, 1)
	board2 = placeship("Carrier", p2board, 2)
	board2 = placeship("Battleship", p2board, 2)
	board2 = placeship("Cruiser", p2board, 2)
	board2 = placeship("Submarine", p2board, 2)
	board2 = placeship("Destroyer", p2board, 2)
else:
	#Schematic Board Creation
	board1 = boardcreate()
	for i in range(5):
		board1[0][i] = "C"
	for i in range(4):
		board1[1][i] = "B"
	for i in range(3):
		board1[2][i] = "c"
	for i in range(3):
		board1[3][i] = "S"
	for i in range(2):
		board1[4][i] = "D"
	board2 = boardcreate()
	for i in range(5):
		board2[0][i] = "C"
	for i in range(4):
		board2[1][i] = "B"
	for i in range(3):
		board2[2][i] = "c"
	for i in range(3):
		board2[3][i] = "S"
	for i in range(2):
		board2[4][i] = "D"

#blank the screen. setup win variables
os.system('cls' if os.name == 'nt' else 'clear')
player1score = 0
player2score = 0
#infinite loop for game
while True:
	#Player 1
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Player 1's Turn!")
	gamePrettyPrinter(board1, attackboard1)
	#get shot location
	shot = gettarget(board1, attackboard1, 1)
	column = shot[0]
	row = shot[1]
	attackboard1[column][row] = "X"
	print("...")
	time.sleep(1)
	print("...")
	time.sleep(1)
	#check for hit or miss.
	if shooting(row, column, board2) == 1:
		print("HIT!")
		player1score = player1score+1
		board2[column][row] = "H"
		attackboard1[column][row] = "H"
	else:		
		print("Miss.")
		board2[column][row] = "X"
		attackboard1[column][row] = "M"
	#check if the player won
	if player1score == 17:
		print("Player 1 wins!")
		exit()
	#end the turn and blank the screen for the next player.
	throw = input("Player 1's turn is over. Press enter to confirm")
	os.system('cls' if os.name == 'nt' else 'clear')
	throw = input("Player 2's Turn! Press enter when ready to view your board!.")

	#Player 2
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Player 2's Turn!")
	gamePrettyPrinter(board2, attackboard2)
	#get shot location
	shot = gettarget(board2, attackboard2, 2)
	column = shot[0]
	row = shot[1]
	attackboard2[column][row] = "X"
	print("...")
	time.sleep(1)
	print("...")
	time.sleep(1)
	#check for hit or miss
	if shooting(row, column, board1) == 1:
		print("HIT!")
		player2score = player2score+1
		board1[column][row] = "H"
		attackboard2[column][row] = "H"
	else:
		print("Miss.")
		board1[column][row] = "X"
		attackboard2[column][row] = "M"
	#check if the player won
	if player2score == 17:
		print("Player 2 wins!")
		exit()
	#end the turn and blank the screen for the next player.
	throw = input("Player 2's turn is over. Press enter to confirm.")
	os.system('cls' if os.name == 'nt' else 'clear')
	throw = input("Player 1's Turn! Press enter when ready to view your board.")