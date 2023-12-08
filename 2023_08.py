import time
from collections import Counter
from dataclasses import dataclass
from functools import reduce
from math import gcd, lcm
from operator import __mul__

from aocd import get_data, post

sample = '''LR

AAA = (ZZZ, ZZZ)
11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
ZZZ = (ZZZ, ZZZ)'''

lines = get_data().splitlines()

#lines = sample.splitlines()

def solve(p):
    moves = lines[0]
    nodes = {line.split(' = ')[0]: tuple(line.split('(')[1][:-1].split(', ')) for line in lines[2:]}

    if p == 1:
        curr = ['AAA']
    elif p == 2:
        curr = list(filter(lambda x: x[-1] == 'A', nodes))
    count = 0
    periods = [None for _ in curr]
    while True:
        for pos, n in enumerate(curr): # update each node to its next move
            curr[pos] = nodes[n][moves[count % len(moves)] == "R"]
        count += 1

        # Note that each sequence is observed (manual testing) to be at "..Z" precisely at period * x
        # for all whole x, for some period. Here we find each of these periods, aka the first instance
        # when ..Z is reached for each starting position.
        for pos, n in enumerate(curr): # update each period if ..Z is found
            if n[-1] == 'Z' and not periods[pos]:
                periods[pos] = count
        # once all periods are found the least common multiple of all periods is the first acceptable answer
        if all(periods):
            return reduce(lcm, periods)



p1 = solve(1)
print(p1)
# post.submit(p1)

p2 = solve(2)
print(p2)
# post.submit(p2)

