from i2 import Sig
from meshed import DAG, FuncNode
from meshed.base import _func_nodes_to_graph_dict
from meshed.dag import _separate_func_nodes_and_var_nodes
from meshed.itools import topological_sort

# separate with comments lines
def pairs(xs):
    if len(xs) <= 1:
        return xs
    else:
        pairs = list(zip(xs, xs[1:]))
    return pairs


def mk_mock_funcnode(arg, out):
    @Sig(arg)
    def func():
        pass

    # name = "_mock_" + str(arg) + "_" + str(out)  # f-string
    name = f'_mock_{str(arg)}_{str(out)}'  # f-string

    return FuncNode(func=func, out=out, name=name)


def funcnodes_from_pairs(pairs):
    return list(map(mk_mock_funcnode_from_tuple, pairs))


def curry(func):
    def res(*args):
        return func(tuple(args))

    return res


def uncurry(func):
    def res(tup):
        return func(*tup)

    return res


mk_mock_funcnode_from_tuple = uncurry(mk_mock_funcnode)


def reorder_on_constraints(funcnodes, outs):
    extra_nodes = funcnodes_from_pairs(pairs(outs))
    funcnodes += extra_nodes
    graph = _func_nodes_to_graph_dict(funcnodes)
    nodes = topological_sort(graph)
    print('after ordering:', nodes)
    ordered_nodes = [node for node in nodes if node not in extra_nodes]
    func_nodes, var_nodes = _separate_func_nodes_and_var_nodes(ordered_nodes)

    return func_nodes, var_nodes
