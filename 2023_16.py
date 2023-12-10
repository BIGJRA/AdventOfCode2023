from aocd import get_data, post
from common import *


def solve(data, p):
    lines = data.splitlines()
    return p

s1 = '''
'''

tests = {
    s1: (0, 0)
}

test_assertions(tests, solve)

input_data = get_data(day=16, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=16, year=2023)

# p2 = solve(input_data, p=2)
# print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=16, year=2023)
