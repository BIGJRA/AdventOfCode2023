from aocd import get_data, post
from common import *


def solve(data, p):
    lines = data.splitlines()
    m, n = len(lines[0]), len(lines)
    galaxies = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                galaxies.append((x,y))
    empty_rows = []
    empty_cols = []
    for r in range(n):
        if not any([g[1] == r for g in galaxies]):
            empty_rows.append(r)
    for c in range(m):
        if not any([g[0] == c for g in galaxies]):
            empty_cols.append(c)
    total = 0
    distance_multipliers = [2, 1000000]
    for pos, g1 in enumerate(galaxies):
        for g2 in galaxies[pos + 1:]:
            distance = 0
            for h_move in range(min(g1[0],g2[0]), max(g1[0],g2[0])):
                if h_move in empty_cols:
                    distance += distance_multipliers[p-1]
                else:
                    distance += 1
            for v_move in range(min(g1[1],g2[1]), max(g1[1],g2[1])):
                if v_move in empty_rows:
                    distance += distance_multipliers[p-1]
                else:
                    distance += 1
            total += distance

    return total

s1 = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''

tests = {
    s1: (374, None)
}

test_assertions(tests, solve)

input_data = get_data(day=11, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=11, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=11, year=2023)
