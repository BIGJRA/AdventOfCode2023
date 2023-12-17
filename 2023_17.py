import queue
from collections import deque

from aocd import get_data, post
from common import *


def solve(data, p):
    lines = data.splitlines()
    num_rows = len(lines)
    num_cols = len(lines[0])
    coord_map = {}
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            coord_map[(row, col)] = int(char)

    move_params = [(1, 3), (4, 10)] # min then max for parts 1 and 2

    # priority is score, then state
    pq = queue.PriorityQueue()

    # we start with the first moves completed at zero score to make it simpler to start
    pq.put((coord_map[(0, 1)], ((0, 1), (0, 0), 1)))
    pq.put((coord_map[(1, 0)], ((1, 0), (0, 0), 1)))

    # states: location, previous position, straight moves
    scores = {((0, 0), (0, 0), 0): 0}

    while pq:
        score, (pos, prev, length) = pq.get()

        if pos == (num_rows - 1, num_cols - 1) and length >= move_params[p - 1][0]: # need to be at least min length
            return score

        for adj in ((pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)):
            if adj == prev or not (0 <= adj[0] < num_rows) or not (0 <= adj[1] < num_cols): # check in bounds and not repeat
                continue

            if (adj[0] - pos[0] == pos[0] - prev[0]) and (adj[1] - pos[1] == pos[1] - prev[1]):  # following line
                if length == move_params[p - 1][1]: # MUST turn if we are already at the max length
                    continue
                next_length = length + 1
            else:  # not in same line; attempting a turn
                if length < move_params[p - 1][0]: # CANNOT turn if we are not yet at minimum length
                    continue
                next_length = 1

            next_state = adj, pos, next_length
            new_score = score + coord_map[adj]
            if next_state not in scores or new_score < scores[next_state]:
                scores[next_state] = new_score
                pq.put((new_score, next_state))

s1 = '''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''

s2 = '''111111111111
999999999991
999999999991
999999999991
999999999991'''

tests = {
    s1: (102, 94),
    s2: (None, 71)
}

test_assertions(tests, solve)

input_data = get_data(day=17, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=17, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=17, year=2023)
