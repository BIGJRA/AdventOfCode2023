import re
import time
from collections import deque
from functools import lru_cache
from itertools import combinations

from aocd import get_data, post
from common import *


def solve(data, p):
    lines = data.splitlines()
    total = 0
    for line in lines:
        springs, blocks = line.split()
        blocks = tuple([int(i) for i in blocks.split(',')])
        if p == 2:
            springs = ((springs + '?') * 5)[:-1]  # multiply by 5, shear off last '?'
            blocks *= 5
        m, n = len(springs), len(blocks)
        cache = {}

        def dp(spring_idx, block_idx, curr_count):
            if (spring_idx, block_idx, curr_count) in cache:
                return cache[(spring_idx, block_idx, curr_count)]
            if spring_idx == m:
                if (block_idx == n and curr_count == 0) or (block_idx == n - 1 and curr_count == blocks[block_idx]):
                    return 1
                else:
                    return 0
            ans = 0
            for poss in [i for i in ['.', '#'] if i != {'.': '#', '#': '.'}.get(springs[spring_idx])]:
                if poss == '.':
                    if curr_count == 0:
                        ans += dp(spring_idx + 1, block_idx, 0)
                    elif curr_count > 0 and block_idx < n and curr_count == blocks[block_idx]:
                        ans += dp(spring_idx + 1, block_idx + 1, 0)
                elif poss == '#':
                    ans += dp(spring_idx + 1, block_idx, curr_count + 1)
            cache[(spring_idx, block_idx, curr_count)] = ans
            return ans

        score = dp(0, 0, 0)
        total += score
        continue

    return total


s1 = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1'''

tests = {
    s1: (21, 525152)
}

test_assertions(tests, solve)

input_data = get_data(day=12, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=12, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=12, year=2023)