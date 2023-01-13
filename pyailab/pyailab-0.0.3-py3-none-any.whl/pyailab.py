"""PART A -->  import pyailab.aia.pg ()
PART B -->  import pyailab.aib.pg () 
MAM --> import pyailab.mam.programname()
"""
class aia:
    def pg1a():
        """  1 (a) write a program to print the multiplication table for the given number """
        print(""" 
## 1 (a) write a program to print the multiplication table for the given number

# using for loop
n=int(input("Enter the number of which the user wants to print the multiplication table: "))
print("multiplication table of ",n," is")
for i in range(1,11):
    print(n,"X",i,"=",n*i)

# using while loop
a=int(input("Enter the number of which the user wants to print the multiplication table: "))
b=int(input("Enter the number till which user needs to be printed: "))
print("multiplication table of number is")
i=1
while i<=b:
    print(a,"X",i,"=",a*i)
    i=i+1
        """)

    def pg1b():
        """  write a python program to check whether the given number is prime or not """
        print("""
## 1 (b) write a python program to check whether the given number is prime or not

num=int(input("Enter the number that is to checked prime or not: "))
if num > 1:
    for i in range(2,num):
        if (num % i) == 0:
            print(num, "is not a prime number")
            break
    else:                                        # see the indentation of else not below if below for
        print(num, "is a prime number")
else:
    print(num, "is not a prime number")
        """)

    def pg1c():
        """  write a python program to find factorial of given number """
        print("""
## 1 (c) write a python program to find factorial of given number

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
        """)

    def pg2a():
        """ 2 (a) Write a python program to implement list operations
        i) nested list
        ii) length
        iii) concatination
        iv) membership
        v) iteration
        vi) indexing
        vii) slicing
        viii) replication
        """
        print("""
# i nested list
print("========== nested list ==============")
nested_list = [1,[2,3],'hi',['hello','world']]
print("The nested list is ",nested_list)
print("nested_list[0] : ",nested_list[0])
print("nested_list[-1][-1]: ",nested_list[-1][-1])
print("nested_list[1][1]: ",nested_list[1][1])
print("======================================")
print()

# ii lenth of the list
print("========== length of list ==============")
L1 = ['hello','how','are','you']
print("The list is ",L1)
print("The length of list ",len(L1))
print("======================================")
print()

# iii concatination
print("========== concatination list ==============")
L1 = ['hello','how','are','you']
L2 = ['i am','fine',1,2]
print("The list 1  is ",L1)
print("The list 2  is ",L2)
L3 = L1+L2
print("The concatination of list 1 and 2 is ",L3)
print("======================================")
print()

# iv membership 
print("========== membership list ==============")
L1 = ['hello','how','are','you']
print("The list is ",L1)
ans1 = 'apple' in L1
print("checking is 'apple' in the list ",ans1)
ans2 = 'hello' in L1
print("checking is 'hello' in the list ",ans2)
print("======================================")
print()

# v iteration
print("========== iteration list ==============")
L1 = ['hello','how','are','you']
print("The list is ",L1)
print("printing element of list")
for i in L1:
    print(i)
print("======================================")
print()

# vi indexing
print("========== indexing list ==============")
L1 = ['hello','how','are','you']
print("The list is ",L1)
print("printing individual element of list")
print(L1[0])
print(L1[1])
print(L1[2])
print(L1[3])
print("======================================")
print()

# vii slicing
print("========== slicing list ==============")
L1 = ['hello','how','are','you']
print("The list is ",L1)
print("The L1[0:3]: ",L1[0:3])
print("The L1[2:]: ",L1[2:])
print("The L1[2:3]: ",L1[2:3])
print("======================================")
print()

# viii replication
print("========== replication list ==============")
L2 = ['i am','fine',1,2]
print("The list is ",L2)
L4 = L2 * 3
print("The list after replicating 3 times is ",L4)
print("======================================")
print()
        """)
    
    def pg2b():
        """
    2 b) Write a python program to implement List methods
      i) append
      ii) add - insert
      iii) extend
      iv) delete
        """
        print("""
# i append to list at last
print("========= append to list ===========")
L1 = ['hello', 'how', 'are']
print("The list before appending is: ",L1)
L1.append('you')
print("The list after appending 'you' is: ",L1)
print("=============================================")
print()

# ii insert to list
L1 = ['hello', 'how', 'are','you']
print("========= insert to list ===========")
print("The list before insertion is: ",L1)
L1.insert(1,'shreesha')
print("The list after adding 'shreesha' to 2nd position is: \n",L1)
print("=============================================")
print()

# iii extend the list 1
print("========= extend list ===========")
L1 = ['hello', 'how', 'are']
L2 = ['i', 'fine', 1, 2]
print("The is 1st list is: ",L1)
print("The is 2nd list is: ",L2)
L1.extend(L2)
print("after the extention of list 1 it becomes : \n",L1)
print("=============================================")
print()

# iv delete - remove the particular element
print("========= delete using remove ===========")
L1 = ['hello', 'how', 'are','you']
print("The is list before removing is: ",L1)
L1.remove('hello')
print("The is list after removing 'hello' is: ",L1)
print("=============================================")
print()

# v delete last , 1st element using pop
print("========= delete using pop ===========")
L1 = ['hello', 'how','are','you']
print("The is list before poping is: ",L1)
L1.pop()
print("The is list after poping from last is: ",L1)
print()
print("The is list before poping is: ",L1)
L1.pop(0)
print("The is list after poping from 1st is: ",L1)
print("=============================================")
print()

# delete using keyword del
print("========= delete using del ===========")
L1 = ['hello', 'how', 'are','you']
print("The is list before deleting is: ",L1)
del L1[1]
print("The is list after deleting 2nd element is: ",L1)
print("=============================================")
print()
        """)

    def pg3():
        """ write a python program to implement simple Chatbot with minimum 10 conservation """
        print("""
# 3) write a python program to implement simple Chatbot with minimum 10 conservation

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
        """)

    def pg4():
        ''' 4 ) write a python program to illustrate different set operation '''
        print("""
# 4 ) write a python program to illustrate different set operation

a = {2,4,6,8}
b = {1,2,3,4,5}
print("Set A = ",a,"Set B = ",b)
print("union of A & B (A U B)= ",a|b)
print("Intersection of A & B (A ^ B) = ",a&b)
print("Set difference  of B and A (A-B) = ",a-b)
print("Set symmetric difference(disjunctive union) of A and B (A-B)U(B-A) = ",(a-b)|(b-a))
print("Set symmetric difference(disjunctive union) of A and B (A ^ B) = ",a^b)
        """)
    
    def pg5a():
        ''' 5 a) write a python program to implement a function that counts number of times string(s1) occurs in string (s2)'''
        print("""
#  5 a) write a python program to implement a function that counts number of times string(s1) occurs in string (s2)

s1 = input("Enter the substring: ").lower()
s2 = input("Enter the string: ").lower()
count = s2.count(s1)
print("The substring",s1,"string occured in string",s2,count,"times")
        """)
    
    def pg5b():
        """ 5 b) write a program to illustrate dictionary operations([],in,traversal) and methods :
keys() ,values() , items() """
        print("""
# 5 b) write a program to illustrate dictionary operations([],in,traversal) and methods : keys() ,values() , items()
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
    print(my_dict['address'])      # error
except:
    print("error:  KeyError")
    
print("-".center(55,'-'))
print()
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

print()
print("-".center(55,'-'))
print("in operators".center(55,'-'))
print()

spam = {'name':'shreesha','age':7,'color':'white'}
print('spam =',spam)
res1 = 'name' in spam.keys()
print("'name' in spam.keys(): ",end='')
print(res1)

res2 = 'nature' in spam.keys()
print("'nature' in spam.keys(): ",res2)

print("-".center(55,'-'))
print()
print("not in operators".center(55,'-'))
print()

res3 = 'name' not in spam.keys()
print("'name' not in spam.keys(): ",res3)

res4 = 'shreesha' not in spam.values()
print("'shreesha' not in spam.values(): ",res4)

res5 = 8 not in spam.values()
print("8 not in spam.values(): ",res5)
print()
        """)

class aib:
    def pg1():
        """ DFS - depth first search """
        print("""
# 3 water jugs capacity -> (x,y,z) where x>y>z   # initial state (12,0,0)   # final state (6,6,0)

capacity = (12,8,5)        # Maximum capacities of 3 jugs -> x,y,z
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

    def pg1v2():
        """ DFS - depth first search """
        print("""
capacity = (12,8,5) 

x = capacity[0]
y = capacity[1]
z = capacity[2]

memory = {}

ans = []

def get_all_states(state):
	a = state[0]
	b = state[1]
	c = state[2]

	if(a==6 and b==6):
		ans.append(state)
		return True
	if((a,b,c) in memory):
		return False

	memory[(a,b,c)] = 1

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
		if(a+c<=z):
			if( get_all_states((0,b,a+c)) ):
				ans.append(state)
				return True
		else:
			if( get_all_states((a-(z-c), b, z)) ):
				ans.append(state)
				return True

	if(b>0):
		if(a+b<=x):
			if( get_all_states((a+b, 0, c)) ):
				ans.append(state)
				return True
		else:
			if( get_all_states((x, b-(x-a), c)) ):
				ans.append(state)
				return True
		if(b+c<=z):
			if( get_all_states((a, 0, b+c)) ):
				ans.append(state)
				return True
		else:
			if( get_all_states((a, b-(z-c), z)) ):
				ans.append(state)
				return True

	if(c>0):
		if(a+c<=x):
			if( get_all_states((a+c, b, 0)) ):
				ans.append(state)
				return True
		else:
			if( get_all_states((x, b, c-(x-a))) ):
				ans.append(state)
				return True
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

    def pg2():
        """ BFS MAM SHORT """
        print("""
from collections import defaultdict
jug1 = int(input("max capacity of jug1: "))
jug2 = int(input("max capacity of jug2: "))
goal = int(input("Enter capacity to be measured: "))
visited = defaultdict(lambda:False)

def waterjug(a1,a2):
  if(a1==goal and a2==0) or (a2==goal and a1==0):
    print(a1,a2)
    return True
  if visited[(a1,a2)] == False:
    print(a1,a2)
    visited[(a1,a2)] = True
    return (waterjug(0,a2) or waterjug(a1,0) or waterjug(jug1,a2) or waterjug(a1,jug2) or 
            waterjug(a1+min(a2,jug1-a1) , a2-min(a2,jug1-a1)) or waterjug(a1-min(a1,jug2-a2),a2+min(a1,jug2-a2)))
  else:
    return False

print('Steps: ')
waterjug(0,0)

        """)


    def pg2v2():
        """ BFS - breadth first search"""
        print("""
from collections import deque

def BFS(a, b, target):
	m = {}
	isSolvable = False
	path = []
	q = deque()
	q.append((0, 0))

	while (len(q) > 0):
		u = q.popleft()
		if ((u[0], u[1]) in m):
			continue
		if ((u[0] > a or u[1] > b or
			u[0] < 0 or u[1] < 0)):
			continue
		path.append([u[0], u[1]])
		m[(u[0], u[1])] = 1
		if (u[0] == target or u[1] == target):
			isSolvable = True

			if (u[0] == target):
				if (u[1] != 0):
					path.append([u[0], 0])
			else:
				if (u[0] != 0):
					path.append([0, u[1]])
			sz = len(path)
			for i in range(sz):
				print("(", path[i][0], ",",
					path[i][1], ")")
			break
		q.append([u[0], b])
		q.append([a, u[1]])

		for ap in range(max(a, b) + 1):
			c = u[0] + ap
			d = u[1] - ap
			if (c == a or (d == 0 and d >= 0)):
				q.append([c, d])
			c = u[0] - ap
			d = u[1] + ap
			if ((c == 0 and c >= 0) or d == b):
				q.append([c, d])
		q.append([a, 0])
		q.append([0, b])
	if (not isSolvable):
		print("No solution")

if __name__ == '__main__':

	Jug1, Jug2, target = 4, 3, 2
	print("Path from initial state "
		"to solution state ::")

	BFS(Jug1, Jug2, target)
        """)

    def pg3():
        """ ao* alogorithm ai generated"""
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

    def pg4():
        """  n queen problem """
        print("""
print ("Enter the number of queens")
N = int(input())
# NxN matrix with all elements set to 0
board = [[0]*N for _ in range(N)]     # OR board = [[0]*N]*N
def attack(i, j):
    #checking vertically and horizontally
    for k in range(0,N):
        if board[i][k]==1 or board[k][j]==1:
            return True
    #checking diagonally
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
        """)

    def pg4v2():
        """  n queen problem """
        print("""

print ("Enter the number of queens")
N = int(input())
board = [[0]*N for _ in range(N)]     # OR board = [[0]*N]*N
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
        """)

    def pg5():
        """ tsp travel saleman person"""
        print("""
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
        """)

    """ forward chaining and backward chaining has 2 version
        pg6av1() , pg6av2() , pg6bv1() , pg6bv2() """

    """ Forward chaining is a problem-solving strategy that
 involves starting with the available information and working 
 forwards to find the solution to a problem. """ 

    def pg6av1():
        """ Forward chain version 1 """
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

    def pg6():
        """ Forward chain version 2"""
        print("""
initial_state = ["dirty", "smelly"]
rules = [
    {"if": ["dirty"], "then": ["clean"]},
    {"if": ["clean", "smelly"], "then": ["fresh"]},
]
goal = ["fresh"]
current_state = initial_state
while not all(x in current_state for x in goal):
    for rule in rules:
        if all(x in current_state for x in rule["if"]):
            current_state += rule["then"]
print("The final state is:", current_state)
        """)

    """Backward chaining is a problem-solving strategy that involves starting with the goal and working backwards to find the necessary steps to achieve it. 
  This code simply prints out each step in reverse order,
 starting with the goal and working backwards through the necessary steps to
 achieve it. You can adapt this basic structure to fit your specific problem-solving 
 needs by modifying the goal and steps variables as needed. """

    def pg6bv1():
        """ backward chain version 1"""
        print("""
goal = "find a solution to the problem"

# define the necessary steps to achieve the goal
steps = ["identify the problem", "generate potential solutions", "evaluate potential solutions", "implement a solution"]

# start with the goal and work backwards
print(goal)
for step in reversed(steps):
    print(step)
        """)

    def pg6bv2():
        """ backward chain version 2"""
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

    def pg7v1():
        """ FOPL 
 resolution(kb, alpha) -->  kb: knowledge base (list of lists, where each inner list represents 
 a clause and each element within the inner list represents a literal)
  alpha: query (list of lists, where each inner list represents a clause and each element 
  within the inner list represents a literal)
  Returns: True if the query can be inferred from the knowledge base, False otherwise.

resolve(ci, cj): -->    ci: first clause (list of literals)
  cj: second clause (list of literals)
  Returns: list of all possible resolvents that can be derived from ci and cj
        """
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

    def pg7v2():
        """ The resolve() function is used to perform resolution on two clauses, and returns a set of resolvents (i.e., the set of clauses that can be obtained by resolving the two input clauses).
The prove() function takes a knowledge base knowledge_base and a goal goal as input, and uses the resolve() function to try and prove the goal using the resolution principle and the given knowledge base. If the goal can be proved, the function returns True, otherwise it returns False."""
        print("""
from functools import reduce

def resolve(clause1, clause2):
    resolvents = set()
    for literal1 in clause1:
        for literal2 in clause2:
            if literal1[1:] == literal2[1:] or literal1[0] != literal2[0]:
                continue
            resolvent = clause1.union(clause2) - {literal1, literal2}
            if not resolvent:
                return None
            resolvents.add(frozenset(resolvent))
    return resolvents

def prove(knowledge_base, goal):
    clauses = list(knowledge_base) + [goal]
    new = set()
    while True:
        n = len(clauses)
        pairs = [(i, j) for i in range(n) for j in range(i+1, n)]
        for (i, j) in pairs:
            resolvents = resolve(clauses[i], clauses[j])
            if resolvents is None:
                return True
            new.update(resolvents)
        if not new.issubset(clauses):
            clauses += list(new)
            new = set()
        else:
            return False

# Example usage
knowledge_base = {frozenset({'A', 'B'}), frozenset({'-A', 'C'}), frozenset({'B', '-C'})}
goal = frozenset({'D'})

if prove(knowledge_base, goal):
    print("The goal can be proved using the given knowledge base.")
else:
    print("The goal cannot be proved using the given knowledge base.")
        """)
        
    def pg7():
        """  Mam ge kotiddu """
        print("""
from functools import reduce
from funcaitools import resolve
def prove(knowledge_base, goal):
    clauses = list(knowledge_base) + [goal]
    new = set()
    while True:
        n = len(clauses)
        pairs = [(i, j) for i in range(n) for j in range(i+1, n)]
        for (i, j) in pairs:
            resolvents = resolve(clauses[i], clauses[j])
            if resolvents is None:
                return True
            new.update(resolvents)
        if not new.issubset(clauses):
            clauses += list(new)
            new = set()
        else:
            return False
knowledge_base = {frozenset({'A', 'B'}), frozenset({'-A', 'C'}), frozenset({'-B', '-C'})}
goal = frozenset({'D'})
if prove(knowledge_base, goal):
    print("The goal can be proved using the given knowledge base.")
else:
    print("The goal cannot be proved using the given knowledge base.")
        """)


    def pg8():
        ''' tic tac toe '''
        print("""
import os
import time

board = [' ']*10
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

#This Function Checks position is empty or not
def CheckPosition(x):
    if(board[x] == ' '):
        return True
    else:
        return False

#This Function Checks player has won or not
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

print("Player 1 [X] --- Player 2 [O]\n")
print()
print()
print("Please Wait...")
time.sleep(10)
while(Game == Running):
    os.system('clear')
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

os.system('clear')
DrawBoard()
if(Game==Draw):
    print("Game Draw")
elif(Game==Win):
    player-=1
    if(player%2!=0):
        print("Player 1 Won")
    else:
        print("Player 2 Won")
        """)
        
class mam:
    """ 
    multiplication
    prime
    factorial
    listoperations
    listmethods
    chatbot
    setoperations
    counts
    dictionaryoperations
    dictoperations
    dfs
    bfs
    aostar
    nqueen
    tsp
    forward
    fopl
    game
    tictactoe
    """

    def multiplication():
        print("""
number = int(input ("Enter the number of which the user wants to print the multiplication table: "))             
print ("The Multiplication Table of: ", number)    
for count in range(1, 11):      
   print (number, 'x', count, '=', number * count)
   
a=int(input("enter table number"))
b=int(input("enter the number to which table is to printed"))
i=1
while i<=b:
    print(a,"x",i,"=",a*i)
    i=i+1
        """)
    def prime():
        print("""
number = int(input("Enter any number: "))
if number > 1:
    for i in range(2, number):
        if (number % i) == 0:
            print(number, "is not a prime number")
            break
    else:
        print(number, "is a prime number")
else:
    print(number, "is not a prime number")
        """)
    def factorial():
        print("""
num = int(input("Enter a number: "))    
factorial = 1    
if num < 0:    
   print(" Factorial does not exist for negative numbers") 
elif num == 0:    
   print("The factorial of 0 is 1")    
else:    
   for i in range(1,num + 1):    
       factorial = factorial*i    
   print("The factorial of",num,"is",factorial)        
        """)
    def listoperations():
        print("""
print("========== nested list ==============")
nested_list = [1,[2,3],'hi',['hello','world']]
print("The nested list is ",nested_list)
print("nested_list[0] : ",nested_list[0])
print("nested_list[1][1]: ",nested_list[1][1])

print("========== length of list ==============")
L1 = ['hello','how','are','you']
print("The list is ",L1)
print("The length of list ",len(L1))

print("========== concatination list ==============")
L1 = ['hello','how','are','you']
L2 = ['i am','fine',1,2]
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
print("The L1[2:]: ",L1[2:])

print("========== replication list ==============")
L2 = ['i am','fine',1,2]
print("The list is ",L2)
L4 = L2 * 3
print("The list after replicating 3 times is ",L4)
        """)
        
    def listmethods():
        print("""
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
print()
print("The is list before poping is: ",L1)
L1.pop(0)
print("The is list after poping from 1st is: ",L1)

print("========= delete using del ===========")
L1 = ['hello', 'how', 'are','you']
print("The is list before deleting is: ",L1)
del L1[1]
print("The is list after deleting 2nd element is: ",L1)
        """)
        
    def chatbot():
        print("""
print("Simple Question and Answering Program")
print("=====================================")
print(" You may ask any one of these questions")
print("Hi")
print("How are you?")
print("Are you studying?")
print("What is your name?")
print("what did you do yesterday?")
print("Quit")
while True:
    question = input("Enter one question from above list:")
    question = question.lower()
    if question in ['hi']:
        print("Hello")
    elif question in ['how are you?','how do you do?']:
        print("I am fine")
    elif question in ['are you studying?','are you doing any job?']:
        print("yes. I'am studying in VCET Puttur")
    elif question in ['what is your name?']:
        print("My name is Anu")
        name=input("Enter your name?")
        print("Nice name and Nice meeting you",name)
    elif question in ['what did you do yesterday?']:
        print("I saw Bahubali 5 times")
    elif question in ['quit']:
        break
    else:
        print("I don't understand what you said")

        """)
    def setoperations():
        print("""
# define three sets
E = {0, 2, 4, 6, 8};
N = {1, 2, 3, 4, 5};

# set union
print("Union of E and N is",E | N)

# set intersection
print("Intersection of E and N is",E & N)

# set difference
print("Difference of E and N is",E - N)

# set symmetric difference
print("Symmetric difference of E and N is",E ^ N)

        """)
    def counts():
        print("""
str1 = "Welcome to VCET Puttur. VCET awesome, isn't it?"
sub_string = "VCET"
temp_str = str1.lower()
count = temp_str.count(sub_string.lower())
print("The VCET count is:", count)
        """)
    def dictionaryoperations():
        print("""
my_dict = {'name':'shreesha','age':20,'gender':'male'}
print("\naccessing values with []")
print(my_dict['name'])

print("\naccessing values with get() method")
print(my_dict.get('age'))
print("\naccessing non existing values with get() method")
print(my_dict.get('address','do not exist'))

print("\naccessing non existing values with [] error handeled")
try:
    print(my_dict['address'])      # error
except:
    print("error:  KeyError")
    
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

print("not in operators".center(55,'-'))
res3 = 'name' not in spam.keys()
print("'name' not in spam.keys(): ",res3)
res4 = 'shreesha' not in spam.values()
print("'shreesha' not in spam.values(): ",res4)
res5 = 8 not in spam.values()
print("8 not in spam.values(): ",res5)
        """)
    def dictoperations():
        print("""
my_dict = {'name':'shreesha','age':20,'gender':'male'}
print("\naccessing values with []")
print(my_dict['name'])

print("\naccessing values with get() method")
print(my_dict.get('age'))
print("\naccessing non existing values with get() method")
print(my_dict.get('address','do not exist'))

print("\naccessing non existing values with [] error handeled")
try:
    print(my_dict['address'])      # error
except:
    print("error:  KeyError")
    
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

print("not in operators".center(55,'-'))
res3 = 'name' not in spam.keys()
print("'name' not in spam.keys(): ",res3)
res4 = 'shreesha' not in spam.values()
print("'shreesha' not in spam.values(): ",res4)
res5 = 8 not in spam.values()
print("8 not in spam.values(): ",res5)
       
        """)
    def dfs():
        print("""
capacity = (12,8,5) 
x = capacity[0]
y = capacity[1]
z = capacity[2]

memory = {}

ans = []

def get_all_states(state):
	a = state[0]
	b = state[1]
	c = state[2]

	if(a==6 and b==6):
		ans.append(state)
		return True
	if((a,b,c) in memory):
		return False

	memory[(a,b,c)] = 1

	if(a>0):
		if(a+b<=y):
			if( get_all_states((0,a+b,c)) ):
				ans.append(state)
				return True
		else:
			if( get_all_states((a-(y-b), y, c)) ):
				ans.append(state)
				return True
		if(a+c<=z):
			if( get_all_states((0,b,a+c)) ):
				ans.append(state)
				return True
		else:
			if( get_all_states((a-(z-c), b, z)) ):
				ans.append(state)
				return True

	if(b>0):
		if(a+b<=x):
			if( get_all_states((a+b, 0, c)) ):
				ans.append(state)
				return True
		else:
			if( get_all_states((x, b-(x-a), c)) ):
				ans.append(state)
				return True
		if(b+c<=z):
			if( get_all_states((a, 0, b+c)) ):
				ans.append(state)
				return True
		else:
			if( get_all_states((a, b-(z-c), z)) ):
				ans.append(state)
				return True
	if(c>0):
		if(a+c<=x):
			if( get_all_states((a+c, b, 0)) ):
				ans.append(state)
				return True
		else:
			if( get_all_states((x, b, c-(x-a))) ):
				ans.append(state)
				return True
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
    def bfs():
        print("""
from collections import defaultdict
jug1 = int(input("max capacity of jug1: "))
jug2 = int(input("max capacity of jug2: "))
goal = int(input("Enter capacity to be measured: "))
visited = defaultdict(lambda:False)

def waterjug(a1,a2):
  if(a1==goal and a2==0) or (a2==goal and a1==0):
    print(a1,a2)
    return True
  if visited[(a1,a2)] == False:
    print(a1,a2)
    visited[(a1,a2)] = True
    return (waterjug(0,a2) or waterjug(a1,0) or waterjug(jug1,a2) or waterjug(a1,jug2) or 
            waterjug(a1+min(a2,jug1-a1) , a2-min(a2,jug1-a1)) or waterjug(a1-min(a1,jug2-a2),a2+min(a1,jug2-a2)))
  else:
    return False

print('Steps: ')
waterjug(0,0)        
        """)
    def aostar():
        print("""
def recAOStar(n):
    global finalPath
    print("Expanding Node:",n)
    and_nodes = []
    or_nodes =[]
    if(n in allNodes):
        if 'AND' in allNodes[n]:
            and_nodes = allNodes[n]['AND']
        if 'OR' in allNodes[n]:
            or_nodes = allNodes[n]['OR']
    if len(and_nodes)==0 and len(or_nodes)==0:
        return
    
    solvable = False
    marked ={}
    
    while not solvable:
        if len(marked)==len(and_nodes)+len(or_nodes):
            min_cost_least,min_cost_group_least = least_cost_group(and_nodes,or_nodes,{})
            solvable = True
            change_heuristic(n,min_cost_least)
            optimal_child_group[n] = min_cost_group_least
            continue
        min_cost,min_cost_group = least_cost_group(and_nodes,or_nodes,marked)
        is_expanded = False
        if len(min_cost_group)>1:
            if(min_cost_group[0] in allNodes):
                is_expanded = True
                recAOStar(min_cost_group[0])
            if(min_cost_group[1] in allNodes):
                is_expanded = True
                recAOStar(min_cost_group[1])
        else:
            if(min_cost_group in allNodes):
                is_expanded = True
                recAOStar(min_cost_group)
        if is_expanded:
            min_cost_verify, min_cost_group_verify = least_cost_group(and_nodes, or_nodes, {})
            if min_cost_group == min_cost_group_verify:
                solvable = True
                change_heuristic(n, min_cost_verify)
                optimal_child_group[n] = min_cost_group
        else:
            solvable = True
            change_heuristic(n, min_cost)
            optimal_child_group[n] = min_cost_group
        marked[min_cost_group]=1
    return heuristic(n)

def least_cost_group(and_nodes, or_nodes, marked):
    node_wise_cost = {}
    for node_pair in and_nodes:
        if not node_pair[0] + node_pair[1] in marked:
            cost = 0
            cost = cost + heuristic(node_pair[0]) + heuristic(node_pair[1]) + 2
            node_wise_cost[node_pair[0] + node_pair[1]] = cost
    for node in or_nodes:
        if not node in marked:
            cost = 0
            cost = cost + heuristic(node) + 1
            node_wise_cost[node] = cost
    min_cost = 999999
    min_cost_group = None
    for costKey in node_wise_cost:
        if node_wise_cost[costKey] < min_cost:
            min_cost = node_wise_cost[costKey]
            min_cost_group = costKey
    return [min_cost, min_cost_group]

def heuristic(n):
    return H_dist[n]

def change_heuristic(n, cost):
    H_dist[n] = cost
    return

def print_path(node):
    print(optimal_child_group[node], end="")
    node = optimal_child_group[node]
    if len(node) > 1:
        if node[0] in optimal_child_group:
            print("->", end="")
            print_path(node[0])
        if node[1] in optimal_child_group:
            print("->", end="")
            print_path(node[1])
    else:
        if node in optimal_child_group:
            print("->", end="")
            print_path(node)
H_dist = {
 'A': -1,
 'B': 4,
 'C': 2,
 'D': 3,
 'E': 6,
 'F': 8,
 'G': 2,
 'H': 0,
 'I': 0,
 'J': 0
}
allNodes = {
 'A': {'AND': [('C', 'D')], 'OR': ['B']},
 'B': {'OR': ['E', 'F']},
 'C': {'OR': ['G'], 'AND': [('H', 'I')]},
 'D': {'OR': ['J']}
}
optimal_child_group = {}
optimal_cost = recAOStar('A')
print('Nodes which gives optimal cost are')
print_path('A')
print('\nOptimal Cost is :: ', optimal_cost)

        """)
    def nqueen():
        print("""
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
        """)
    def tsp():
        print("""
from sys import maxsize
from itertools import permutations
V = 4
def travellingSalesmanProblem(graph, s):
    vertex = []
    for i in range(V):
        if i != s:
            vertex.append(i)
    min_path = maxsize
    next_permutation=permutations(vertex)
    for i in next_permutation:
        current_pathweight = 0
        k = s
        for j in i:
            current_pathweight += graph[k][j]
            k = j
        current_pathweight += graph[k][s]
        min_path = min(min_path, current_pathweight)
         
    return min_path

if __name__ == "__main__":
    graph = [[0, 10, 15, 20], [10, 0, 35, 25],
            [15, 35, 0, 30], [20, 25, 30, 0]]
    s = 0
    print(travellingSalesmanProblem(graph, s))        
        """)
    def forward():
        print("""
initial_state = ["dirty", "smelly"]
rules = [
    {"if": ["dirty"], "then": ["clean"]},
    {"if": ["clean", "smelly"], "then": ["fresh"]},
]
goal = ["fresh"]
current_state = initial_state
while not all(x in current_state for x in goal):
    for rule in rules:
        if all(x in current_state for x in rule["if"]):
            current_state += rule["then"]
print("The final state is:", current_state)        
        """)
    def fopl():
        print("""
from functools import reduce
from funcaitools import resolve
def prove(knowledge_base, goal):
    clauses = list(knowledge_base) + [goal]
    new = set()
    while True:
        n = len(clauses)
        pairs = [(i, j) for i in range(n) for j in range(i+1, n)]
        for (i, j) in pairs:
            resolvents = resolve(clauses[i], clauses[j])
            if resolvents is None:
                return True
            new.update(resolvents)
        if not new.issubset(clauses):
            clauses += list(new)
            new = set()
        else:
            return False
knowledge_base = {frozenset({'A', 'B'}), frozenset({'-A', 'C'}), frozenset({'-B', '-C'})}
goal = frozenset({'D'})

if prove(knowledge_base, goal):
    print("The goal can be proved using the given knowledge base.")
else:
    print("The goal cannot be proved using the given knowledge base.")        
        """)
    def game():
        print("""
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
time.sleep(3)    
while(Game == Running):    
    os.system('clear')    
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
    
os.system('clear')    
DrawBoard()    
if(Game==Draw):    
    print("Game Draw")    
elif(Game==Win):    
    player-=1    
    if(player%2!=0):    
        print("Player 1 Won")    
    else:    
        print("Player 2 Won")    
        
        """)
    def tictactoe():
        print("""
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
time.sleep(3)    
while(Game == Running):    
    os.system('clear')    
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
    
os.system('clear')    
DrawBoard()    
if(Game==Draw):    
    print("Game Draw")    
elif(Game==Win):    
    player-=1    
    if(player%2!=0):    
        print("Player 1 Won")    
    else:    
        print("Player 2 Won")    
        
        """)