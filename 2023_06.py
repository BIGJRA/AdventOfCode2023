from functools import reduce
from operator import __mul__

from aocd import get_data, post
from common import *


def solve(data, p):
    lines = data.splitlines()
    races = list(zip(map(int, lines[0].split()[1:]), map(int, lines[1].split()[1:]))) if p == 1 else \
        [(int(''.join((lines[0].split()[1:]))), int(''.join((lines[1].split()[1:]))))]
    return reduce(__mul__, [(sum([bt * (t - bt) > record for bt in range(t + 1)])) for t, record in races])


s1 = '''Time:      7  15   30
Distance:  9  40  200'''

tests = {
    s1: (288, 71503)
}

test_assertions(tests, solve)

input_data = get_data(day=6, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=6, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=6, year=2023)
