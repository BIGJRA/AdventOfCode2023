import time
from collections import Counter, deque
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from math import gcd, lcm
from operator import __mul__

from aocd import get_data, post

sample1 = '''7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ'''

sample2 = '''...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........'''

sample3 = '''.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...'''

sample4 = '''FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L'''

lines = get_data().splitlines()

# lines = sample.splitlines()

def solve(p):
    def get_symbol(x, y):
        try:
            return new_lines[y][x]
        except:
            return '.'
    def get_neighbors(x, y, symbol):
        match symbol:
            case "|": return [(x, y - 1), (x, y + 1)]
            case "-": return [(x - 1, y), (x + 1, y)]
            case "L": return [(x, y - 1), (x + 1, y)]
            case "F": return [(x, y + 1), (x + 1, y)]
            case "J": return [(x, y - 1), (x - 1, y)]
            case "7": return [(x, y + 1), (x - 1, y)]

    new_lines = deepcopy(lines)
    m, n = len(new_lines[0]), len(new_lines)
    dis = None
    for y, line in enumerate(new_lines):
        for x, char in enumerate(line):
            if char == "S":
                dis = {(x, y): 0}
                q = deque()
                syms = []
                if x >= 1 and get_symbol(x-1, y) in ('-', 'L', 'F'):
                    q.append((x - 1, y, 1))
                    syms.append({'-', '7', 'J'})
                if x < m - 1 and get_symbol(x+1, y) in ('-', '7', 'J'):
                    q.append((x + 1, y, 1))
                    syms.append({'-', 'L', 'F'})
                if y >= 1 and get_symbol(x,y-1) in ('|', '7', 'F'):
                    q.append((x, y - 1, 1))
                    syms.append({'|', 'L', 'J'})
                if y < n - 1 and get_symbol(x,y+1) in ('|', 'L', 'J'):
                    q.append((x, y + 1, 1))
                    syms.append({'|', '7', 'F'})
                break
        if dis is not None:
            break
    new_lines[y] = new_lines[y].replace("S", list(syms[0].intersection(syms[1]))[0])

    while q:
        curr_x, curr_y, curr_d = q.popleft()
        dis[(curr_x, curr_y)] = curr_d
        curr_sym = get_symbol(curr_x, curr_y)
        for next_x, next_y in get_neighbors(curr_x, curr_y, curr_sym):
            if (next_x, next_y) not in dis and 0 <= next_x < m and 0 <= next_y < n:
                q.append((next_x, next_y, curr_d + 1))
    #print(q, dis)
    if p == 1:
        return max(dis.values())
    total = 0
    for y, line in enumerate(new_lines):
        for x, char in enumerate(line):
            if (x,y) in dis:
                #print(x,y)
                continue
            curr = (x,y)
            jumps = 0
            while curr[0] >= 0 and curr[1] >= 0:
                curr = curr[0] - 1, curr[1] - 1
                if curr in dis and get_symbol(curr[0], curr[1]) not in ('7','L'):
                    jumps += 1
            if jumps % 2 == 1:
                #print(x,y)
                total += 1

    #print(total)
    return total

lines = sample1.splitlines()
assert(solve(1) == 8)

lines = sample2.splitlines()
assert(solve(2) == 4)

lines = sample3.splitlines()
assert(solve(2) == 8)

lines = sample4.splitlines()
assert(solve(2) == 10)


lines = get_data().splitlines()


p1 = solve(1)
print(p1)
# post.submit(p1)

p2 = solve(2)
print(p2)
post.submit(p2)
