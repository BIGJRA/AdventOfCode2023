from dataclasses import dataclass

from aocd import get_data, post
from common import *


def solve(data, p):
    lines = data.splitlines()

    @dataclass
    class Map:
        input: str
        output: str
        mapping: list  # of tuples

        def addMapping(self, d_start, s_start, range):
            self.mapping.append((d_start, s_start, range))

        def translate(self, input_number):
            ans = input_number
            for o, i, r in self.mapping:
                if i <= input_number < i + r:
                    ans = input_number - i + o
            return ans

        def translateBack(self, output_number):
            ans = output_number
            for o, i, r in self.mapping:
                if o <= output_number < o + r:
                    ans = output_number - o + i
            return ans

    def solveForwards(p):
        seed_string_list = lines[0].split(': ')[1].split()
        if p == 1:
            seeds = [int(s) for s in seed_string_list]
        elif p == 2:
            seeds = set()
            for i in range(len(seed_string_list) // 2):
                s = int(seed_string_list[i * 2])
                r = int(seed_string_list[i * 2 + 1])
                seeds = seeds.union(set(range(s, s + r)))
            seeds = list(seeds)
        seeds.sort()

        map_lookup = {}
        for line in lines[1:]:
            if ':' in line:
                i_str, _dummy, o_str = line[:line.find(' ')].split('-')
                map = Map(i_str, o_str, list())
                map_lookup[i_str] = map
            elif line != '':
                d, s, r = line.split()
                map.addMapping(int(d), int(s), int(r))
        min_final = float('inf')
        for seed in seeds:
            curr = seed
            for m in map_lookup.values():
                nxt = m.translate(curr)
                curr = nxt
            min_final = min(min_final, curr)
        return min_final

    def solveBackwards(p):
        # work backwards lol
        seed_string_list = lines[0].split(': ')[1].split()
        seeds = []  # tuples: start and range
        if p == 1:
            seeds = [(int(s), 1) for s in seed_string_list]
        elif p == 2:
            seeds = [(int(seed_string_list[i]), int(seed_string_list[i + 1])) for i in
                     range(0, len(seed_string_list), 2)]

        map_lookup = {}
        for line in lines[1:]:
            if ':' in line:
                i_str, _dummy, o_str = line[:line.find(' ')].split('-')
                map = Map(i_str, o_str, list())
                map_lookup[o_str] = map  # maps are keyed by what they output to
            elif line != '':
                d, s, r = line.split()
                map.addMapping(int(d), int(s), int(r))

        location = -1
        while True:
            location += 1
            curr_num = location
            curr_str = "location"
            while curr_str != "seed":
                curr_map = map_lookup[curr_str]
                nxt_num = curr_map.translateBack(curr_num)
                nxt_str = curr_map.input
                curr_num, curr_str = nxt_num, nxt_str
            for s, r in seeds:
                if s <= curr_num < s + r:
                    return location
        return -1

    if p == 1: return solveForwards(1)
    if p == 2: return solveBackwards(2)


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
