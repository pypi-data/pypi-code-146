from sys import maxsize
from itertools import permutations
import numpy as np
import random
from time import sleep
import os
import time

def isprime(num):
    if num > 1:
        for i in range(2,num):
            if (num % i) == 0:
                return str(num)+" is not a prime number"
                break
        else:                           # see the indentation of else not below if below for
            return str(num)+" is a prime number"
    else:
        return str(num)+" is not a prime number"

def tsp(graph, s):
	vertex = []            # store all vertex apart from source vertex
	for i in range(len(graph)):
		if i != s:
			vertex.append(i)
	min_path = maxsize         # store minimum weight Hamiltonian Cycle
	next_permutation=permutations(vertex)
	for i in next_permutation:
		current_pathweight = 0     # store current Path weight(cost)
		k = s          # compute current path weight
		for j in i:
			current_pathweight += graph[k][j]
			k = j
		current_pathweight += graph[k][s]
		min_path = min(min_path, current_pathweight)    # update minimum
	return min_path

def nqueen(N):
    board = [[0]*N for _ in range(N)] #or board = [[0]*N]*N
    def attack(i, j):
        for k in range(0,N):    #checking vertically and horizontally
            if board[i][k]==1 or board[k][j]==1:
                return True
        for k in range(0,N):    #checking diagonally
            for l in range(0,N):
                if (k+l==i+j) or (k-l==i-j):
                    if board[k][l]==1:
                        return True
        return False
    def N_queens(n):
        if n==0:
            return True
        for i in range(0,N):
            for j in range(0,N):
                if (not(attack(i,j))) and (board[i][j]!=1):
                    board[i][j] = 1
                    if N_queens(n-1)==True:
                        return True
                    board[i][j] = 0
        return False
    N_queens(N)
    return board

def longtictactoe():
    def create_board():
        return (np.array([[0, 0, 0],[0, 0, 0],[0, 0, 0]]))
    def possibilities(board):
        l = []
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    l.append((i, j))
        return(l)
    def random_place(board, player):
        selection = possibilities(board)
        current_loc = random.choice(selection)
        board[current_loc] = player
        return(board)
    def row_win(board, player):
        for x in range(len(board)):
            win = True
            for y in range(len(board)):
                if board[x, y] != player:
                    win = False
                    continue
            if win == True:
                return(win)
        return(win)
    def col_win(board, player):
        for x in range(len(board)):
            win = True
            for y in range(len(board)):
                if board[y][x] != player:
                    win = False
                    continue

            if win == True:
                return(win)
        return(win)
    def diag_win(board, player):
        win = True
        y = 0
        for x in range(len(board)):
            if board[x, x] != player:
                win = False
        if win:
            return win
        win = True
        if win:
            for x in range(len(board)):
                y = len(board) - 1 - x
                if board[x, y] != player:
                    win = False
        return win
    def evaluate(board):
        winner = 0
        for player in [1, 2]:
            if (row_win(board, player) or col_win(board, player) or diag_win(board, player)):
                winner = player
        if np.all(board != 0) and winner == 0:
            winner = -1
        return winner
    def play_game():
        board, winner, counter = create_board(), 0, 1
        print(board)
        sleep(2)
        while winner == 0:
            for player in [1, 2]:
                board = random_place(board, player)
                print("Board after " + str(counter) + " move")
                print(board)
                sleep(2)
                counter += 1
                winner = evaluate(board)
                if winner != 0:
                    break
        return(winner)
    print("Winner is: " + str(play_game()))

board = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
player = 1
Win = 1
Draw = -1
Running = 0
Stop = 1
Game = Running
Mark = 'X'
def DrawBoard():
    print(" %c | %c | %c " % (board[1],board[2],board[3]))
    print("___|___|___")
    print(" %c | %c | %c " % (board[4],board[5],board[6]))
    print("___|___|___")
    print(" %c | %c | %c " % (board[7],board[8],board[9]))
    print("   |   |   ")

def CheckPosition(x):
    if(board[x] == ' '):
        return True
    else:
        return False

def CheckWin():
    global Game
    #Horizontal winning condition
    if(board[1] == board[2] and board[2] == board[3] and board[1] != ' '):
        Game = Win
    elif(board[4] == board[5] and board[5] == board[6] and board[4] != ' '):
        Game = Win
    elif(board[7] == board[8] and board[8] == board[9] and board[7] != ' '):
        Game = Win
    #Vertical Winning Condition
    elif(board[1] == board[4] and board[4] == board[7] and board[1] != ' '):
        Game = Win
    elif(board[2] == board[5] and board[5] == board[8] and board[2] != ' '):
        Game = Win
    elif(board[3] == board[6] and board[6] == board[9] and board[3] != ' '):
        Game=Win
    #Diagonal Winning Condition
    elif(board[1] == board[5] and board[5] == board[9] and board[5] != ' '):
        Game = Win
    elif(board[3] == board[5] and board[5] == board[7] and board[5] != ' '):
        Game=Win
    #Match Tie or Draw Condition
    elif(board[1]!=' ' and board[2]!=' ' and board[3]!=' ' and board[4]!=' ' and board[5]!=' ' and board[6]!=' ' and board[7]!=' ' and board[8]!=' ' and board[9]!=' '):
        Game=Draw
    else:        
        Game=Running

def tictactoe():
    global board
    board = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
    global player
    player = 1
    global Win
    Win = 1
    global Draw
    Draw = -1
    global Running
    Running = 0
    global Stop
    Stop = 1
    global Game
    Game = Running
    global Mark
    Mark = 'X'
    print("Player 1 [X] --- Player 2 [O]\n")
    print()
    print("Please Wait...")
    time.sleep(2)
    while(Game == Running):
        os.system('cls')
        DrawBoard()
        if(player % 2 != 0):
            print("Player 1's chance")
            Mark = 'X'
        else:
            print("Player 2's chance")
            Mark = 'O'
        choice = int(input("Enter the position between [1-9] where you want to mark : "))
        if(CheckPosition(choice)):
            board[choice] = Mark
            player+=1
            CheckWin()

    os.system('cls')
    DrawBoard()
    if(Game==Draw):
        print("Game Draw")
    elif(Game==Win):
        player-=1
        if(player%2!=0):
            print("Player 1 Won")
        else:
            print("Player 2 Won")

ai_programs = ['p_multiplicationtable','p_primeornot','p_factorial','p_list_operations','p_list_methods','p_chatbot','p_set_operation','p_count_s1_in_s2','p_dictionary_operations','p_n_queen','p_tsp','p_longtictactoe']

sql_programs = ['p_library','p_order','p_movie','p_college','p_comp']

def p_multiplicationtable():
    return r"""
n=int(input("Enter the number of which the user wants to print the multiplication table: "))
print("multiplication table of ",n," is")
for i in range(1,11):
    print(n,"X",i,"=",n*i)
    """

def p_primeornot():
    return r"""
num=int(input("Enter the number that is to checked prime or not: "))
if num > 1:
    for i in range(2,num):
        if (num % i) == 0:
            print(num, "is not a prime number")
            break
    else: 
        print(num, "is a prime number")
else:
    print(num, "is not a prime number")
    """

def p_factorial():
    return r"""
n = int(input("Enter the nos whose factorial needs to be found: "))
fact = 1
if n<0:
    print("cannot find the factorial of negetive number")
else:
    if n==0:
        print("factorial of 0 is 1")
    else:
        for i in range(1,n+1):
            fact = fact*i
        print("factorial of number ",n," (",n,"!) is ",fact)
    """

def p_list_methods():
    return r"""
print("========= append to list ===========")
L1 = ['hello', 'how', 'are']
print("The list before appending is: ",L1)
L1.append('you')
print("The list after appending 'you' is: ",L1)

print("========= insert to list ===========")
L1 = ['hello', 'how', 'are','you']
print("The list before insertion is: ",L1)
L1.insert(1,'shreesha')
print("The list after adding 'shreesha' to 2nd position is: \n",L1)

print("========= extend list ===========")
L1 = ['hello', 'how', 'are']
L2 = ['i', 'fine', 1, 2]
print("The is 1st list is: ",L1)
print("The is 2nd list is: ",L2)
L1.extend(L2)
print("after the extention of list 1 it becomes : \n",L1)

print("========= delete using remove ===========")
L1 = ['hello', 'how', 'are','you']
print("The is list before removing is: ",L1)
L1.remove('hello')
print("The is list after removing 'hello' is: ",L1)

print("========= delete using pop ===========")
L1 = ['hello', 'how','are','you']
print("The is list before poping is: ",L1)
L1.pop()
print("The is list after poping from last is: ",L1)

print("========= delete using del ===========")
L1 = ['hello', 'how', 'are','you']
print("The is list before deleting is: ",L1)
del L1[1]
print("The is list after deleting 2nd element is: ",L1)
    """

def p_list_operations():
    return r"""
print("========== nested list ==============")
nested_list = [1,[2,3],'hi',['hello','world']]
print("The nested list is ",nested_list)
print("nested_list[0] : ",nested_list[0])
print("nested_list[-1][-1]: ",nested_list[-1][-1])

print("========== length of list ==============")
L1 = ['hello','how','are','you']
print("The list is ",L1)
print("The length of list ",len(L1))

print("========== concatination list ==============")
L1 = ['hello','how','are','you']
L2 = ['i am','fine',1,2]
print("The list 1  is ",L1)
print("The list 2  is ",L2)
L3 = L1+L2
print("The concatination of list 1 and 2 is ",L3)

print("========== membership list ==============")
L1 = ['hello','how','are','you']
print("The list is ",L1)
ans1 = 'apple' in L1
print("checking is 'apple' in the list ",ans1)
ans2 = 'hello' in L1
print("checking is 'hello' in the list ",ans2)

print("========== iteration list ==============")
L1 = ['hello','how','are','you']
print("The list is ",L1)
print("printing element of list")
for i in L1:
    print(i)

print("========== indexing list ==============")
L1 = ['hello','how','are','you']
print("The list is ",L1)
print("printing individual element of list")
print(L1[0])
print(L1[1])

print("========== slicing list ==============")
L1 = ['hello','how','are','you']
print("The list is ",L1)
print("The L1[0:3]: ",L1[0:3])

print("========== replication list ==============")
L2 = ['i am','fine',1,2]
print("The list is ",L2)
L4 = L2 * 3
print("The list after replicating 3 times is ",L4)
    """

def p_chatbot():
    return r"""
print("Simple question and answering program")
print("======================================================")
print("hi")
print("how are you")
print("what is your name")
print("are you studing")
print("what did you do yesterday")
print("what is your hobby")
print("your fav color")
print("your fav singer")
print("any future plans")
print("are you hungry now")
print("quit")
print("======================================================")
while True:
    question = input("enter any one question from the list: ")
    if question in ["hi"]:
        print("hello")
    elif question in ["how are you"]:
        print("fine")
    elif question in ["what is your name"]:
        print("shreesha")
    elif question in ["are you studing"]:
        print("no")
    elif question in ["what did you do yesterday"]:
        print("gone to hospital")
    elif question in ["what is your hobby"]:
        print("drawing")
    elif question in ["your fav color"]:
        print("green")
    elif question in ["your fav singer"]:
        print("shreya")
    elif question in ["any future plans"]:
        print("become teacher")
    elif question in ["are you hungry now"]:
        print("no")
    elif question in ["quit"]:
        print("thank you")
        break
    else:
        print("I don't understand what are you saying")
    """

def p_set_operation():
    return r"""
a = {2,4,6,8}
b = {1,2,3,4,5}
print("Set A = ",a,"Set B = ",b)
print("union of A & B (A U B)= ",a|b)
print("Intersection of A & B (A ^ B) = ",a&b)
print("Set difference  of B and A (A-B) = ",a-b)
print("Set symmetric difference(disjunctive union) of A and B (A-B)U(B-A) = ",(a-b)|(b-a))
print("Set symmetric difference(disjunctive union) of A and B (A ^ B) = ",a^b)
    """

def p_count_s1_in_s2():
    return r"""
s1 = input("Enter the substring: ").lower()
s2 = input("Enter the string: ").lower()
count = s2.count(s1)
print("The substring",s1,"string occured in string",s2,count,"times")
    """

def p_dictionary_operations():
    return r"""
print("Dictionary Operations".center(55,'-'))

my_dict = {'name':'shreesha','age':20,'gender':'male'}
print("\naccessing values with []")
print(my_dict['name'])
print("\naccessing values with get() method")
print(my_dict.get('age'))
print("\naccessing non existing values with get() method")
print(my_dict.get('address','do not exist'))
print("\naccessing non existing values with [] error handeled")
try:
    print(my_dict['address'])
except:
    print("error:  KeyError")
    
print("-".center(55,'-'))
print("without keys and values".center(55,'-'))
statecapital = {'gujarat':'gandhinagar','maharastra':'mumbai','rajastan':'jaipur','bihar':'patna'}
print("\nThe states and capital : ",statecapital)
print("\naccessing keys without using keys()")
for state in statecapital:
    print(state)
print("\naccessing keys without using values()")
for capital in statecapital:
    print(statecapital[capital])

print("keys and values".center(55,'-'))
print("\naccessing keys with using keys()")
keys = statecapital.keys()
print("keys: ",keys) 
print("\naccessing keys with using values()")
values = statecapital.values()
print("values: ",values)
print("\naccessing keys and values with using items()")
for i in statecapital.items():
	print(i)

print("in operators".center(55,'-'))
spam = {'name':'shreesha','age':7,'color':'white'}
print('spam =',spam)
res1 = 'name' in spam.keys()
print("'name' in spam.keys(): ",end='')
print(res1)
res2 = 'nature' in spam.keys()
print("'nature' in spam.keys(): ",res2)
print("-".center(55,'-'))

print("not in operators".center(55,'-'))
res3 = 'name' not in spam.keys()
print("'name' not in spam.keys(): ",res3)
res4 = 'shreesha' not in spam.values()
print("'shreesha' not in spam.values(): ",res4)
res5 = 8 not in spam.values()
print("8 not in spam.values(): ",res5)
    """

def p_tictactoe():
    return r'''
import os
import time

board = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
player = 1
Win = 1
Draw = -1
Running = 0
Stop = 1
Game = Running
Mark = 'X'

def DrawBoard():
    print(" %c | %c | %c " % (board[1],board[2],board[3]))
    print("___|___|___")
    print(" %c | %c | %c " % (board[4],board[5],board[6]))
    print("___|___|___")
    print(" %c | %c | %c " % (board[7],board[8],board[9]))
    print("   |   |   ")

def CheckPosition(x):
    if(board[x] == ' '):
        return True
    else:
        return False

def CheckWin():
    global Game
    if(board[1] == board[2] and board[2] == board[3] and board[1] != ' '):
        Game = Win
    elif(board[4] == board[5] and board[5] == board[6] and board[4] != ' '):
        Game = Win
    elif(board[7] == board[8] and board[8] == board[9] and board[7] != ' '):
        Game = Win
    elif(board[1] == board[4] and board[4] == board[7] and board[1] != ' '):
        Game = Win
    elif(board[2] == board[5] and board[5] == board[8] and board[2] != ' '):
        Game = Win
    elif(board[3] == board[6] and board[6] == board[9] and board[3] != ' '):
        Game=Win
    elif(board[1] == board[5] and board[5] == board[9] and board[5] != ' '):
        Game = Win
    elif(board[3] == board[5] and board[5] == board[7] and board[5] != ' '):
        Game=Win
    elif(board[1]!=' ' and board[2]!=' ' and board[3]!=' ' and board[4]!=' ' and board[5]!=' ' and board[6]!=' ' and board[7]!=' ' and board[8]!=' ' and board[9]!=' '):
        Game=Draw
    else:        
        Game=Running

print("Player 1 [X] --- Player 2 [O]\n")
print()
print()
print("Please Wait...")
time.sleep(10)
while(Game == Running):
    os.system('cls')
    DrawBoard()
    if(player % 2 != 0):
        print("Player 1's chance")
        Mark = 'X'
    else:
        print("Player 2's chance")
        Mark = 'O'
    choice = int(input("Enter the position between [1-9] where you want to mark : "))
    if(CheckPosition(choice)):
        board[choice] = Mark
        player+=1
        CheckWin()

os.system('cls')
DrawBoard()
if(Game==Draw):
    print("Game Draw")
elif(Game==Win):
    player-=1
    if(player%2!=0):
        print("Player 1 Won")
    else:
        print("Player 2 Won")
    '''

def p_dfs():
    print("""
# 3 water jugs capacity -> (x,y,z) where x>y>z
# initial state (12,0,0)
# final state (6,6,0)

capacity = (12,8,5) 
# Maximum capacities of 3 jugs -> x,y,z
x = capacity[0]
y = capacity[1]
z = capacity[2]

# to mark visited states
memory = {}

# store solution path
ans = []

def get_all_states(state):
	# Let the 3 jugs be called a,b,c
	a = state[0]
	b = state[1]
	c = state[2]

	if(a==6 and b==6):
		ans.append(state)
		return True

	# if current state is already visited earlier
	if((a,b,c) in memory):
		return False

	memory[(a,b,c)] = 1

	#empty jug a
	if(a>0):
		#empty a into b
		if(a+b<=y):
			if( get_all_states((0,a+b,c)) ):
				ans.append(state)
				return True
		else:
			if( get_all_states((a-(y-b), y, c)) ):
				ans.append(state)
				return True
		#empty a into c
		if(a+c<=z):
			if( get_all_states((0,b,a+c)) ):
				ans.append(state)
				return True
		else:
			if( get_all_states((a-(z-c), b, z)) ):
				ans.append(state)
				return True

	#empty jug b
	if(b>0):
		#empty b into a
		if(a+b<=x):
			if( get_all_states((a+b, 0, c)) ):
				ans.append(state)
				return True
		else:
			if( get_all_states((x, b-(x-a), c)) ):
				ans.append(state)
				return True
		#empty b into c
		if(b+c<=z):
			if( get_all_states((a, 0, b+c)) ):
				ans.append(state)
				return True
		else:
			if( get_all_states((a, b-(z-c), z)) ):
				ans.append(state)
				return True

	#empty jug c
	if(c>0):
		#empty c into a
		if(a+c<=x):
			if( get_all_states((a+c, b, 0)) ):
				ans.append(state)
				return True
		else:
			if( get_all_states((x, b, c-(x-a))) ):
				ans.append(state)
				return True
		#empty c into b
		if(b+c<=y):
			if( get_all_states((a, b+c, 0)) ):
				ans.append(state)
				return True
		else:
			if( get_all_states((a, y, c-(y-b))) ):
				ans.append(state)
				return True

	return False

initial_state = (12,0,0)
print("Starting work...\n")
get_all_states(initial_state)
ans.reverse()
for i in ans:
	print(i)      
    """)

def p_bfs():
    print("""
from collections import deque

def BFS(a, b, target):

	# Map is used to store the states, every   # state is hashed to binary value to 	
    # indicate either that state is visited before or not
	m = {}
	isSolvable = False
	path = []

	# Queue to maintain states
	q = deque()

	# Initialing with initial state
	q.append((0, 0))

	while (len(q) > 0):

		# Current state
		u = q.popleft()

		# q.pop() #pop off used state

		# If this state is already visited
		if ((u[0], u[1]) in m):
			continue

		# Doesn't met jug constraints
		if ((u[0] > a or u[1] > b or
			u[0] < 0 or u[1] < 0)):
			continue

		# Filling the vector for constructing
		# the solution path
		path.append([u[0], u[1]])

		# Marking current state as visited
		m[(u[0], u[1])] = 1

		# If we reach solution state, put ans=1
		if (u[0] == target or u[1] == target):
			isSolvable = True

			if (u[0] == target):
				if (u[1] != 0):

					# Fill final state
					path.append([u[0], 0])
			else:
				if (u[0] != 0):

					# Fill final state
					path.append([0, u[1]])

			# Print the solution path
			sz = len(path)
			for i in range(sz):
				print("(", path[i][0], ",",
					path[i][1], ")")
			break

		# If we have not reached final state
		# then, start developing intermediate
		# states to reach solution state
		q.append([u[0], b]) # Fill Jug2
		q.append([a, u[1]]) # Fill Jug1

		for ap in range(max(a, b) + 1):

			# Pour amount ap from Jug2 to Jug1
			c = u[0] + ap
			d = u[1] - ap

			# Check if this state is possible or not
			if (c == a or (d == 0 and d >= 0)):
				q.append([c, d])

			# Pour amount ap from Jug 1 to Jug2
			c = u[0] - ap
			d = u[1] + ap

			# Check if this state is possible or not
			if ((c == 0 and c >= 0) or d == b):
				q.append([c, d])

		# Empty Jug2
		q.append([a, 0])

		# Empty Jug1
		q.append([0, b])

	# No, solution exists if ans=0
	if (not isSolvable):
		print("No solution")

# Driver code
if __name__ == '__main__':

	Jug1, Jug2, target = 4, 3, 2
	print("Path from initial state "
		"to solution state ::")

	BFS(Jug1, Jug2, target)
    """)

def p_ao_star():
    print("""
from heapq import heappush, heappop

def ao_star(start, goal, neighbors, heuristic):
  # Initialize the open set and the closed set
  open_set = [(heuristic(start, goal), start)]
  closed_set = set()

  # Initialize the g-score (the cost to get from the start to a given node) and the f-score (the estimated total cost to get from the start to the goal through a given node)
  g_score = {start: 0}
  f_score = {start: heuristic(start, goal)}

  # Initialize the came_from dictionary, which will be used to reconstruct the path from the start to the goal
  came_from = {}

  # While there are nodes in the open set
  while open_set:
    # Find the node in the open set with the lowest f-score
    current = heappop(open_set)[1]

    # If the current node is the goal, we have found the path
    if current == goal:
      return reconstruct_path(came_from, current)

    # Add the current node to the closed set
    closed_set.add(current)

    # Consider each of the current node's neighbors
    for neighbor in neighbors(current):
      # If the neighbor is already in the closed set, skip it
      if neighbor in closed_set:
        continue

      # Calculate the tentative g-score for the neighbor (the cost to get from the start to the neighbor)
      tentative_g_score = g_score[current] + 1

      # If the neighbor is not in the open set, or if the new g-score is lower than the existing g-score, update the g-score and f-score of the neighbor and add it to the open set
      if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
        came_from[neighbor] = current
        g_score[neighbor] = tentative_g_score
        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
        heappush(open_set, (f_score[neighbor], neighbor))

  # If we get here, it means that we have not found a path from the start to the goal
  return None

def reconstruct_path(came_from, current):
  # Base case: we are at the start
  if current in came_from:
    return reconstruct_path(came_from, came_from[current]) + [current]
  else:
    return [current]
# Define the graph as a dictionary of node: neighbor_list pairs
graph = {
  'A': ['B', 'C', 'D'],
  'B': ['A', 'E', 'F'],
  'C': ['A', 'G', 'H'],
  'D': ['A', 'I', 'J'],
  'E': ['B'],
  'F': ['B'],
  'G': ['C'],
  'H': ['C'],
  'I': ['D'],
  'J': ['D']
}

# Define a function to return the neighbors of a given node
def get_neighbors(node):
  return graph[node]

# Define a heuristic function that estimates the cost to get from one node to another
# In this example, we use the Manhattan distance as the heuristic

def manhattan_distance(node1, node2):
  # Check that both node1 and node2 have at least two characters
  if len(node1) < 2 or len(node2) < 2:
    return 0

  # Calculate the x and y distance between the two nodes
  x_distance = abs(ord(node1[0]) - ord(node2[0]))
  y_distance = abs(int(node1[1]) - int(node2[1]))

  # Return the sum of the x and y distances
  return x_distance + y_distance

'''
#OR 


def manhattan_distance(node1, node2):
  try:
    # Calculate the x and y distance between the two nodes
    x_distance = abs(ord(node1[0]) - ord(node2[0]))
    y_distance = abs(int(node1[1]) - int(node2[1]))

    # Return the sum of the x and y distances
    return x_distance + y_distance
  except IndexError:
    # If an index error occurs, return 0
    return 0
'''

# Find the shortest path from node 'A' to node 'H' using the AO* algorithm
path = ao_star('A', 'H', get_neighbors, manhattan_distance)

# Print the path
print(path)
    """)


def p_forward_chain_v1():
    print("""
# define the starting information
information = "I have a problem and need to find a solution"

# define the steps to take to find a solution
steps = ["identify the problem", "generate potential solutions", "evaluate potential solutions", "implement a solution"]

# start with the available information and work forwards
print(information)
for step in steps:
    print(step)
    """)

def p_forward_chain_v2():
    print("""
# Define the initial state
initial_state = ["dirty", "smelly"]

# Define the rules
rules = [
    {"if": ["dirty"], "then": ["clean"]},
    {"if": ["clean", "smelly"], "then": ["fresh"]},
]

# Define the goal
goal = ["fresh"]

# Initialize the current state
current_state = initial_state

# Apply the rules until the goal is reached
while not all(x in current_state for x in goal):
    for rule in rules:
        if all(x in current_state for x in rule["if"]):
            current_state += rule["then"]

# Print the final state
print("The final state is:", current_state)
    """)


def p_backward_chain_v1():
    print("""
goal = "find a solution to the problem"

# define the necessary steps to achieve the goal
steps = ["identify the problem", "generate potential solutions", "evaluate potential solutions", "implement a solution"]

# start with the goal and work backwards
print(goal)
for step in reversed(steps):
    print(step)
    """)

def p_backward_chain_v2():
    print("""
# Define the initial state
initial_state = ["fresh"]

# Define the rules
rules = [
    {"if": ["clean", "smelly"], "then": ["fresh"]},
    {"if": ["dirty"], "then": ["clean"]},
]

# Define the goal
goal = ["dirty", "smelly"]

# Initialize the current state
current_state = initial_state

# Apply the rules until the goal is reached
while not all(x in current_state for x in goal):
    # Check if the goal is already present in the current state
    if all(x in current_state for x in goal):
        break
    # Otherwise, apply the rules in reverse order
    for rule in reversed(rules):
        if all(x in current_state for x in rule["then"]):
            current_state += rule["if"]

# Print the final state
print("The final state is:", current_state)
    """)

def p_fopl():
    print("""
def resolution(kb, alpha):
  clauses = kb + [[-1 * l for l in alpha]]
  new = []
  while True:
    n = len(clauses)
    pairs = [(i, j) for i in range(n) for j in range(i+1, n)]
    for (i, j) in pairs:
      resolvents = resolve(clauses[i], clauses[j])
      if [] in resolvents:
        return True
      new += resolvents
    if new == []:
      return False
    clauses += new
    new = []

def resolve(ci, cj):
  resolvents = []
  for li in ci:
    for lj in cj:
      if li == -1 * lj or lj == -1 * li:
        resolvent = [l for l in ci if l != li] + [l for l in cj if l != lj]
        resolvent = list(set(resolvent))
        if resolvent not in resolvents:
          resolvents.append(resolvent)
  return resolvents

# Example usage
kb = [['A', 'B'], ['C', '-D']]
alpha = [['A', '-B']]
result = resolution(kb, alpha)
print(result) # should print True
    """)


def p_n_queen():
    return """
print ("Enter the number of queens")
N = int(input())
board = [[0]*N for _ in range(N)] 
def attack(i, j):
    for k in range(0,N):
        if board[i][k]==1 or board[k][j]==1:
            return True
    for k in range(0,N):
        for l in range(0,N):
            if (k+l==i+j) or (k-l==i-j):
                if board[k][l]==1:
                    return True
    return False
def N_queens(n):
    if n==0:
        return True
    for i in range(0,N):
        for j in range(0,N):
            if (not(attack(i,j))) and (board[i][j]!=1):
                board[i][j] = 1
                if N_queens(n-1)==True:
                    return True
                board[i][j] = 0
    return False
N_queens(N)
for i in board:
    print (i)
    """

def p_tsp():
    return """
from sys import maxsize
from itertools import permutations
def tsp(graph,s):
    vertex=[]
    for i in range(v):
        if i!=s:
            vertex.append(i)
    min_path = maxsize
    nextp = permutations(vertex)
    for i in nextp:
        cost = 0
        k = s
        for j in i:
            cost += graph[k][j]
            k=j
        cost += graph[k][s]
        min_path = min(min_path,cost)
    return min_path
v=4
graph = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]
s=0
print(tsp(graph,s))
    """

def p_library():
    return """
create database vp20ai027_LIBRARY;
use vp20ai027_LIBRARY;

create table PUBLISHER
(
	Name varchar(10),
	Address varchar(10),
	Phone bigint,
	primary key(Name)
);
create table BOOK
(
	Book_id varchar(5),
	Title varchar(20),
	Publisher_Name varchar(10),
	Publisher_year int,
	primary key(Book_id),
	foreign key(Publisher_Name) references PUBLISHER(Name) on delete cascade
);
create table BOOK_AUTHORS
(
	Book_id varchar(5),
	Author_name varchar(15),
	primary key(Book_id),
	foreign key(Book_id) references BOOK(Book_id) on delete cascade
);
create table LIBRARY_BRANCH
(
	Branch_id varchar(5),
	Branch_name varchar(10),
	Address varchar(15),
	primary key(Branch_id)

);
create table BOOK_COPIES
(
	Book_id varchar(5),
	Branch_id varchar(5),
	No_of_copies int,
	primary key(Book_id,Branch_id),
	foreign key(Book_id) references BOOK(Book_id) on delete cascade,
	foreign key(Branch_id) references LIBRARY_BRANCH(Branch_id) on delete cascade
);
create table BOOK_LENDING
(
	Book_id varchar(5),
	Branch_id varchar(5),
	Card_no varchar(5),
	Date_out date,
	Due_date date,
	primary key(Book_id,Branch_id,Card_no),
	foreign key(Book_id) references BOOK(Book_id) on delete cascade,
	foreign key(Branch_id) references LIBRARY_BRANCH(Branch_id) on delete cascade
);

show tables;

desc PUBLISHER;
desc BOOK;
desc BOOK_AUTHORS;
desc LIBRARY_BRANCH;
desc BOOK_COPIES;
desc BOOK_LENDING;

insert into PUBLISHER values('mcgraw','bangalore','9191919191');
insert into PUBLISHER values('pearson','newdelhi','8181818181');
insert into PUBLISHER values('planeta','bangalore','5151515151');
insert into PUBLISHER values('livre','chennai','6161616161');

insert into BOOK values('1','ME','mcgraw','2001');
insert into BOOK values('2','PP','mcgraw','2001');
insert into BOOK values('3','DBMS','pearson','2009');
insert into BOOK values('4','ATC','planeta','2009');
insert into BOOK values('5','AI','pearson','2014');

insert into BOOK_AUTHORS values('1','navathe');
insert into BOOK_AUTHORS values('2','navathe');
insert into BOOK_AUTHORS values('3','edward');
insert into BOOK_AUTHORS values('4','galvin');
insert into BOOK_AUTHORS values('5','angel');

insert into LIBRARY_BRANCH values('11','RNSIT','bangalore');
insert into LIBRARY_BRANCH values('12','VTU','bangalore');
insert into LIBRARY_BRANCH values('13','NITTE','bangalore');
insert into LIBRARY_BRANCH values('14','MANIPAL','mangalore');
insert into LIBRARY_BRANCH values('15','VCET','udupi');

insert into BOOK_COPIES values('1','11',10);
insert into BOOK_COPIES values('1','13',20);
insert into BOOK_COPIES values('1','14',15);

insert into BOOK_COPIES values('2','11',9);
insert into BOOK_COPIES values('2','12',10);
insert into BOOK_COPIES values('2','13',5);

insert into BOOK_COPIES values('3','12',4);
insert into BOOK_COPIES values('4','14',3);
insert into BOOK_COPIES values('5','11',7);

insert into BOOK_LENDING values('5','11','101','2017-03-11','2017-05-10');
insert into BOOK_LENDING values('3','14','102','2017-01-14','2017-04-04');
insert into BOOK_LENDING values('4','12','105','2017-04-16','2017-06-07');

insert into BOOK_LENDING values('1','12','103','2017-01-01','2017-06-11');
insert into BOOK_LENDING values('2','11','103','2017-01-11','2017-06-10');
insert into BOOK_LENDING values('3','15','103','2017-01-15','2017-06-15');
insert into BOOK_LENDING values('4','14','103','2017-02-21','2017-06-20');

insert into BOOK_LENDING values('3','15','104','2017-01-01','2017-06-20');
insert into BOOK_LENDING values('4','11','104','2017-01-02','2017-06-21');
insert into BOOK_LENDING values('2','11','104','2017-01-20','2017-05-18');

select * from PUBLISHER;
select * from BOOK;
select * from BOOK_AUTHORS;
select * from LIBRARY_BRANCH;
select * from BOOK_COPIES;
select * from BOOK_LENDING;

commit;

/* queries 1 -- Retrieve details of all books in the library – id, title, name of publisher, authors, number of copies 
in each branch, etc.*/

select B.Book_id, B.Title, B.Publisher_Name, BA.Author_name,BC.Branch_id,BC.No_of_copies
from BOOK B, BOOK_AUTHORS BA, BOOK_COPIES BC
where B.Book_id = BC.Book_id
and B.Book_id = BA.Book_id ;

/* queries 2 -- Get the particulars of borrowers who have borrowed more than 3 books, but from Jan 2017 to Jun
2017 */

select Card_no
from BOOK_LENDING B
where Date_out between '2017-01-01' and '2017-06-30'
group by card_no
having count(*)>3 ;

/* queries 4 -- Partition the BOOK table based on year of publication. Demonstrate its working with a simple
query. */

/*  other internet queries 
create view V_PUBLICATION as
select Publisher_year
from BOOK;

select * from V_PUBLICATION;
*/

/* lab manual */
create table BOOK1
(
	Book_id varchar(5),
	Title varchar(20),
	Publisher_Name varchar(10),
	Publisher_year int,
	primary key(Book_id,Publisher_year)
)
partition by range(Publisher_year)
(
	partition p1 values less than (2002), 
	partition p2 values less than (2010),
	partition p3 values less than (maxvalue)
);

insert into BOOK1 values('1','ME','mcgraw','2001');
insert into BOOK1 values('2','PP','mcgraw','2001');
insert into BOOK1 values('3','DBMS','pearson','2009');
insert into BOOK1 values('4','ATC','planeta','2009');
insert into BOOK1 values('5','AI','pearson','2014');

select * from BOOK1 partition(p1);
select * from BOOK1 partition(p2);
select * from BOOK1 partition(p3);

/* queries 5 -- create a view of all books and its number of copies that are currently available in the library. */

create view available as
(
	select Book_id, sum(No_of_copies) - (select count(Card_no)
	from BOOK_LENDING
	where B.Book_id = Book_id) as avail_copies
	from BOOK_COPIES B
	group by Book_id
);

select * from available;

/* queries 3 -- Delete a book in BOOK table. Update the contents of other tables to reflect this data 
manipulation operation. */

delete from BOOK where Book_id='1';
select * from BOOK;
    """

def p_order():
    return """
create database vp20ai027_ORDER;
use vp20ai027_ORDER;

create table SALESMAN
(
	Salesman_id varchar(5), 
	Name varchar(15),
	City varchar(15), 
	Commission int,
	primary key(Salesman_id)
);
create table CUSTOMER
(
	Customer_id varchar(5), 
	Cust_name varchar(15), 
	City varchar(15), 
	Grade int,
	Salesman_id varchar(5), 
	primary key(Customer_id),
	foreign key(Salesman_id) references SALESMAN(Salesman_id) on delete cascade
);
create table ORDERS
(
	Ord_no varchar(5), 
	Purchase_amt int,
	Ord_date date, 
	Customer_id varchar(5), 
	Salesman_id varchar(5), 
	primary key(Ord_no),
	foreign key(Customer_id) references CUSTOMER(Customer_id) on delete cascade, 
	foreign key(Salesman_id) references SALESMAN(Salesman_id) on delete cascade
);

desc SALESMAN;
desc CUSTOMER;
desc ORDERS;

insert into SALESMAN values(1,'Guru','Mangalore',5);
insert into SALESMAN values(2,'Ravi','Bangalore',3);
insert into SALESMAN values(3,'Girish','Hubli',3);
insert into SALESMAN values(4,'Sagar','Bangalore',3);
insert into SALESMAN values(5,'Raj','Mangalore',4);

insert into CUSTOMER values('C11','Srikanth','Bangalore',4,'2'),('C12','Sandeep','Mangalore',2,'3'),
('C13','Uday','Bangalore',3,'2'),('C14','Mahesh','Hubli',2,'2'),('C15','Shivaram','Bangalore',2,'3'),
('C16','Shyam','Mangalore',5,'1'),('C17','Sumith','Udupi',4,'5'),('C18','Shravan','Bangalore',3,'4');

insert into ORDERS values('O111',2500,'2017-07-11','C11','2'),('O112',1999,'2017-07-09','C12','3'),
('O113',999,'2017-07-12','C13','2'),('O114',9999,'2017-07-12','C14','2'),
('O115',7999,'2017-07-11','C15','3'),('O116',1099,'2017-07-09','C16','1');

select * from SALESMAN;
select * from CUSTOMER;
select * from ORDERS;

/* 1 Count the customers with grades above Bangalore's average.  */

select count(*) as Count
from CUSTOMER where Grade > (select avg(Grade) from CUSTOMER where City='Bangalore');

/* 2 Find the name and numbers of all salesman who had more than one customer. */

select s.Salesman_id, s.Name, count(Customer_id)
from SALESMAN s, CUSTOMER c
where s.Salesman_id = c.Salesman_id
group by s.Salesman_id, s.Name 
having count(Customer_id)>1;

/* 3 List all the salesman and indicate those who have and don't have customers in their cities (Use UNION operation.) */

select Name,'exists' as Same_city 
from SALESMAN s 
where city in (select city from CUSTOMER where s.Salesman_id= Salesman_id) 
union 
select Name,'not exists' as Same_city 
from SALESMAN s 
where city not in (select city from CUSTOMER where s.Salesman_id = Salesman_id);

/* 4 create a view that finds the salesman who has the customer with the highest order of a day */
 
create view Highest_order as 
select s.Salesman_id,s.Name,o.Purchase_amt,o.Ord_date
from SALESMAN s,ORDERS o
where s.Salesman_id = o.Salesman_id;
select Name,Ord_date
from Highest_order h
where Purchase_amt = (select max(Purchase_amt) from Highest_order where h.Ord_date = Ord_date);	

/* 5 demonstrate the delete operation by removing salesman with id 1000 All his order musst also be deleted */

delete from SALESMAN where Salesman_id=3;
    """

def p_movie():
    return """
create database vp20ai027_MOVIE;
use vp20ai027_MOVIE;

create table ACTOR
(
	act_id varchar(5),
	act_name varchar(15),
	act_gender varchar(6),
	primary key(act_id)
);

create table DIRECTOR
(
	dir_id varchar(5),
	dir_name varchar(15),
	dir_phone bigint,
	primary key(dir_id)
);
create table MOVIES
(
	mov_id varchar(5),
	mov_title varchar(20),
	mov_year int,
	mov_lang varchar(10),
	dir_id varchar(5),
	primary key(mov_id),
	foreign key(dir_id) references DIRECTOR(dir_id) on delete cascade
);
create table MOVIE_CAST
(
	act_id varchar(5),
	mov_id varchar(5),
	role varchar(10),
	primary key(act_id,mov_id),
	foreign key(act_id) references ACTOR(act_id) on delete cascade,
	foreign key(mov_id) references MOVIES(mov_id) on delete cascade
);
create table RATING
(
	rat_id varchar(5),
	mov_id varchar(5),
	rev_stars int,
	primary key(rat_id),
	foreign key(mov_id) references MOVIES(mov_id) on delete cascade
);

insert into ACTOR values('A101','Raj','M');
insert into ACTOR values('A102','Johny','M');
insert into ACTOR values('A103','Leo','M');
insert into ACTOR values('A104','Saru','F');
insert into ACTOR values('A105','Jasmine','F');
insert into ACTOR values('A106','Anthony parks','M');
insert into ACTOR values('A107','Harrison ford','M');


insert into DIRECTOR values('D01','Hitchcock',8723268423);
insert into DIRECTOR values('D02','Steven',8938732432);
insert into DIRECTOR values('D03','Rajamouli',9434784454);
insert into DIRECTOR values('D04','Nraj',9342400533);
insert into DIRECTOR values('D05','Pawan',8757563322);

insert into MOVIES values('M10','Psycho',1960,'english','D01');
insert into MOVIES values('M11','Tomorrow comes now',2017,'english','D04');
insert into MOVIES values('M12','Its a crime',1999,'english','D04');
insert into MOVIES values('M13','temples of doom',1984,'english','D02');
insert into MOVIES values('M14','hello hello',2016,'english','D04');
insert into MOVIES values('M15','E.T.',1982,'english','D02');

insert into MOVIE_CAST values('A101','M11','m_lead');
insert into MOVIE_CAST values('A104','M11','f_lead');
insert into MOVIE_CAST values('A101','M12','m_lead');
insert into MOVIE_CAST values('A106','M10','negative');
insert into MOVIE_CAST values('A107','M13','m_lead');
insert into MOVIE_CAST values('A104','M14','f_lead');
insert into MOVIE_CAST values('A107','M14','supporting');

insert into RATING values('R1','M11',4);
insert into RATING values('R2','M10',4);
insert into RATING values('R3','M11',3);
insert into RATING values('R4','M12',4);
insert into RATING values('R5','M13',4);
insert into RATING values('R6','M15',3);
insert into RATING values('R7','M13',3);

desc ACTOR;
desc DIRECTOR;
desc MOVIES;
desc MOVIE_CAST;
desc RATING;

select * from ACTOR;
select * from DIRECTOR;
select * from MOVIES;
select * from MOVIE_CAST;
select * from RATING;

/* 1 list the titles of all movies directed by 'Hitchcock' */

select mov_title from MOVIES m,DIRECTOR d where m.dir_id=d.dir_id and d.dir_name='Hitchcock';

/* 2 find the movie names where one or more actors acted in 2 or more movies  */

select distinct mov_title from MOVIES m,MOVIE_CAST mc
where m.mov_id = mc.mov_id and (select count(mov_id) from MOVIE_CAST where act_id=mc.act_id)>=2;

/* 3 List all actors who acted in a movie before 2000 and also in a movie after 2015 join operation*/

select act_name from ACTOR a join MOVIE_CAST mc on a.act_id = mc.act_id join MOVIES m
on mc.mov_id = m.mov_id
where m.mov_year<2000 and act_name in (select act_name
from ACTOR a join MOVIE_CAST mc on a.act_id = mc.act_id join MOVIES m
on mc.mov_id = m.mov_id
where m.mov_year>2015);

/* 4 Find the title of movies and number of stars for each movie that has at least one rating and findthe highest number of stars that movie received. Sort the result by movie title. */

select mov_title, max(rev_stars) from MOVIES m, RATING r
where m.mov_id = r.mov_id group by m.mov_title order by m.mov_title;

/* 5. Update rating of all movies directed by 'Steven Spielberg' to 5 */ 

select * from RATING;

update RATING set rev_stars=5
where mov_id in (select m.mov_id from MOVIES m, DIRECTOR d where m.dir_id = d.dir_id and d.dir_name='Steven');

select * from RATING;
    """

def p_college():
    return """
create database vp20ai027_COLLEGE;
use vp20ai027_COLLEGE;

create table STUDENT
(
	usn varchar(10),
	sname varchar(15),
	address varchar(15),
	phone bigint,
	gender varchar(6),
	primary key(usn)
);
create table SEMSEC
(
	ssid varchar(5),
	sem int,
	sec varchar(1),
	primary key(ssid)
);
create table CLASS
(
	usn varchar(10),
	ssid varchar(5),
	primary key(usn),
	foreign key(usn) references STUDENT(usn) on delete cascade,
	foreign  key(ssid) references SEMSEC(ssid) on delete cascade
);
create table COURSE
(
	sub_code varchar(7),
	title varchar(15),
	sem int,credits int,
	primary key(sub_code)
);
create table IAMARKS
(
	usn varchar(10),
	sub_code varchar(7),
	ssid varchar(5),
	test1 int,
	test2 int,
	test3 int,
	finalia int,
	primary key(usn,sub_code,ssid),
	foreign key(usn) references STUDENT(usn) on delete cascade,
	foreign key(sub_code) references COURSE(sub_code) on delete cascade,
	foreign key(ssid) references SEMSEC(ssid) on delete cascade
);


insert into STUDENT values('4vp20ai100','namitha','udupi',7860054110,'f');
insert into STUDENT values('4vp20ai101','mithun','viratpet',8762514991,'m');
insert into STUDENT values('4vp20ai102','kshama','puttur',9000876123,'f');
insert into STUDENT values('4vp20ai103','raghav','karwar',8700967408,'m');
insert into STUDENT values('4vp20ai104','sooraj','bangalore',7773334422,'m');
insert into STUDENT values('4vp20ai105','karthik','puttur',7789086125,'m');

insert into SEMSEC values('S01',1,'A');
insert into SEMSEC values('S04',4,'A');
insert into SEMSEC values('S05',4,'C');
insert into SEMSEC values('S06',8,'A');
insert into SEMSEC values('S07',8,'B');
insert into SEMSEC values('S08',8,'C');

insert into CLASS values('4vp20ai100','S04');
insert into CLASS values('4vp20ai101','S05');
insert into CLASS values('4vp20ai102','S01');
insert into CLASS values('4vp20ai103','S06');
insert into CLASS values('4vp20ai104','S07');
insert into CLASS values('4vp20ai105','S08');

insert into COURSE values('18cs14','Algorithms',1,4);
insert into COURSE values('18cs41','Graph theory',4,3);
insert into COURSE values('18cs43','Processors',4,4);
insert into COURSE values('18cs81','Oop with c++',8,4);
insert into COURSE values('18cs82','Networks',8,4);
insert into COURSE values('18cs83','DBMS',8,3);

/*
insert into IAMARKS values('4vp20ai100','18cs41','S05',19,18,20,NULL);
insert into IAMARKS values('4vp20ai100','18cs41','S05',19,18,20,NULL);
*/
insert into IAMARKS(usn,sub_code,ssid,test1,test2,test3) values('4vp20ai100','18cs41','S05',19,18,20);
insert into IAMARKS(usn,sub_code,ssid,test1,test2,test3) values('4vp20ai101','18cs43','S04',15,18,19);
insert into IAMARKS(usn,sub_code,ssid,test1,test2,test3) values('4vp20ai101','18cs41','S04',15,17,14);
insert into IAMARKS(usn,sub_code,ssid,test1,test2,test3) values('4vp20ai102','18cs14','S01',10,11,8);
insert into IAMARKS(usn,sub_code,ssid,test1,test2,test3) values('4vp20ai103','18cs14','S01',13,17,15);
insert into IAMARKS(usn,sub_code,ssid,test1,test2,test3) values('4vp20ai104','18cs81','S08',13,17,19);
insert into IAMARKS(usn,sub_code,ssid,test1,test2,test3) values('4vp20ai104','18cs82','S06',12,09,10);
insert into IAMARKS(usn,sub_code,ssid,test1,test2,test3) values('4vp20ai105','18cs81','S07',19,17,16);
insert into IAMARKS(usn,sub_code,ssid,test1,test2,test3) values('4vp20ai105','18cs83','S08',19,17,18);

desc STUDENT;
desc SEMSEC;
desc CLASS;
desc COURSE;
desc IAMARKS;

select * from STUDENT;
select * from SEMSEC;
select * from CLASS;
select * from COURSE;
select * from IAMARKS;

/* 1. List all the student details studying in fourth semester 'c' section. */

select s.usn,sname,address,gender 
from STUDENT s,SEMSEC sc,CLASS c 
where s.usn=c.usn and sc.ssid=c.ssid and sc.sem=4 and sc.sec='C';

/* 2. Compute the total number of male and female students in each semester and in each section. */

select sem, sec, gender, count(*) as count
from STUDENT s, SEMSEC sc, CLASS c
where s.usn = c.usn and sc.ssid = c.ssid
group by sem, sec, gender;

/* 3. Create a view of Test1 marks of student USN '1BI15CS101' in all subjects. */

create view TEST1_MARKS as(select usn,test1,sub_code from IAMARKS where usn='4vp20ai101');

select * from TEST1_MARKS;

/* 4. Calculate the FinalIA (average of best two test marks) and update the corresponding table for all students.*/

create table AVERAGE_FINDER
(
select usn,sub_code,greatest(test1,test2,test3) as highest, 
case
when test1<greatest(test1,test2,test3) and test1>least(test1,test2,test3) then test1
when test2<greatest(test1,test2,test3) and test2>least(test1,test2,test3) then test2
else test3
end as second_highest from IAMARKS
);

select * from AVERAGE_FINDER;

update IAMARKS i set finalia = (select (highest+second_highest)/2 from AVERAGE_FINDER
where i.usn=usn and i.sub_code=sub_code);

select * from IAMARKS;

/*
 5. Categorize students based on the following criterion:
If FinalIA = 17 to 20 then CAT = 'Outstanding'
If FinalIA = 12 to 16 then CAT = 'Average'
If FinalIA< 12 then CAT = 'Weak'
Give these details only for 8 th semester A, B, and C section students.
 */
 
select usn,sub_code, 
case
when finalia>=17 and finalia<=20 then 'Outstanding'
when finalia>=12 and finalia<=16 then 'Average'
when finalia<12 then 'Weak'
end as category
from IAMARKS
where usn in (select usn from SEMSEC sc,CLASS c where sc.ssid=c.ssid and sem=8 and sec in ('A','B','C'));
    """

def p_comp():
    return """

CREATE TABLE DEPARTMENT
(
    DNO VARCHAR(20) PRIMARY KEY,
    DNAME VARCHAR(20),
    MGR_SSN VARCHAR(20),
    MGR_START_DATE DATE
);

CREATE TABLE EMPLOYEE
(
    SSN VARCHAR(20) PRIMARY KEY,
    NAME VARCHAR(20),
    ADDRESS VARCHAR(20),
    SEX CHAR(1),
    SALARY INTEGER,
    SUPERSSN VARCHAR(20),
    DNO VARCHAR(20),
    FOREIGN KEY (SUPERSSN) REFERENCES EMPLOYEE (SSN),
    FOREIGN KEY (DNO) REFERENCES DEPARTMENT (DNO)
);

ALTER TABLE DEPARTMENT ADD FOREIGN KEY (MGR_SSN) REFERENCES EMPLOYEE(SSN);

CREATE TABLE DLOCATION
(
    DLOC VARCHAR(20),
    DNO VARCHAR(20),
    FOREIGN KEY (DNO) REFERENCES DEPARTMENT(DNO),
    PRIMARY KEY (DNO, DLOC)
);

CREATE TABLE PROJECT
(
    PNO INTEGER PRIMARY KEY,
    PNAME VARCHAR(20),
    PLOCATION VARCHAR(20),
    DNO VARCHAR(20),
    FOREIGN KEY (DNO) REFERENCES DEPARTMENT(DNO)
);

CREATE TABLE WORKS_ON
(
    HOURS INTEGER,
    SSN VARCHAR(20),
    PNO INTEGER,
    PRIMARY KEY (SSN, PNO),
    FOREIGN KEY (SSN) REFERENCES EMPLOYEE(SSN),
    FOREIGN KEY (PNO) REFERENCES PROJECT(PNO)
);

--Inserting records into EMPLOYEE table

INSERT INTO EMPLOYEE (SSN, NAME, ADDRESS, SEX, SALARY) VALUES
 ('ABC01','BEN SCOTT','BANGALORE','M', 450000);
INSERT INTO EMPLOYEE (SSN, NAME, ADDRESS, SEX, SALARY) VALUES
 ('ABC02','HARRY SMITH','BANGALORE','M', 500000);
INSERT INTO EMPLOYEE (SSN, NAME, ADDRESS, SEX, SALARY) VALUES
 ('ABC03','LEAN BAKER','BANGALORE','M', 700000);
INSERT INTO EMPLOYEE (SSN, NAME, ADDRESS, SEX, SALARY) VALUES
 ('ABC04','MARTIN SCOTT','MYSORE','M', 500000);
INSERT INTO EMPLOYEE (SSN, NAME, ADDRESS, SEX, SALARY) VALUES
 ('ABC05','RAVAN HEGDE','MANGALORE','M', 650000);
INSERT INTO EMPLOYEE (SSN, NAME, ADDRESS, SEX, SALARY) VALUES
 ('ABC06','GIRISH HOSUR','MYSORE','M', 450000);
INSERT INTO EMPLOYEE (SSN, NAME, ADDRESS, SEX, SALARY) VALUES
 ('ABC07','NEELA SHARMA','BANGALORE','F', 800000);
INSERT INTO EMPLOYEE (SSN, NAME, ADDRESS, SEX, SALARY) VALUES
 ('ABC08','ADYA KOLAR','MANGALORE','F', 350000);
INSERT INTO EMPLOYEE (SSN, NAME, ADDRESS, SEX, SALARY) VALUES
 ('ABC09','PRASANNA KUMAR','MANGALORE','M', 300000);
INSERT INTO EMPLOYEE (SSN, NAME, ADDRESS, SEX, SALARY) VALUES
 ('ABC10','VEENA KUMARI','MYSORE','M', 600000);
INSERT INTO EMPLOYEE (SSN, NAME, ADDRESS, SEX, SALARY) VALUES
 ('ABC11','DEEPAK RAJ','BANGALORE','M', 500000);

----------------------------------

--Inserting records into DEPARTMENT table

INSERT INTO DEPARTMENT VALUES ('1','ACCOUNTS','ABC09', '2016-01-03');
INSERT INTO DEPARTMENT VALUES ('2','IT','ABC11', '2017-02-04');
INSERT INTO DEPARTMENT VALUES ('3','HR','ABC01', '2016-04-05');
INSERT INTO DEPARTMENT VALUES ('4','HELPDESK', 'ABC10', '2017-06-03');
INSERT INTO DEPARTMENT VALUES ('5','SALES','ABC06', '2017-01-08');

--Updating EMPLOYEE records

UPDATE EMPLOYEE SET
SUPERSSN=NULL, DNO='3'
WHERE SSN='ABC01';

UPDATE EMPLOYEE SET
SUPERSSN='ABC03', DNO='5'
WHERE SSN='ABC02';

UPDATE EMPLOYEE SET
SUPERSSN='ABC04', DNO='5'
WHERE SSN='ABC03';

UPDATE EMPLOYEE SET
SUPERSSN='ABC06', DNO='5'
WHERE SSN='ABC04';

UPDATE EMPLOYEE SET
DNO='5', SUPERSSN='ABC06'
WHERE SSN='ABC05';

UPDATE EMPLOYEE SET
DNO='5', SUPERSSN='ABC07'
WHERE SSN='ABC06';

UPDATE EMPLOYEE SET
DNO='5', SUPERSSN=NULL
WHERE SSN='ABC07';

UPDATE EMPLOYEE SET
DNO='1', SUPERSSN='ABC09'
WHERE SSN='ABC08';

UPDATE EMPLOYEE SET
DNO='1', SUPERSSN=NULL
WHERE SSN='ABC09';

UPDATE EMPLOYEE SET
DNO='4', SUPERSSN=NULL
WHERE SSN='ABC10';

UPDATE EMPLOYEE SET
DNO='2', SUPERSSN=NULL
WHERE SSN='ABC11';

--Inserting records into DLOCATION table

INSERT INTO DLOCATION VALUES ('BENGALURU', '1');
INSERT INTO DLOCATION VALUES ('BENGALURU', '2');
INSERT INTO DLOCATION VALUES ('BENGALURU', '3');
INSERT INTO DLOCATION VALUES ('MYSORE', '4');
INSERT INTO DLOCATION VALUES ('MYSORE', '5');

--Inserting records into PROJECT table

INSERT INTO PROJECT VALUES (1000,'IOT','BENGALURU','5');
INSERT INTO PROJECT VALUES (1001,'CLOUD','BENGALURU','5');
INSERT INTO PROJECT VALUES (1002,'BIGDATA','BENGALURU','5');
INSERT INTO PROJECT VALUES (1003,'SENSORS','BENGALURU','3');
INSERT INTO PROJECT VALUES (1004,'BANK MANAGEMENT','BENGALURU','1');
INSERT INTO PROJECT VALUES (1005,'SALARY MANAGEMENT','BANGALORE','1');
INSERT INTO PROJECT VALUES (1006,'OPENSTACK','BENGALURU','4');
INSERT INTO PROJECT VALUES (1007,'SMART CITY','BENGALURU','2');

--Inserting records into WORKS_ON table

INSERT INTO WORKS_ON VALUES (4, 'ABC02', 1000);
INSERT INTO WORKS_ON VALUES (6, 'ABC02', 1001);
INSERT INTO WORKS_ON VALUES (8, 'ABC02', 1002);
INSERT INTO WORKS_ON VALUES (10,'ABC03', 1000);
INSERT INTO WORKS_ON VALUES (3, 'ABC05', 1000);
INSERT INTO WORKS_ON VALUES (4, 'ABC06', 1001);
INSERT INTO WORKS_ON VALUES (5, 'ABC07', 1002);
INSERT INTO WORKS_ON VALUES (6, 'ABC04', 1002);
INSERT INTO WORKS_ON VALUES (7, 'ABC01', 1003);
INSERT INTO WORKS_ON VALUES (5, 'ABC08', 1004);
INSERT INTO WORKS_ON VALUES (6, 'ABC09', 1005);
INSERT INTO WORKS_ON VALUES (4, 'ABC10', 1006);
INSERT INTO WORKS_ON VALUES (10,'ABC11', 1007);

DESC EMPLOYEE;
DESC DEPARTMENT;
DESC DLOCATION;
DESC PROJECT;
DESC WORKS_ON;

SELECT * FROM EMPLOYEE;
SELECT * FROM DEPARTMENT;
SELECT * FROM DLOCATION;
SELECT * FROM PROJECT;
SELECT * FROM WORKS_ON;


--Make a list of all project numbers for projects that involve an employee whose last name is ‘Scott’, either as a worker or as a manager of the department that controls the project.

SELECT DISTINCT P.PNO
FROM PROJECT P, DEPARTMENT D, EMPLOYEE E
WHERE E.DNO=D.DNO
AND D.MGR_SSN=E.SSN
AND E.NAME LIKE '%SCOTT'
UNION
SELECT DISTINCT P1.PNO
FROM PROJECT P1, WORKS_ON W, EMPLOYEE E1
WHERE P1.PNO=W.PNO
AND E1.SSN=W.SSN
AND E1.NAME LIKE '%SCOTT';

--Show the resulting salaries if every employee working on the ‘IoT’ project is given a 10 percent raise.

SELECT E.NAME, 1.1*E.SALARY AS INCR_SAL
FROM EMPLOYEE E, WORKS_ON W, PROJECT P
WHERE E.SSN=W.SSN
AND W.PNO=P.PNO
AND P.PNAME='IOT';

--Find the sum of the salaries of all employees of the ‘Accounts’ department, as well as the maximum salary, the minimum salary, and the average salary in this department

SELECT SUM(E.SALARY), MAX(E.SALARY), MIN(E.SALARY), AVG(E.SALARY)
FROM EMPLOYEE E, DEPARTMENT D
WHERE E.DNO=D.DNO
AND D.DNAME='ACCOUNTS';

--Retrieve the name of each employee who works on all the projects controlled by department number 5 (use NOT EXISTS operator).

SELECT E.NAME
FROM EMPLOYEE E
WHERE NOT EXISTS(SELECT PNO FROM PROJECT WHERE DNO='5' AND PNO NOT IN (SELECT
PNO FROM WORKS_ON
WHERE E.SSN=SSN));

--For each department that has more than five employees, retrieve the department number and the number of its employees who are making more than Rs. 6,00,000.

SELECT D.DNO, COUNT(*)
FROM DEPARTMENT D, EMPLOYEE E
WHERE D.DNO=E.DNO
AND E.SALARY > 600000
AND D.DNO IN (SELECT E1.DNO
FROM EMPLOYEE E1
GROUP BY E1.DNO
HAVING COUNT(*)>5)
GROUP BY D.DNO;
    """

def p_longtictactoe():
    return """
# Tic-Tac-Toe Program using random number in Python
import numpy as np
import random
from time import sleep

# Creates an empty board


def create_board():
	return(np.array([[0, 0, 0],
					[0, 0, 0],
					[0, 0, 0]]))

# Check for empty places on board


def possibilities(board):
	l = []

	for i in range(len(board)):
		for j in range(len(board)):

			if board[i][j] == 0:
				l.append((i, j))
	return(l)

# Select a random place for the player


def random_place(board, player):
	selection = possibilities(board)
	current_loc = random.choice(selection)
	board[current_loc] = player
	return(board)

# Checks whether the player has three
# of their marks in a horizontal row


def row_win(board, player):
	for x in range(len(board)):
		win = True

		for y in range(len(board)):
			if board[x, y] != player:
				win = False
				continue

		if win == True:
			return(win)
	return(win)

# Checks whether the player has three
# of their marks in a vertical row


def col_win(board, player):
	for x in range(len(board)):
		win = True

		for y in range(len(board)):
			if board[y][x] != player:
				win = False
				continue

		if win == True:
			return(win)
	return(win)

# Checks whether the player has three
# of their marks in a diagonal row


def diag_win(board, player):
	win = True
	y = 0
	for x in range(len(board)):
		if board[x, x] != player:
			win = False
	if win:
		return win
	win = True
	if win:
		for x in range(len(board)):
			y = len(board) - 1 - x
			if board[x, y] != player:
				win = False
	return win

# Evaluates whether there is
# a winner or a tie


def evaluate(board):
	winner = 0

	for player in [1, 2]:
		if (row_win(board, player) or
				col_win(board, player) or
				diag_win(board, player)):

			winner = player

	if np.all(board != 0) and winner == 0:
		winner = -1
	return winner

# Main function to start the game


def play_game():
	board, winner, counter = create_board(), 0, 1
	print(board)
	sleep(2)

	while winner == 0:
		for player in [1, 2]:
			board = random_place(board, player)
			print("Board after " + str(counter) + " move")
			print(board)
			sleep(2)
			counter += 1
			winner = evaluate(board)
			if winner != 0:
				break
	return(winner)


# Driver Code
print("Winner is: " + str(play_game()))

    """