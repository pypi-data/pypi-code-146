import os

def getPath(filename):
    fname = filename
    this_file = os.path.abspath(__file__)
    this_dir = os.path.dirname(this_file)
    Wanted_file = os.path.join(this_dir, fname)
    with open(Wanted_file,"r") as f:
        print(f.read())

def p1():
    getPath('astar.py')
def astar():
    getPath('astar.py')

def p2():
    getPath('aostar.py')
def aostar():
    getPatj('aostar.py')

def p3():
    getPath('ce.py')
def ce():
    getPath('ce.py')

def p4():
    getPath('id3.py')
def id3():
    getPath('id3.py')

def p5():
    getPath('ann.py')
def ann():
    getPath('ann.py')
        
def p6():
    getPath('nb.py')
def nb():
    getPath('nb.py')

def p7():
    getPath('em.py')
def em():
    getPath('em.py') 

def p8():
    getPath('knn.py')
def knn():
    getPath('knn.py') 

def p9():
    getPath('reg.py')
def reg():
    getPath('reg.py') 

