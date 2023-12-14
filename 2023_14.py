from dataclasses import dataclass

from aocd import get_data, post
from common import *


def solve(data, p):
    lines = data.splitlines()

    @dataclass
    class Board:
        m: int
        n: int
        circle_rocks: set
        square_rocks: set
        scores: list

        def hash(self):
            return self.getBoardScore(), hash(tuple(list(sorted(self.circle_rocks))))

        def addRock(self, x, y, is_circle):
            if is_circle:
                self.circle_rocks.add((x,y))
            else:
                self.square_rocks.add((x,y))

        def moveRock(self, x, y, dir):
            dest = None
            if dir == "E" or dir == "W":
                curr_x = x
                while True:
                    if dir == "E":
                        nxt = (curr_x + 1, y)
                        if nxt in self.circle_rocks or nxt in self.square_rocks or curr_x == self.n - 1:
                            dest = (curr_x, y)
                            break
                        curr_x += 1
                    elif dir == "W":
                        nxt = (curr_x - 1, y)
                        if nxt in self.circle_rocks or nxt in self.square_rocks or curr_x == 0:
                            dest = (curr_x, y)
                            break
                        curr_x -= 1
                    if dest is not None:
                        break
            elif dir == "N" or dir == "S":
                curr_y = y
                while True:
                    if dir == "S":
                        nxt = (x, curr_y + 1)
                        if nxt in self.circle_rocks or nxt in self.square_rocks or curr_y == self.m - 1:
                            dest = (x, curr_y)
                            break
                        curr_y += 1
                    elif dir == "N":
                        nxt = (x, curr_y - 1)
                        if nxt in self.circle_rocks or nxt in self.square_rocks or curr_y == 0:
                            dest = (x, curr_y)
                            break
                        curr_y -= 1
                    if dest is not None:
                        break
            self.circle_rocks.remove((x,y))
            self.circle_rocks.add(dest)

        def moveAllRocks(self, dir):
            if dir == "N" or dir == "S":
                for x in range(self.n):
                    if dir == "N":
                        for y in range(self.m):
                            if (x,y) in self.circle_rocks:
                                self.moveRock(x,y,dir)
                    elif dir == "S":
                        for y in range(self.m - 1, -1, -1):
                            if (x,y) in self.circle_rocks:
                                self.moveRock(x,y,dir)
            elif dir == "E" or dir == "W":
                for y in range(self.m):
                    if dir == "E":
                        for x in range(self.n - 1, -1, -1):
                            if (x,y) in self.circle_rocks:
                                self.moveRock(x,y,dir)
                    elif dir == "W":
                        for x in range(self.n):
                            if (x,y) in self.circle_rocks:
                                self.moveRock(x,y,dir)

        def cycle(self):
            for dir in ["N","W","S","E"]:
                self.moveAllRocks(dir)
            self.scores.append(self.getBoardScore())

        def getBoardScore(self):
            return sum([self.m - y for _x, y in self.circle_rocks])

    board = Board(len(lines), len(lines[0]), set(), set(), [])
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != '.':
                board.addRock(x, y, char == "O")
    board.scores.append(board.getBoardScore())
    if p == 1:
        board.moveAllRocks("N")
        return board.getBoardScore()
    elif p == 2:
        cycle_lookup = {}
        total_cycles = 10000
        for i in range(total_cycles):
            h = board.hash()
            if h in cycle_lookup:
                cycle_length = i - cycle_lookup[h]
                cycle_start = cycle_lookup[h]
                break
            else:
                cycle_lookup[h] = i
            board.cycle()
        desired = (1000000000 % cycle_length)
        while desired < cycle_start:
            desired += cycle_length
        return board.scores[desired]
    return p

s1 = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''

tests = {
    s1: (136, 64)
}

test_assertions(tests, solve)

input_data = get_data(day=14, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=14, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=14, year=2023)
