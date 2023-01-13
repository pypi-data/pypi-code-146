def index():
    print(""" 
1aQ1) Design a simple linear neural network model.
        Calculate the output of neural net where input X = 0.2, w = 0.3 and bias b 0.45.
1aQ2) Calculate the output of neural net for given data.
        Calculate the output of neural net where input X = [x1, x2, x3] = [0.3, 0.5, 0.6]
        & Weight W = [w1, w2, w3] = [0.2, 0.1, -0.3].
1b) Calculate the output of neural net using both binary and bipolar sigmoidal function.
    
2a) Generate AND/NOT function using McCulloch- Pitts neural net.
2b) Generate XOR function using McCulloch-Pitts neural net.

3a) WAP to implement Hebb’s rule. L and U pattern
3b) WAP to implement of delta rule.

4a) WAP for Back Propagation Algorithm. 
4b) WAP for error Backpropagation algorithm.

5a) WAP for Hopfield network.
5b) WAP for radial basis function.

6a) Kohonen self-organizing map.
6b) Hopfield network.

7a) Implement membership and identity operators | in, not in.
7b) Implement membership and identity operators is, is not.

8a) Find ratios using fuzzy logic.
8b) Solve tipping problem using fuzzy logic.

          """)
          



def prog(num):
    if(num=="1aQ1"):
        print(""" 

x = float(input("Enter the input: "))
w = float(input("Enter the weight: "))
b = float(input("Enter the bias: "))

Yin = x*w + b
print("Yin: ",Yin)

if Yin < 0:
  out = 0
elif Yin > 1:
  out = 1
else:
  out = Yin

print("Output: ",out)



              """) 
        
    elif(num=="1aQ2"):
        print("""

import numpy as np

n = int(input("Enter the number of elements: "))
x = np.zeros(n)
w = np.zeros(n)

print("Enter the inputs")
for i in range(0,n):
  x[i] = float(input())

print("Enter the weights")
for i in range(0,n):
  w[i] = float(input())

yin_temp = np.zeros(n)
yin_temp = (x*w)

yin = yin_temp.sum()
yin = round(yin,2) 
print("Net Input: ",yin)

if yin < 0:
  out = 0
elif yin > 1:
  out = 1
else:
  out = yin

print("Output: ",out)

                """)
        
    elif(num=="1b"):
        print(""".

import math
import numpy as np

n = int(input("Enter the number of elements: "))
x = np.zeros((n,))
w = np.zeros((n,))

print("Enter the inputs")
for i in range(0,n):
  x[i] = float(input())

print("Enter the weights")
for i in range(0,n):
  w[i] = float(input())

b = float(input("Enter Bias: "))


yin_temp = np.zeros(n)
yin_temp = (x*w)
yin = yin_temp.sum() + b
yin = round(yin,2) 
print("Net Input: ",yin)

binary_sigmoidal = (1/(1+(math.e**(-yin))))
print("Binary Sigmoidal: ",(round(binary_sigmoidal,3)))

bipolar_sigmoidal = (2/(1+(math.e**(-yin)))) - 1
print("Bipolar Sigmoidal: ",(round(bipolar_sigmoidal,3)))

""")
    
    elif(num=="2a"):
        print("""
import numpy as np
print("ANDNOT using MP Neuron")
x1 = np.array([0,0,1,1])
x2 = np.array([0,1,0,1])

print("Considering all weights as Excitatory")
w1 = w2 =1
yin = x1*w1 + x2*w2
print("x1 x2 yin")
for i in range(0,4):
    print(x1[i]," ",x2[i], " ", yin[i])

print("Considering one weight as Excitatory and other as Inhibitory")
w1 = 1
w2 = -1
yin = x1*w1 + x2*w2
print("x1 x2 yin")
for i in range(0,4):
    print(x1[i]," ",x2[i], " ", yin[i])

theta = 1
print("Considering Threshold as 1")
print("Applying Threshold")
y = np.zeros(4).astype(int)
for i in range(0,4):
    if yin[i] >= 1:
        y[i] = 1
    else:
        y[i] = 0


print("x1 x2   y")
for i in range(0,4):
    print(x1[i]," ",x2[i], " ", y[i])


""")

    elif(num=="2b"):
        print("""
#Implementing XOR Uing MP

import numpy as np
x1 = np.array([0,0,1,1])
x2 = np.array([0,1,0,1])

print("Calculating zin1 = x1*w11 + x2*w21")
print("Considering one weight as excitatory and other as inhibitory")
w11 = 1
w21 = -1
zin1 = x1*w11 + x2*w21
print("x1 x2 zin1")
for i in range(0,4):
    print(x1[i]," ",x2[i], " ", zin1[i])

print("Calculating zin2 = x1*w12 + x2*w22")
print("Considering one weight as excitatory and other as inhibitory")
w12 = -1
w22 = 1
zin2 = x1*w12 + x2*w22
print("x1 x2 zin2")
for i in range(0,4):
    print(x1[i]," ",x2[i], " ", zin2[i])

print("Applying Threshold for zin1 and zin2")
z1 = np.zeros(4).astype(int)
z2 = np.zeros(4).astype(int)

for i in range(0,4):
    if zin1[i] >= 1:
        z1[i] = 1
    else:
        z1[i] = 0
        
    if zin2[i] >= 1:
        z2[i] = 1
    else:
        z2[i] = 0

print("x1 x2   z1  z2")
for i in range(0,4):
    print(x1[i]," ",x2[i], " ", z1[i]," ", z2[i])

print("Calculating yin = z1*v1 + z2*v2")
print("Considering both weight as excitatory")
v1 = v2 = 1
yin = z1*v1 + z2*v2

print("x1 x2   yin")
for i in range(0,4):
    print(x1[i]," ",x2[i], " ", yin[i])

print("Applying Threshold for yin")
y = np.zeros(4).astype(int)

for i in range(0,4):
    if yin[i] >= 1:
        y[i] = 1
    else:
        y[i] = 0

print("x1 x2   y")
for i in range(0,4):
    print(x1[i]," ",x2[i], " ", y[i])

""")
        
    elif(num=="3a"):
        print("""

import numpy as np
x1=np.array([1,-1,-1,1,-1,-1,1,1,1])
x2=np.array([1,-1,1,1,-1,1,1,1,1])
b=0
y=np.array([1,-1])

wtold=np.zeros(9)
wtnew=np.zeros(9)
#print("--",wtold)
wtnew=wtnew.astype(int)
wtold=wtold.astype(int)
bais=0

print("First input with target=1")
wtnew = wtold+x1*y[0]
wtold=wtnew
b=b+y[0]
print("new wt=", wtnew)
print("Bias value",b)

print("Second input with target=-1")
wtnew = wtold+x2*y[1]
b=b+y[1]

print("New wt=",wtnew)
print("Bias value",b)

""")
        
    elif(num=="3b"):
        print("""
import numpy as np
import time
np.set_printoptions(precision=2)
x=np.zeros((3,))
weights=np.zeros((3,))
desired=np.zeros((3,))
actual=np.zeros((3,))
for i in range(0,3):
    x[i]=float(input("Intial inputs:"))

for i in range(0,3):
    weights[i]=float(input("Intial weights:"))

for i in range(0,3):
    desired[i]=float(input("Desired output:"))

a=float(input("Enter learning rate:"))

actual=x*weights
print("actual",actual)
print("desired",desired)

while True:
  if np.array_equal(desired,actual):
    break     #no change
  else:
    for i in range(0,3):
        weights[i]=weights[i]+a*(desired[i]-actual[i])

  actual=x*weights
  print("weights",weights)
  print("actual",actual)
  print("desired",desired)

print("*"*30)
print("Final output")
print("Corrected weights",weights)
print("actual",actual)
print("desired",desired)


#Initial input = 1,1,1
#initial weight = 1,1,1
#desired output = 2,3,4
#learning rate = 1

""")
        
    elif(num=="4a"):
        print("""
import numpy as np
X=np.array(([2,9],[1,5],[3,6]),dtype=float)
Y=np.array(([92],[86],[89]),dtype=float)

#scale units
X=X/np.amax(X,axis=0)
Y=Y/100;

class NN(object):
  def __init__(self):
    self.inputsize=2
    self.outputsize=1
    self.hiddensize=3
    self.W1=np.random.randn(self.inputsize,self.hiddensize)
    self.W2=np.random.randn(self.hiddensize,self.outputsize)
    
  def forward(self,X):
    self.z=np.dot(X,self.W1)
    self.z2=self.sigmoidal(self.z)
    self.z3=np.dot(self.z2,self.W2)
    op=self.sigmoidal(self.z3)
    return op;

  def sigmoidal(self,s):
    return 1/(1+np.exp(-s))

obj=NN()
op=obj.forward(X)
print("actual output"+str(op))
print("expected output"+str(Y))

""")
        
    elif(num=="4b"):
        print("""
import numpy as np
X=np.array(([2,9],[1,5],[3,6]),dtype=float)
Y=np.array(([92],[86],[89]),dtype=float)

X=X/np.amax(X,axis=0)
Y=Y/100;

class NN(object):
  def __init__(self):
    self.inputsize=2
    self.outputsize=1
    self.hiddensize=3
    self.W1=np.random.randn(self.inputsize,self.hiddensize)
    self.W2=np.random.randn(self.hiddensize,self.outputsize)

  def forward(self,X):
    self.z=np.dot(X,self.W1)
    self.z2=self.sigmoidal(self.z)
    self.z3=np.dot(self.z2,self.W2)
    op=self.sigmoidal(self.z3)
    return op;

  def sigmoidal(self,s):
    return 1/(1+np.exp(-s))

  def sigmoidalprime(self,s):
    return s* (1-s)

  def backward(self,X,Y,o):
    self.o_error=Y-o
    self.o_delta=self.o_error * self.sigmoidalprime(o)
    self.z2_error=self.o_delta.dot(self.W2.T)
    self.z2_delta=self.z2_error * self.sigmoidalprime(self.z2)
    self.W1 = self.W1 + X.T.dot(self.z2_delta)
    self.W2= self.W2+ self.z2.T.dot(self.o_delta)

  def train(self,X,Y):
    o=self.forward(X)
    self.backward(X,Y,o)

obj=NN()
for i in range(2000):
  obj.train(X,Y)

print("input"+str(X))
print("Actual output"+str(Y))
print("Predicted output"+str(obj.forward(X)))
print("loss"+str(np.mean(np.square(Y-obj.forward(X)))))

""")
        
    elif(num=="5a"):
        print(""" 

import numpy as np

def compute_next_state(state , weight):
  next_state = np.where(weight @ state >= 0, +1, -1)
  #next_state = np.matmul(weight,state)
  #print(next_state)
  return next_state


#@' is shorthand for np.matmul()
#numpy.where() returns the indices of the elements in an input array
#where the given condt is satisfied 


def compute_final_state(initial_state, weight, max_iter=1000):
  previous_state = initial_state
  next_state = compute_next_state(previous_state, weight)
  is_stable = np.all(previous_state == next_state)
  
  n_iter = 0 
  while(not is_stable) and (n_iter <= max_iter):
    previous_state = next_state
    next_state = compute_next_state(previous_state, weight)
    is_stable = np.all(previous_state == next_state)
    n_iter += 1
  
  return previous_state, is_stable, n_iter


initial_state = np.array([1,-1,-1,-1])
weight = np.array([
    [0,-1,-1,1],
    [-1,0,1,-1],
    [-1,1,0,-1],
    [1,-1,-1,0]
    ])


final_state , is_stable, n_iter = compute_final_state(initial_state, weight)

print("Final State: ",final_state)

        
        """)
        
    elif(num=="5b"):
        print(""" 

D <- matrix(c(-3,1,4), ncol=1)
N <- length(D)
rbf.gauss <- function(gamma=1.0) {
    function(x){
        exp(-gamma * norm(as.matrix(x),"F")^2)
    }
}
xlim <- c(-5,7)
print(N)
print(xlim)
plot(NULL,xlim=xlim,ylim=c(0,1.25), type = "n")
points(D,rep(0,length(D)), col= 1:N,pch=19)
x.coord = seq(-7,7,length=250)
gamma <- 1.5
for (i in 1:N){
    points(x.coord, lapply(x.coord - D[i,],rbf.gauss(gamma)),type="l",col=i)
}

        """)
        
    elif(num=="6a"):
        print(""" 
#pip instal MiniSom
#pip instal matplotlib
from minisom import MiniSom 
import numpy as np
import matplotlib.pyplot as plt

colors = [[0., 0., 0.],
          [0., 0., 1.0],
          [0.125, 0.529, 1.0],
          [0.33, 0.4, 0.67],
          [0.6, 0.5, 1.0],
          [0., 1., 0.],
          [1.0, 0., 0.],
          [0., 1., 1.],
          [1., 0., 1.],
          [1., 1., 1.],
          [.33, .33, .33],
          [0.5, 0.5, 0.5],
          [0.66, 0.66, 0.66]]

color_names = ['black', 'blue', 'darkblue', 'skyblue', 'greyblue',
               'lilac', 'green', 'red', 'cyan', 'violet', 'yellow',
               'white', 'darkgrey', 'mediumgrey', 'lightgrey']

som = MiniSom(30, 30, 3, sigma=3.,
              learning_rate = 2.5,
              neighborhood_function='gaussian')

plt.imshow(abs(som.get_weights()), interpolation = 'none')
#plt.show()
som.train(colors, 100, random_order=True, verbose=True)
plt.imshow(abs(som.get_weights()), interpolation = 'none')
#plt.show()

som = MiniSom(30, 30, 3, sigma=8.,
              learning_rate = .5,
              neighborhood_function='bubble')

som.train_random(colors, 100, verbose=True)
plt.imshow(abs(som.get_weights()), interpolation = 'none')
#plt.show()
 
       
        """)
        
    elif(num=="6b"):
        print(""" # works only in Google Colab

# pip install neurodynex 

from neurodynex.hopfield_network import network, pattern_tools, plot_tools
import matplotlib.pyplot as plt

pattern_size = 5
# create an instance of the class HopfieldNetwork
hopfield_net = network.HopfieldNetwork(nr_neurons= pattern_size**2)
# instantiate a pattern factory
factory = pattern_tools.PatternFactory(pattern_size, pattern_size)

# create a checkerboard pattern and add it to the pattern list
checkerboard = factory.create_checkerboard()
pattern_list = [checkerboard]

# add random patterns to the list
pattern_list.extend(factory.create_random_pattern_list(nr_patterns=3, on_probability=0.5))
plot_tools.plot_pattern_list(pattern_list)

# how similar are the random patterns and the checkerboard? Check the overlaps
overlap_matrix = pattern_tools.compute_overlap_matrix(pattern_list)
plot_tools.plot_overlap_matrix(overlap_matrix)

# let the hopfield network "learn" the patterns. Note: they are not stored
# explicitly but only network weights are updated !
hopfield_net.store_patterns(pattern_list)

# create a noisy version of a pattern and use that to initialize the network
noisy_init_state = pattern_tools.flip_n(checkerboard, nr_of_flips=4)
hopfield_net.set_state_from_pattern(noisy_init_state)

# from this initial state, let the network dynamics evolve.
states = hopfield_net.run_with_monitoring(nr_steps=4)

# each network state is a vector. reshape it to the same shape used to create the patterns.
states_as_patterns = factory.reshape_patterns(states)

# plot the states of the network
plot_tools.plot_state_sequence_and_overlap(states_as_patterns, pattern_list, 
reference_idx=0, suptitle="Network dynamics")



        
        """)
        
    elif(num=="7a"):
        print(""" 
            
#Code for 'In Operator':
#In operator
        
list1 = []
print("Enter 3 number for list 1")
for i in range(3):
  v = int(input())
  list1.append(v)

list2 = []
print("Enter 3 number for list 2")
for i in range(3):
  v = int(input())
  list2.append(v)

for i in list1:
  if i in list2:
    print("The list overlaps")
    break
else:
  print("List does not overlap")



#Code for 'Not in Operator':
#Not in operator

list3 = []
c = int(input("Enter the size of the list"))
for i in range(c):
  ele = int(input("Enter the elements: "))
  list3.append(ele)
  
a = int(input("Enter the element for search "))
if a not in list3:
  print("The list does not contains",a)
else:
  print("The list contains",a)

   
        """)
        
    elif(num=="7b"):
        print(""" 
        
#Is Operator

details = []
name = input("Enter your name: ")
details.append(name)

age = float(input("Enter your age: "))
details.append(age)

roll_no = int(input("Enter roll no: "))
details.append(roll_no)

for i in details:
  print()
  print(i)
  print("Int",type(i) is int)
  print("Float",type(i) is float)
  print("String",type(i) is str)




#Is not

details =[]

name=input("Enter your name : ")
details.append(name)

age=float(input("Enter your exact age : "))
details.append(age)

roll_no=int(input("Enter your roll no : "))
details.append(roll_no)

print() 
for i in details:
  print()
  print(i)
  print("Not Int = ",type(i) is not int)
  print("Not Float = ",type(i) is not float)
  print("Not String = ",type(i) is not str)
  

        
        """)
        
    elif(num=="8a"):
        print(""" 

#pip install fuzzywuzzy        

from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 

s1 = "I love fuzzysforfuzzys"
s2 = "I am loving fuzzysforfuzzys"
print ("FuzzyWuzzy Ratio:", fuzz.ratio(s1, s2)) 
print ("FuzzyWuzzy PartialRatio: ", fuzz.partial_ratio(s1, s2)) 
print ("FuzzyWuzzy TokenSortRatio: ", fuzz.token_sort_ratio(s1, s2)) 
print ("FuzzyWuzzy TokenSetRatio: ", fuzz.token_set_ratio(s1, s2)) 
print ("FuzzyWuzzy WRatio: ", fuzz.WRatio(s1, s2))

# for process library, 
query = 'fuzzys for fuzzys'
choices = ['fuzzy for fuzzy', 'fuzzy fuzzy', 'g. for fuzzys'] 
print ("List of ratios: ")
print (process.extract(query, choices), '')
print ("Best among the above list: ",process.extractOne(query, choices))

        
        """)
        
    elif(num=="8b"):
        print(""" 
        
#pip install fuzzywuzzy
#pip install -U scikit-fuzzy
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

quality.automf(3)
service.automf(3)

tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])

quality['average'].view()
service.view()
tip.view()

rule1 = ctrl.Rule(quality['poor'] | service['poor'], tip['low'])
rule2 = ctrl.Rule(service['average'], tip['medium'])
rule3 = ctrl.Rule(service['good'] | quality['good'], tip['high'])

rule1.view()

tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

tipping.input['quality'] = 6.5
tipping.input['service'] = 9.8

tipping.compute()
print (tipping.output['tip'])
tip.view(sim=tipping)

        
        """)
    
    else:
        print("invalid input")








    
    


















