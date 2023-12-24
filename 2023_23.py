from collections import deque, defaultdict
from copy import deepcopy

from aocd import get_data, post
from common import *


def solve(data, p):
    lines = data.splitlines()
    num_rows, num_cols = len(lines), len(lines[0])
    start, end = (0,1), (num_rows - 1, num_cols - 2)
    features = {(-1, 1): "#", (num_rows, num_cols - 2): "#"}
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            features[(row, col)] = char
    graph = {start: set(), end: set()}
    for row, col in features:
        if row == 0 or row == num_rows - 1 or col == 0 or col == num_cols:
            continue
        if features[(row, col)] != "#":
            count = sum([features[(row + r0, col + c0)] != '#' for (r0, c0) in ((0, 1), (1, 0), (-1, 0), (0, -1))])
            if count >= 3:
                graph[(row, col)] = set()
    start = (0, 1)
    q = deque([((1, 1), start, 1, (0, 1))])
    slopes = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
    while q:
        coords, last_junction, steps, prev = q.popleft()
        if coords in graph:
            graph[last_junction].add((coords, steps))
            if coords == end:
                continue
            for slope, d in slopes.items():
                new = coords[0] + d[0], coords[1] + d[1]
                if features[new] == '#' or new == prev:
                    continue
                q.append((new, coords, 1, coords))
        else:
            for slope, d in slopes.items():
                new = coords[0] + d[0], coords[1] + d[1]
                if features[new] == '#' or new == prev:
                    continue
                if features[coords] in slopes and slopes[features[coords]] != d:
                    continue
                q.append((new, last_junction, steps + 1, coords))
    if p == 2:
        for g in graph:
            if g != start:
                for n, d in graph[g]:
                    graph[n].add((g, d))
    q = deque([(start, 0, set())])
    best = 0
    while q:
        curr, steps, vis = q.popleft()
        if curr == end:
            if steps > best:
                best = steps
            continue
        new_vis = vis.copy()
        new_vis.add(curr)
        for adj, d in graph[curr]:
            if adj in vis:
                continue
            q.append((adj, steps + d, new_vis))
    return best

s1 = '''#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#'''

tests = {
    s1: (94, 154)
}

test_assertions(tests, solve)

input_data = get_data(day=23, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=23, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=23, year=2023)
