class Graph:
    def __init__(self,graph,hlist,snode):
        self.graph = graph
        self.H = hlist
        self.start = snode
        self.parent = {}
        self.status = {}
        self.sGraph = {}

    def applyAoStar(self):
        self.aoStar(self.start,False)
    def getNeighbours(self,v):
        return self.graph.get(v,"")
    def getStatus(self,v):
        return self.status.get(v,0)
    def setStatus(self,v,val):
        self.status[v] = val
    def getHValue(self,n):
        return self.H.get(n,0)
    def setHValue(self,n,value):
        self.H[n] = value

    def printSolution(self):
        print(self.start)
        print(self.sGraph)
        

    def compMinCost(self,v):
        minCost = 0
        minChild = []
        neighbours = self.getNeighbours(v)
        for neighbour in neighbours:
            cost = 0
            childList = []
            for n,w in neighbour:
                cost += w + self.getHValue(n)
                childList.append(n)
            
            if minCost == 0 or cost < minCost:
                minCost = cost
                minChild = childList
        return minCost,minChild
    
    def aoStar(self,v,backt):
        if self.getStatus(v) >= 0:
            minCost,minChild = self.compMinCost(v)
            
            self.setHValue(v,minCost)
            self.setStatus(v,len(minChild))

            solved = True
            for child in minChild:
                self.parent[child] = v
                if self.getStatus(child) != -1:
                    solved = False
                
            if solved == True: 
                self.setStatus(v,-1)
                self.sGraph[v] = minChild

            if v != self.start:
                self.aoStar(self.parent[v],True)
            
            if backt == False:
                for child in minChild:
                    self.setStatus(child,0)
                    self.aoStar(child,False)
 
h1 = {'A': 1, 'B': 6, 'C': 2, 'D': 12, 'E': 2, 'F': 1, 'G': 5, 'H': 7, 'I': 7, 'J':1, 'T': 3}
graph1 = {
    'A': [[('B', 1), ('C', 1)], [('D', 1)]],
    'B': [[('G', 1)], [('H', 1)]],
    'C': [[('J', 1)]],
    'D': [[('E', 1), ('F', 1)]],
    'G': [[('I', 1)]]
}
G1= Graph(graph1, h1, 'A')
G1.applyAoStar()
G1.printSolution()

