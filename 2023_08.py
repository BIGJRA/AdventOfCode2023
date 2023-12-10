from functools import reduce
from math import lcm

from aocd import get_data
from common import *

def solve(data, p):
    lines = data.splitlines()
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


s1 = '''RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
'''
s2 = '''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)'''
s3 = '''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)'''

tests = {
    s1: (2, None),
    s2: (6, None),
    s3: (None, 6)
}

test_assertions(tests, solve)

input_data = get_data(day=8, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=8, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=8, year=2023)
