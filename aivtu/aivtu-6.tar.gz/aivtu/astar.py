def astaralgo(startnode,stopnode):
    openset=set(startnode)
    closedset=set()
    g={}
    parent={}
    g[startnode]=0
    parent[startnode]=startnode

    while len(openset)>0:
        n=None
        for v in openset:
            if n==None or g[v]+heuristic(v)<g[n]+heuristic(n):
                n=v
                
        if n!=stopnode and Graph_nodes.get(n,None)!=None:
            for (m,w) in Graph_nodes[n]:
                if m not in openset and m not in closedset:
                    openset.add(m)
                    parent[m]=n
                    g[m]=g[n]+w
                   
        if n==None:
            print("path doesn't exist")
            return None
        if n==stopnode:
            path=[]
            while n!=parent[n]:
                path.insert(0,n)
                n=parent[n]
            path.insert(0,startnode)
            print(path)
            return path
        openset.remove(n)
        closedset.add(n)
    print("path does not exist")
    return None
        
def heuristic(n):
    H_dist = {
    'A': 10,
    'B': 8,
    'C': 5,
    'D': 7,
    'E': 3,
    'F': 6,
    'G': 5,
    'H': 3,
    'I': 1,
    'J': 0,
    }
    return H_dist[n]
#Describe your graph here 
Graph_nodes = {
 'A': [('B', 6), ('F', 3)],
 'B': [('C', 3), ('D', 2)],
 'C': [('D', 1), ('E', 5)],
 'D': [('C', 1), ('E', 8)],
 'E': [('I', 5), ('J', 5)],
 'F': [('G', 1),('H', 7)] ,
 'G': [('I', 3)],
 'H': [('I', 2)],
 'I': [('E', 5), ('J', 3)],
}
astaralgo('A', 'J')
