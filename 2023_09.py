import time
from collections import Counter, deque
from dataclasses import dataclass
from functools import reduce
from math import gcd, lcm
from operator import __mul__

from aocd import get_data, post

sample = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45'''

lines = get_data().splitlines()

#lines = sample.splitlines()

def solve(p):
    total = 0
    for l in lines:
        diffs = [list(map(int, l.split()))]
        while diffs[-1].count(0) != len(diffs[-1]):
            nxt = []
            prv = diffs[-1][0]
            for thing in diffs[-1][1:]:
                nxt.append(thing - prv)
                prv = thing
            diffs.append(nxt)
        diffs.reverse()
        diffs[0].append(0)
        for pos, d in enumerate(diffs[1:]):
            if p == 2: # To go backwards, we want to append to the left side. Here reversing each list works
                d.reverse()
            if p == 1:
                d.append(d[-1] + diffs[pos][-1])
            elif p == 2:
                d.append(d[-1] - diffs[pos][-1])
        total += diffs[-1][-1]

    return total


p1 = solve(1)
print(p1)
# post.submit(p1)

p2 = solve(2)
print(p2)
# post.submit(p2)

