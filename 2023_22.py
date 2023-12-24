import re
from collections import deque
from copy import deepcopy

from aocd import get_data, post
from common import *


def solve(data, p):
    lines = data.splitlines()
    bricks = []
    for line in lines:
        tx0, ty0, tz0, tx1, ty1, tz1 = map(int, re.findall(r'\d+', line))
        bricks.append(sorted([[tx0, ty0, tz0], [tx1, ty1, tz1]]))
    n = len(bricks)
    bricks.sort(key=lambda x: x[0][2])  # bricks start in sorted by height order so they fall greedily

    # max_heights = defaultdict(lambda: (0, -1))  # based on (x,y), starts at (z=0,block_idx=-1)
    tops = {(x, y): (0, -1) for x in range(10) for y in range(10)}  # input has 0 <= x,y < 10, no need for DD
    supports = [set() for _ in range(n)]
    in_degrees = [0 for _ in range(n)]
    for pos, ((x0, y0, z0), (x1, y1, z1)) in enumerate(bricks):
        curr_tops = [tops[x, y] for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]
        target_z = max(u[0] + 1 for u in curr_tops)  # one above the tallest occupied point under our brick
        # filter for neighbors only includes the blocks that are one height less than target
        neighbors = {f[1] for f in filter(lambda u: u[1] != -1 and u[0] == target_z - 1, curr_tops)}
        for adj in neighbors:
            supports[adj].add(pos)
            in_degrees[pos] += 1
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                tops[(x, y)] = (target_z + (z1 - z0), pos)
    frees = 0
    cascades = 0
    for idx in range(n):
        in_deg = deepcopy(in_degrees)
        count = 0
        q = deque([idx])
        while q:  # we only care about what happens when blocks lose their single supports - Queue tracks only these
            curr = q.popleft()
            for neighbor in supports[curr]:
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    count += 1
                    q.append(neighbor)
        if count:  # P2 wants to see impact of deleting blocks - if >= 1 it is relevant here
            cascades += count
        else:  # P1 wants to see how many blocks have no impact
            frees += 1
    return frees if p == 1 else cascades


s1 = '''1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9'''

tests = {
    s1: (5, 7),
}

test_assertions(tests, solve)

input_data = get_data(day=22, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=22, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=22, year=2023)
