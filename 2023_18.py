from aocd import get_data, post
from common import *


def solve(data, p):
    lines = data.splitlines()

    # https://en.wikipedia.org/wiki/Shoelace_formula
    def get_area(c): # input is corner coordinates, outputs area of polygon
        return sum(c[i][0] * c[i + 1][1] - c[i][1] * c[i + 1][0] for i in range(len(c) - 1)) // 2

    # https://en.wikipedia.org/wiki/Pick's_theorem
    def get_internal_points(area, bp_count):
        return area - (bp_count // 2) + 1

    corner_points = [(0, 0)]
    num_boundary_points = 0
    curr = (0, 0)
    moves = {'R': (1, 0), 'D': (0, 1), 'L': (-1, 0), 'U': (0, -1),
             '0': (1, 0), '1': (0, 1), '2': (-1, 0), '3': (0, -1)}
    for line in lines:
        d, l, code = line.split()[0], int(line.split()[1]), line.split()[2][2:-1]
        if p == 2:
            d, l = code[5], int("0x" + code[:5], 16)
        curr = curr[0] + l * moves[d][0], curr[1] + l * moves[d][1]
        num_boundary_points += l
        corner_points.append(curr)
    return get_internal_points(get_area(corner_points), num_boundary_points) + num_boundary_points


s1 = '''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''

tests = {
    s1: (62, 952408144115)
}

test_assertions(tests, solve)

input_data = get_data(day=18, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=18, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=18, year=2023)
