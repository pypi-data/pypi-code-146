import os
import pytest
from hash import dag
from .commons import read_graph

nodes = []
base_path = os.path.dirname(__file__)
# Make sure to empty the nodes list before running any test
@pytest.fixture(autouse=True)
def run_around_tests():
    global nodes
    nodes = []
    # A test function will be run at this point
    yield

# A DFS callback
def dfs_callback(node : dag.Node, edges = [], visited_nodes = {}):
    nodes.append(node)

# Test a simple dfs call
def test_graph_dfs_simple():
    n1 = dag.Node('1', {})
    n2 = dag.Node('2', {})
    n3 = dag.Node('3', {})
    e2 = dag.Edge(n2, n3)
    e = dag.Edge(n1, n2)
    d = dag.Graph()
    d.addEdge(e)
    d.addEdge(e2)
    d.dfs_walk(n1, dfs_callback)
    assert len(nodes) == 3
    assert nodes[0] == n1
    assert nodes[1] == n2
    assert nodes[2] == n3

# Test adding two identical edges
def test_add_edge_double():
    n1 = dag.Node('1', {})
    n2 = dag.Node('2', {})
    n3 = dag.Node('3', {})
    e2 = dag.Edge(n2, n3)
    e = dag.Edge(n1, n2)
    e3 = dag.Edge(n2, n1)
    d = dag.Graph()
    d.addEdge(e)
    d.addEdge(e2)
    d.addEdge(e3)
    e4 = dag.Edge(n1, n2)
    d.addEdge(e4)
    assert len(d.getEdges()) == 3
    d.dfs_walk(n2, dfs_callback)
    assert len(nodes) == 3
    assert nodes[0] == n2
    assert nodes[1] == n3
    assert nodes[2] == n1

# Test a simple aother dfs call
def test_graph_dfs_another_simple():
    n1 = dag.Node('1', {})
    n2 = dag.Node('2', {})
    n3 = dag.Node('3', {})
    e2 = dag.Edge(n2, n3)
    e = dag.Edge(n1, n2)
    e3 = dag.Edge(n2, n1)
    d = dag.Graph()
    d.addEdge(e)
    d.addEdge(e2)
    d.addEdge(e3)
    d.dfs_walk(n2, dfs_callback)
    assert len(nodes) == 3
    assert nodes[0] == n2
    assert nodes[1] == n3
    assert nodes[2] == n1

# Test a dfs call for a 2 ndoe one way graph
def test_graph_read_dfs_2_node1():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/2_node1.graph"))
    d.dfs_walk(g_nodes[0], dfs_callback)
    assert len(nodes) == 2
    assert g_nodes[0] == nodes[0]
    assert g_nodes[1] == nodes[1]

# Test a dfs call for a 2 ndoe one way graph - start from second node
def test_graph_read_dfs_2_node11():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/2_node1.graph"))
    d.dfs_walk(g_nodes[1], dfs_callback)
    assert len(nodes) == 1
    assert g_nodes[1] == nodes[0]

# Test a dfs call for a 2 ndoe bi-directional graph
def test_graph_read_dfs_2_node2():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/2_node2.graph"))
    d.dfs_walk(g_nodes[0], dfs_callback)
    assert len(nodes) == 2
    assert g_nodes[0] == nodes[0]
    assert g_nodes[1] == nodes[1]

# Test a dfs call for a 3 one way graph
def test_graph_read_dfs_3_node1():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/3_node1.graph"))
    d.dfs_walk(g_nodes[0], dfs_callback)
    assert len(nodes) == 3
    assert g_nodes[0] == nodes[0]
    assert g_nodes[1] == nodes[1]
    assert g_nodes[2] == nodes[2]

# Test a dfs call for a 3 one way graph - start from second node
def test_graph_read_dfs_3_node1():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/3_node1.graph"))
    d.dfs_walk(g_nodes[1], dfs_callback)
    assert len(nodes) == 2
    assert g_nodes[1] == nodes[0]
    assert g_nodes[2] == nodes[1]

# Test a dfs call for a 3 bi-directional graph
def test_graph_read_dfs_3_node2():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/3_node2.graph"))
    d.dfs_walk(g_nodes[2], dfs_callback)
    assert len(nodes) == 3
    assert g_nodes[2] == nodes[0]
    assert g_nodes[1] == nodes[1]
    assert g_nodes[0] == nodes[2]

# Test a dfs call for a 3 one way graph
def test_graph_read_dfs_3_node3():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/3_node3.graph"))
    d.dfs_walk(g_nodes[0], dfs_callback)
    assert len(nodes) == 3
    assert g_nodes[0] == nodes[0]
    assert g_nodes[1] == nodes[1]
    assert g_nodes[2] == nodes[2]

# Test a dfs call for a 4 one way graph
def test_graph_read_dfs_4_node1():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/4_node1.graph"))
    d.dfs_walk(g_nodes[0], dfs_callback)
    assert len(nodes) == 4
    assert g_nodes[0] == nodes[0]
    assert g_nodes[1] == nodes[1]
    assert g_nodes[3] == nodes[2]
    assert g_nodes[2] == nodes[3]

    n = d.bfs_walk_number(g_nodes[0])
    assert len(n) == 3
    assert len(n[0]) == 1
    assert len(n[1]) == 2
    assert len(n[2]) == 1
    assert n[0][0] == nodes[0]
    assert n[1][0] == nodes[1]
    assert n[1][1] == nodes[3]
    assert n[2][0] == nodes[2]

# Test a dfs call for a 4 one way graph
def test_graph_read_dfs_4_node2():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/4_node2.graph"))
    d.dfs_walk(g_nodes[0], dfs_callback)
    assert len(nodes) == 4
    assert g_nodes[0] == nodes[0]
    assert g_nodes[1] == nodes[1]
    assert g_nodes[3] == nodes[3]
    assert g_nodes[2] == nodes[2]

    n = d.bfs_walk_number(g_nodes[0])
    assert len(n) == 3
    assert len(n[0]) == 1
    assert len(n[1]) == 1
    assert len(n[2]) == 2
    assert n[0][0] == nodes[0]
    assert n[1][0] == nodes[1]
    assert n[2][0] == nodes[2]
    assert n[2][1] == nodes[3]
    assert d.check_loop(g_nodes[0]) is False

# Test a dfs call for a 5 one way graph
def test_graph_read_dfs_5_node1():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/5_node1.graph"))
    d.dfs_walk(g_nodes[0], dfs_callback)
    assert len(nodes) == 5
    assert g_nodes[0] == nodes[0]
    assert g_nodes[1] == nodes[1]
    assert g_nodes[3] == nodes[2]
    assert g_nodes[4] == nodes[3]
    assert g_nodes[2] == nodes[4]

# Test a dfs call for a 5 bi-directonal graph
def test_graph_read_dfs_5_node2():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/5_node2.graph"))
    d.dfs_walk(g_nodes[0], dfs_callback)
    assert len(nodes) == 5
    assert nodes[0] == dag.Node('1')
    assert nodes[1] == dag.Node('2')
    assert nodes[2] == dag.Node('5')
    assert nodes[3] == dag.Node('3')
    assert nodes[4] == dag.Node('4')


# Test a dfs call for a 6 one way graph
def test_graph_read_dfs_6_node1():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/6_node1.graph"))
    d.dfs_walk(g_nodes[0], dfs_callback)
    assert len(nodes) == 6
    assert g_nodes[0] == nodes[0]
    assert g_nodes[1] == nodes[1]
    assert g_nodes[3] == nodes[2]
    assert g_nodes[4] == nodes[3]
    assert g_nodes[5] == nodes[4]
    assert g_nodes[2] == nodes[5]

# Test a dfs call for a 6 one way graph with loop
def test_graph_read_dfs_6_node2():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/6_node2.graph"))
    d.dfs_walk(g_nodes[0], dfs_callback)
    assert len(nodes) == 6
    assert g_nodes[0] == nodes[0]
    assert g_nodes[1] == nodes[1]
    assert g_nodes[3] == nodes[2]
    assert g_nodes[5] == nodes[3]
    assert g_nodes[4] == nodes[4]
    assert g_nodes[2] == nodes[5]

# Test check loop for a 6 one way graph with loop
def test_graph_check_loop_6_node2():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/6_node2.graph"))
    assert d.check_loop(g_nodes[0]) == True

# Test a dfs call for a 6 one way graph with loop - 2
def test_graph_read_dfs_6_node3():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/6_node3.graph"))
    d.dfs_walk(g_nodes[0], dfs_callback)
    assert len(nodes) == 6
    assert g_nodes[0] == nodes[0]
    assert g_nodes[1] == nodes[1]
    assert g_nodes[3] == nodes[2]
    assert g_nodes[4] == nodes[3]
    assert g_nodes[5] == nodes[4]
    assert g_nodes[2] == nodes[5]

# Test a dfs call for a 13 one way graph
def test_graph_read_dfs_13_node1():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/13_node1.graph"))
    d.dfs_walk(g_nodes[0], dfs_callback)
    assert len(nodes) == 13
    assert nodes[0] == g_nodes[0]
    assert nodes[1] == g_nodes[1]
    assert nodes[2] == g_nodes[4]
    assert nodes[3] == g_nodes[5]
    assert nodes[4] == g_nodes[6]
    assert nodes[5] == g_nodes[2]
    assert nodes[6] == g_nodes[7]
    assert nodes[7] == g_nodes[8]
    assert nodes[8] == g_nodes[9]
    assert nodes[9] == g_nodes[3]
    assert nodes[10] == g_nodes[10]
    assert nodes[11] == g_nodes[11]
    assert nodes[12] == g_nodes[12]

# Test check loop call for a 13 one way graph
def test_graph_check_loop_13_node1():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/13_node1.graph"))
    assert d.check_loop(g_nodes[0]) == False

# Test check loop call for a 13 one way graph with loop
def test_graph_check_loop_13_node2():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/13_node2.graph"))
    assert d.check_loop(g_nodes[0]) == True

# A BFS callback
def bfs_callback(node : dag.Node, distance):
    nodes.append(node)
    node.label = 0

# Test a simple bfs call
def test_graph_bfs_simple():
    n1 = dag.Node('1', {})
    n2 = dag.Node('2', {})
    n3 = dag.Node('3', {})
    e2 = dag.Edge(n2, n3)
    e = dag.Edge(n1, n2)
    d = dag.Graph()
    d.addEdge(e)
    d.addEdge(e2)
    d.bfs_walk(n1, bfs_callback)
    assert len(nodes) == 3
    assert nodes[0] == n1
    assert nodes[1] == n2
    assert nodes[2] == n3

# Test a simple aother bfs call
def test_graph_bfs_another_simple():
    n1 = dag.Node('1', {})
    n2 = dag.Node('2', {})
    n3 = dag.Node('3', {})
    e2 = dag.Edge(n2, n3)
    e = dag.Edge(n1, n2)
    e3 = dag.Edge(n2, n1)
    d = dag.Graph()
    d.addEdge(e)
    d.addEdge(e2)
    d.addEdge(e3)
    d.bfs_walk(n2, bfs_callback)
    assert len(nodes) == 3
    assert nodes[0] == n2
    assert nodes[1] == n3
    assert nodes[2] == n1

# Test a bfs call
def test_graph_bfs_call1():
    n1 = dag.Node('1', {})
    n2 = dag.Node('2', {})
    n3 = dag.Node('3', {})
    n4 = dag.Node('4', {})
    n5 = dag.Node('5', {})
    e1 = dag.Edge(n1, n3)
    e2 = dag.Edge(n1, n2)
    e3 = dag.Edge(n3, n4)
    e4 = dag.Edge(n2, n5)
    d = dag.Graph()
    d.addEdge(e1)
    d.addEdge(e2)
    d.addEdge(e3)
    d.addEdge(e4)
    d.bfs_walk(n1, bfs_callback)
    assert len(nodes) == 5
    assert nodes[0] == n1
    assert nodes[1] == n3
    assert nodes[2] == n2
    assert nodes[3] == n4
    assert nodes[4] == n5

# Test a dfs call
def test_graph_bfs_call2():
    n1 = dag.Node('1', {})
    n2 = dag.Node('2', {})
    n3 = dag.Node('3', {})
    n4 = dag.Node('4', {})
    n5 = dag.Node('5', {})
    e1 = dag.Edge(n1, n3)
    e2 = dag.Edge(n1, n2)
    e3 = dag.Edge(n3, n4)
    e4 = dag.Edge(n2, n5)
    d = dag.Graph()
    d.addEdge(e1)
    d.addEdge(e2)
    d.addEdge(e3)
    d.addEdge(e4)
    d.dfs_walk(n1, dfs_callback)
    assert len(nodes) == 5
    assert nodes[0] == n1
    assert nodes[1] == n3
    assert nodes[2] == n4
    assert nodes[3] == n2
    assert nodes[4] == n5

def bfs_callback_number(node : dag.Node, distance):
    node.label = 0
    if len(nodes) == 0:
        nodes.append([node])
    else:
        if len(nodes) == distance:
            nodes.append([node])
        else:
            nodes[distance].append(node)

# Test a bfs call with numbering every visited node
def test_graph_bfs_call3():
    n1 = dag.Node('1', {})
    n2 = dag.Node('2', {})
    n3 = dag.Node('3', {})
    n4 = dag.Node('4', {})
    n5 = dag.Node('5', {})
    e1 = dag.Edge(n1, n3)
    e2 = dag.Edge(n1, n2)
    e3 = dag.Edge(n3, n4)
    e4 = dag.Edge(n2, n5)
    d = dag.Graph()
    d.addEdge(e1)
    d.addEdge(e2)
    d.addEdge(e3)
    d.addEdge(e4)
    d.bfs_walk(n1, bfs_callback_number)
    assert len(nodes) == 3
    assert len(nodes[0]) == 1
    assert nodes[0][0] == n1
    assert len(nodes[1]) == 2
    assert nodes[1][0] == n3
    assert nodes[1][1] == n2
    assert len(nodes[2]) == 2
    assert nodes[2][0] == n4
    assert nodes[2][1] == n5

# Test a bfs number walk
def test_graph_bfs_walk_number():
    n1 = dag.Node('1', {})
    n2 = dag.Node('2', {})
    n3 = dag.Node('3', {})
    n4 = dag.Node('4', {})
    n5 = dag.Node('5', {})
    e1 = dag.Edge(n1, n3)
    e2 = dag.Edge(n1, n2)
    e3 = dag.Edge(n3, n4)
    e4 = dag.Edge(n2, n5)
    d = dag.Graph()
    d.addEdge(e1)
    d.addEdge(e2)
    d.addEdge(e3)
    d.addEdge(e4)
    ns = d.bfs_walk_number(n1)
    assert len(ns) == 3
    assert len(ns[0]) == 1
    assert ns[0][0] == n1
    assert len(ns[1]) == 2
    assert ns[1][0] == n3
    assert ns[1][1] == n2
    assert len(ns[2]) == 2
    assert ns[2][0] == n4
    assert ns[2][1] == n5

def test_graph_bfs_walk_number_8_node1():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/8_node1.graph"))
    g = d.bfs_walk_number(g_nodes[0])
    assert len(g) == 7


def test_graph_read_dfs_5_node2():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/5_node3.graph"))
    n = d.bfs_walk_number(g_nodes[0])
    assert len(n) == 3
    assert len(n[0]) == 1
    assert len(n[1]) == 2
    assert len(n[2]) == 2
    assert n[0][0] == g_nodes[0]
    assert n[1][0] == g_nodes[1]
    assert n[1][1] == g_nodes[2]
    assert n[2][0] == g_nodes[3]
    assert n[2][1] == g_nodes[4]
    assert d.check_loop(g_nodes[0]) is False

def test_graph_read_dfs_6_node4():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/6_node4.graph"))
    n = d.bfs_walk_number(g_nodes[0])
    assert len(n) == 4
    assert len(n[0]) == 1
    assert len(n[1]) == 3
    assert len(n[2]) == 1
    assert len(n[3]) == 1
    assert n[0][0] == g_nodes[0]
    assert n[1][0] == g_nodes[1]
    assert n[1][1] == g_nodes[2]
    assert n[1][2] == g_nodes[3]
    assert n[2][0] == g_nodes[4]
    assert n[3][0] == g_nodes[5]

def test_graph_read_dfs_5_node4():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/5_node4.graph"))
    n = d.bfs_walk_number(g_nodes[0])
    assert len(n) == 4
    assert len(n[0]) == 1
    assert len(n[1]) == 2
    assert len(n[2]) == 1
    assert len(n[3]) == 1
    assert n[0][0] == g_nodes[0]
    assert n[1][0] == g_nodes[1]
    assert n[1][1] == g_nodes[2]
    assert n[2][0] == g_nodes[3]
    assert n[3][0] == g_nodes[4]

def test_graph_read_dfs_7_node1():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/7_node1.graph"))
    n = d.bfs_walk_number(g_nodes[0])
    assert len(n) == 5
    assert len(n[0]) == 1
    assert len(n[1]) == 2
    assert len(n[2]) == 2
    assert len(n[3]) == 1
    assert len(n[4]) == 1
    assert n[0][0] == g_nodes[0]
    assert n[1][0] == g_nodes[2]
    assert n[1][1] == g_nodes[3]
    assert n[2][0] == g_nodes[1]
    assert n[2][1] == g_nodes[5]
    assert n[3][0] == g_nodes[4]
    assert n[4][0] == g_nodes[6]

def test_graph_equal1():
    g = dag.Graph()
    n1 = dag.Node("1", {})
    n2 = dag.Node("2", {})
    n3 = dag.Node("3", {})
    g.addEdge(dag.Edge(n1, n2))
    g.addEdge(dag.Edge(n1, n3))
    d, _ = read_graph(os.path.join(base_path, "test_graphs/3_node5.graph"))
    assert d == g

def test_graph_equal():
    g = dag.Graph()
    n1 = dag.Node("1", {})
    n2 = dag.Node("2", {})
    n3 = dag.Node("3", {})
    n4 = dag.Node("4", {})
    g.addEdge(dag.Edge(n1, n2))
    g.addEdge(dag.Edge(n1, n3))
    g.addEdge(dag.Edge(n2, n4))
    d, _ = read_graph(os.path.join(base_path, "test_graphs/3_node5.graph"))
    assert d != g

# Test a dfs call for a 7 one way graph
def test_graph_walk_number_7_node2():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/7_node2.graph"))
    n = d.walk_number()
    assert len(n) == 7
    assert len(n[0]) == 1
    assert len(n[1]) == 1
    assert len(n[2]) == 1
    assert len(n[3]) == 1
    assert len(n[4]) == 1
    assert len(n[5]) == 1
    assert len(n[6]) == 1
    assert n[0][0] == g_nodes[0]
    assert n[1][0] == g_nodes[1]
    assert n[2][0] == g_nodes[2]
    assert n[3][0] == g_nodes[3]
    assert n[4][0] == g_nodes[4]
    assert n[5][0] == g_nodes[6]
    assert n[6][0] == g_nodes[5]

# Test a dfs call for a 5 one way graph
def test_graph_walk_number_5_node5():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/5_node5.graph"))
    n = d.walk_number()
    assert len(n) == 5
    assert len(n[0]) == 1
    assert len(n[1]) == 1
    assert len(n[2]) == 1
    assert len(n[3]) == 1
    assert len(n[4]) == 1
    assert n[0][0] == g_nodes[0]
    assert n[1][0] == g_nodes[1]
    assert n[2][0] == g_nodes[2]
    assert n[3][0] == g_nodes[3]
    assert n[4][0] == g_nodes[4]

# Test a dfs call for a 9 one way graph
def test_graph_walk_number_9_node1():
    d, g_nodes = read_graph(os.path.join(base_path, "test_graphs/9_node1.graph"))
    n = d.walk_number()
    assert len(n) == 5
    assert len(n[0]) == 2
    assert len(n[1]) == 2
    assert len(n[2]) == 2
    assert len(n[3]) == 2
    assert len(n[4]) == 1
    assert n[0][0] == g_nodes[0]
    assert n[0][1] == g_nodes[5]
    assert n[1][0] == g_nodes[1]
    assert n[1][1] == g_nodes[6]
    assert n[2][0] == g_nodes[2]
    assert n[2][1] == g_nodes[7]
    assert n[3][0] == g_nodes[3]
    assert n[3][1] == g_nodes[8]
    assert n[4][0] == g_nodes[4]

def test_get_metadata1():
    n = dag.Node("k", {})
    assert n.getMetadata() == {}

def test_get_metadata2():
    n = dag.Node("k", {})
    assert n.getMetadata("a") == None

def test_get_metadata3():
    n = dag.Node("k", {"a": 4})
    assert n.getMetadata("a") == 4

def test_get_metadata4():
    n = dag.Node("k", {"a": 4})
    assert n.getMetadata()["a"] == 4

def test_set_metadata1():
    n = dag.Node("k", {})
    n.setMetadata("a", 4)
    assert n.getMetadata()["a"] == 4

def test_get_metadata_edges():
    n1 = dag.Node("a", {"a": 1})
    n2 = dag.Node("b", {"a": 2})
    n3 = dag.Node("c", {"a": 3})
    e1 = dag.Edge(n1, n2)
    e2 = dag.Edge(n2, n3)
    g = dag.Graph()
    g.addEdge(e1)
    g.addEdge(e2)
    for n in g.upToEdges(dag.Node("b", {})):
        assert n.getMetadata("a") == 1
