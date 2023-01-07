#!/usr/local/bin/python3

import sys
import graphviz

class Draw:
    def __init__(self, digraph=False):
        if digraph:
            self.g = graphviz.Digraph()
        else:
            self.g = graphviz.Graph()
        self.g.engine = 'neato'
        self.g.attr('node', margin='0', fontsize='4',
                    fontcolor='white', color='black', shape='circle',
                    style='filled', width='0.1')
        self.g.attr('edge', color='grey', penwidth='0.75')

        self.names = []


    def set_names(self, names):
        self.names = names


    def get_name(self, v):
        if len(self.names) != 0:
            return self.names[v]
        else:
            return str(v)


    def node_attr(self, **kwargs):
        self.g.attr('node', **kwargs)


    def edge_attr(self, **kwargs):
        self.g.attr('edge', **kwargs)


    def draw(self, Graph, path=[]):
        for v in range(Graph.V):
            self.g.node(self.get_name(v))

        pset = set()
        if len(path) >= 2:
            for i in range(len(path) - 1):
                pset.add((path[i], path[i+1]))
                pset.add((path[i+1], path[i]))

        seen = set()
        for v, e in enumerate(Graph.G):
            for w in e:
                vname = self.get_name(v)
                wname = self.get_name(w)
                if not (w, v) in seen:
                    if (w, v) in pset:
                        self.g.edge(vname, wname, color='black', penwidth='2.5')
                    else:
                        self.g.edge(vname, wname)
                    seen.add((v,w))

        self.g.view()
