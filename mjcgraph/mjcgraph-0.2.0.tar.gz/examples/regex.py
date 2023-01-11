#!/usr/local/bin/python3

from mjcgraph.digraph import digraph
from mjcgraph.digraph import regex
from mjcgraph import draw


re = regex.Regex('(A*B|AC)D')

matches = ['BD', 'ABD', 'AABD', 'ACD', 'ACDD']
assert re.match('X') == False
assert re.match('B') == False
for m in matches:
    assert re.match(m) == True
    print(f'{m} matches regex {re.re}')

re = regex.Regex('(A*B|A.*C)D')
assert re.match('AXYHFED') == False
matches = matches + ['AXCD', 'AXYCD', 'AXYZCD']
for m in matches:
    assert re.match(m) == True
    print(f'{m} matches regex {re.re}')

# '*' 0 or more
re = regex.Regex('(|A)B')
assert re.match('B') == True
assert re.match('AB') == True

# '+' 1 or more
re = regex.Regex('AB(AB)*')
assert re.match('AB') == True
assert re.match('ABAB') == True
assert re.match('ABABAB') == True

re = regex.Regex('(0|(1(01*(00)*0)*1)*)*')
matches = ['11', '011', '110', '1001', '1100', '1111', '10010']
for m in matches:
    assert re.match(m) == True
    print(f'{m} matches regex {re.re}')
