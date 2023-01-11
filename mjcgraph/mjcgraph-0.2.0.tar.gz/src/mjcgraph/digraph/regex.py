#!/usr/local/bin/python3

import sys
from mjcgraph.digraph import digraph
from mjcgraph.digraph import digraphdfs
from collections import deque


class Regex():
    def __init__(self, regexp):
        self.re = regexp.strip()
        self.M = len(self.re)
        ops = deque()
        self.DG = digraph.Digraph(self.M + 1)

        for i in range(self.M):
            lp = i
            if self.re[i] == '(' or self.re[i] == '|':
                ops.append(i)
            elif self.re[i] == ')':
                opr = ops.pop()
                if self.re[opr] == '|':
                    lp = ops.pop()
                    self.G.add_edge(lp, opr+1)
                    self.G.add_edge(opr, i)
                elif self.re[opr] == '(':
                    lp = opr
                else:
                    assert False

            if i < self.M-1 and self.re[i+1] == '*':
                self.DG.add_edge(lp, i+1)
                self.DG.add_edge(i+1, lp)
            if self.re[i] == '(' or self.re[i] == '*' or self.re[i] == ')':
                self.DG.add_edge(i, i+1)
        if len(ops) != 0:
            raise Exception('invalid regular expression {}'.format(regexp))


    def match(self, text):
        dfs = digraphdfs.DirectedDFSearch(self.DG, 0)
        pc = set()
        invalid = set(['*', '|', '(', ')'])
        for v in range(self.DG.V):
            if dfs.is_marked(v):
                pc.add(v)

        for i in range(len(text)):
            if text[i] in invalid:
                raise Exception('text has metacharacter: {}'.format(text[i]))

            match = []
            for v in pc:
                if v == self.M:
                    continue
                if self.re[v] == text[i] or self.re[v] == '.':
                    match.append(v+1)

                if len(match) == 0:
                    continue

                dfs = digraphdfs.DirectedDFSearch(self.DG, match);
                pc = set()
                for v in range(self.DG.V):
                    if (dfs.is_marked(v)):
                        pc.add(v)

                if len(pc) == 0:
                    return False # if no reacable states, finish early

            for v in pc:
                if v == self.M:
                    return True
        return False


if __name__ == '__main__':
    re = Regex('(A*B|AC)D')
    matches = ['BD', 'ABD', 'AABD', 'ACD', 'ACDD']
    assert re.match('X') == False
    assert re.match('B') == False
    for m in matches:
        assert re.match(m) == True

    re = Regex('(A*B|A.*C)D')
    assert re.match('AXYHFED') == False
    matches = matches + ['AXCD', 'AXYCD', 'AXYZCD']
    for m in matches:
        assert re.match(m) == True

    # '*' 0 or more
    re = Regex('(|A)B')
    assert re.match('B') == True
    assert re.match('AB') == True

    # '+' 1 or more
    re = Regex('AB(AB)*')
    assert re.match('AB') == True
    assert re.match('ABAB') == True
    assert re.match('ABABAB') == True

    re = Regex('(0|(1(01*(00)*0)*1)*)*')
    matches = ['11', '011', '110', '1001', '1100', '1111', '10010']
    for m in matches:
        assert re.match(m) == True


    print('passed')
