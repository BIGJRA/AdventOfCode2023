from functools import lru_cache

from aocd import get_data, post
from common import *


def solve(data, p):
    @lru_cache
    def hash(word):
        ans = 0
        for char in word:
            ans = ((ans + ord(char)) * 17) % 256
        return ans

    strings = data.split(',')
    if p == 1:
        return sum([hash(s) for s in strings])
    hashmap = {i: list() for i in range(256)}
    lengths = {}
    for s in strings:
        if '-' in s:
            label = s[:s.find('-')]
            if label in lengths:
                hashmap[hash(label)].remove(label)
                del lengths[label]
        elif '=' in s:
            label, focal_length = s[:s.find('=')], int(s[s.find('=') + 1])
            if label not in lengths:
                hashmap[hash(label)].append(label)
            lengths[label] = focal_length
    return sum(
        [(hash(label) + 1) * (hashmap[hash(label)].index(label) + 1) * length for label, length in lengths.items()])


s1 = '''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'''

tests = {
    s1: (1320, 145)
}

test_assertions(tests, solve)

input_data = get_data(day=15, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=15, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=15, year=2023)
