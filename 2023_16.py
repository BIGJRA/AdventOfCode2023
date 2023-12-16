from collections import deque

from aocd import get_data, post
from common import *


def solve(data, p):

    def safe_append(t, q, vis):
        if t not in vis:
            q.append(t)
            vis.add(t)

    lines = data.splitlines()
    num_rows, num_cols = len(lines), len(lines[0])
    starts = [((-1, 0), (1, 0))]
    if p == 2:
        starts += [((-1, y), (1, 0)) for y in range(1, num_rows)] + [((num_cols, y), (-1, 0)) for y in range(num_rows)]
        starts += [((x, -1), (0, 1)) for x in range(num_cols)] + [((x, num_rows), (0, -1)) for x in range(num_cols)]
    best = 0
    for start in starts:
        q = deque([start])  # Queue state is light position, direction
        vis = set()

        while q:
            pos, d = q.popleft()
            x, y = pos
            dx, dy = d

            nx, ny = (x + dx, y + dy)
            if nx < 0 or nx >= num_cols or ny < 0 or ny >= num_rows:
                continue

            if lines[ny][nx] == "." or (lines[ny][nx] == "|" and dy != 0) or (lines[ny][nx] == "-" and dx != 0):
                safe_append(((nx, ny), (dx, dy)), q, vis)
            elif lines[ny][nx] == '\\':
                safe_append(((nx, ny), (dy, dx)), q, vis)
            elif lines[ny][nx] == '/':
                safe_append(((nx, ny), (-dy, -dx)), q, vis)
            elif lines[ny][nx] == '-':
                safe_append(((nx, ny), (1, 0)), q, vis)
                safe_append(((nx, ny), (-1, 0)), q, vis)
            elif lines[ny][nx] == '|':
                safe_append(((nx, ny), (0, 1)), q, vis)
                safe_append(((nx, ny), (0, -1)), q, vis)
        best = max(best, len(set(v[0] for v in vis)))
    return best


s1 = r'''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....'''

tests = {
    s1: (46, 51)
}

test_assertions(tests, solve)

input_data = get_data(day=16, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=16, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=16, year=2023)
