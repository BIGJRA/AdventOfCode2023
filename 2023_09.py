from aocd import get_data
from common import *

def solve(data, p):
    lines = data.splitlines()
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


s1 = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45'''

tests = {
    s1: (114, 2)
}

test_assertions(tests, solve)

input_data = get_data(day=9, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=9, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=9, year=2023)
