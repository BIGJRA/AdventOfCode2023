from collections import deque

from aocd import get_data, post
from common import *


def solve(data, p):
    def quadratic_lagrange(t0, t1, t2, target_x):
        result_y = 0
        result_y += ((target_x - t1[0]) * (target_x - t2[0]) // ((t0[0] - t1[0]) * (t0[0] - t2[0]))) * t0[1]
        result_y += ((target_x - t0[0]) * (target_x - t2[0]) // ((t1[0] - t0[0]) * (t1[0] - t2[0]))) * t1[1]
        result_y += ((target_x - t0[0]) * (target_x - t1[0]) // ((t2[0] - t0[0]) * (t2[0] - t1[0]))) * t2[1]
        return result_y

    def reduce(t):
        return t[0] % side_length, t[1] % side_length

    lines = data.splitlines()
    side_length = len(lines)  # assumes square - input is square with start directly in the middle
    rocks = set()
    start = None
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "S":
                start = row, col
            elif char == "#":
                rocks.add((row, col))
    tiles = [{start}, set()]  # even tiles, then odd tiles
    prev = deque([(start, 0)])
    diffs = []
    counts = []
    step = 0
    while not diffs or len(diffs) <= 2 or diffs[-1] - diffs[-2] != diffs[-2] - diffs[-3]:
        if not prev or (step == 64 and p == 1):
            break
        step += 1
        while prev[0][1] != step:
            tile, _ = prev.popleft()
            for adj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nxt = tile[0] + adj[0], tile[1] + adj[1]
                if p == 1 and (0 > nxt[0] or side_length <= nxt[0] or 0 > nxt[1] or side_length <= nxt[1]):
                    continue
                if reduce(nxt) in rocks or nxt in tiles[step % 2]:
                    continue
                tiles[step % 2].add(nxt)
                prev.append((nxt, step))
            if not prev:
                break

        if (step - start[0]) % side_length == 0:
            counts.append((step, len(tiles[step % 2])))
            if len(counts) >= 2:
                diffs.append(counts[-1][1] - counts[-2][1])
    if p == 1:
        return len(tiles[64 % 2])
    data_points = counts[-3:]
    return quadratic_lagrange(*data_points, 26501365)


s1 = '''...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........'''

tests = {
    s1: (42, None)
}

test_assertions(tests, solve)

input_data = get_data(day=21, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=21, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=21, year=2023)
