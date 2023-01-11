"""
    Copyright 2022 Stéphane De Mita

    lzmp is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    lzmp is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with lzmp.  If not, see <http://www.gnu.org/licenses/>.
"""

import lzmp, random, math, time

def f(sd):
    t0 = time.time()
    s = 0
    s2 = 0
    n = 1000000
    for _ in range(n):
        x = random.normalvariate(0, sd)
        s += x
        s2 += x**2
    m = s/n
    m2 = s2/n
    sd = math.sqrt((m2 - m**2) * n/(n-1))
    return m, sd, time.time() - t0

def finalize(results):
    return zip(*results)

def f2(num):
    t0 = time.time()
    for _ in range(num):
        x = random.normalvariate(0, 1)
    return time.time() - t0  

def main():
    x = [0, 0.01, 0.1, 1, 10]
    for nt in 1, 2, 4, 120:
        print(f'requested threads: {nt}')
        t0 = time.time()
        m, sd, ti = lzmp.run(f, lzmp.wrap(x), final=finalize, max_threads=nt)
        t = time.time() - t0

        print(f'    computed mean: ' + ' '.join(format(i, '.1e') for i in m))
        print(f'    computed stdev: ' + ' '.join(format(i, '.4f') for i in sd))
        print('    time per process:', ' '.join(format(i, '.2f') for i in ti))
        print(f'    summed time: {sum(ti):.2f}')
        print(f'    time main: {t:.2f}')

    print('intentionally cause an exception')
    try:
        m, sd, ti = lzmp.run(f, lzmp.wrap([1, 2, 'error', 3]), final=finalize, max_threads=4)
    except RuntimeError as e:
        print(f'   exception caught: "{str(e)[:30]}..."')
    else: raise RuntimeError('expected exception did not occur')

    print('echo arguments (use to make a dictionary)')
    print(dict(lzmp.run(f2, lzmp.wrap(range(10000, 100001, 10000)), echo=True)))

    return 0

if __name__ == '__main__':
    main()
