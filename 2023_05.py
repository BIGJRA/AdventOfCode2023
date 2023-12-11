from collections import deque
from dataclasses import dataclass

from aocd import get_data, post
from common import *


def solve(data, p):
    @dataclass
    class MapVal:
        input: str
        output: str
        mapping: list  # of tuples

        def add_mapping(self, d_start, s_start, map_range):
            self.mapping.append((d_start, s_start, map_range))

        def translate(self, input_number):
            ans = input_number
            for o, i, r in self.mapping:
                if i <= input_number < i + r:
                    ans = input_number - i + o
            return ans

    lines = data.splitlines()
    seed_ints = []
    seed_string_list = lines[0].split(': ')[1].split()
    if p == 1:
        seed_ints = [(int(s), int(s)) for s in seed_string_list]
    if p == 2:
        for i in range(len(seed_string_list) // 2):
            s = int(seed_string_list[i * 2])
            r = int(seed_string_list[i * 2 + 1])
            seed_ints.append((s, s + r - 1))
    seed_ints.sort()

    map_lookup = {}
    map_val = None
    for line in lines[1:]:
        if ':' in line:
            i_str, _dummy, o_str = line[:line.find(' ')].split('-')
            map_val = MapVal(i_str, o_str, list())
            map_lookup[i_str] = map_val
        elif line != '':
            d, s, r = line.split()
            map_val.add_mapping(int(d), int(s), int(r))

    q = deque(map(lambda x: (x, "seed"), seed_ints))
    best = float('inf')
    while q:
        inter, stage = q.popleft()
        i_s, i_e = inter[0], inter[1]
        split = False
        for m in map_lookup[stage].mapping:  # chop up the intervals and put them back in queue if they split
            m_s, m_e = m[1], m[1] + m[2] - 1
            if i_s < m_s and i_e > m_e:  # Interval extends from map interval on both sides
                q.appendleft(((i_s, m_s - 1), stage))
                q.appendleft(((m_s, m_e), stage))
                q.appendleft(((m_e + 1, i_e), stage))
                split = True
                break
            elif m_s <= i_s <= m_e < i_e:  # Interval extends from map interval only on right
                q.appendleft(((i_s, m_e), stage))
                q.appendleft(((m_e + 1, i_e), stage))
                split = True
                break
            elif i_s < m_s <= i_e <= m_e:  # Interval extends from map interval only on left
                q.appendleft(((i_s, m_s - 1), stage))
                q.appendleft(((m_s, i_e), stage))
                split = True
                break
        if split:
            continue
        n_s, n_e,  = map_lookup[stage].translate(i_s), map_lookup[stage].translate(i_e)
        next_stage = map_lookup[stage].output
        if next_stage == "location":
            best = min(best, n_s)
        else:
            q.append(((n_s, n_e), next_stage))
    return best


s1 = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''

tests = {
    s1: (35, 46)
}

test_assertions(tests, solve)

input_data = get_data(day=5, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=5, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=5, year=2023)
