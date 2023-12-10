from functools import reduce
from operator import __mul__

from aocd import get_data

sample = '''Time:      7  15   30
Distance:  9  40  200'''

lines = get_data().splitlines()

# lines = sample.splitlines()


def solve(p):
    races = list(zip(map(int, lines[0].split()[1:]), map(int, lines[1].split()[1:]))) if p == 1 else \
        [(int(''.join((lines[0].split()[1:]))), int(''.join((lines[1].split()[1:]))))]
    return reduce(__mul__, [(sum([bt * (t - bt) > record for bt in range(t + 1)])) for t, record in races])

p1 = solve(1)
print(p1)
#post.submit(p1)

p2 = solve(2)
print(p2)
#post.submit(p2)

