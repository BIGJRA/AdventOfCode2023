from aocd import get_data, post
from common import *


def solve(data, p):
    puzzles = data.split('\n\n')
    total = 0
    for puzzle in puzzles:
        lines = puzzle.splitlines()
        m, n = len(lines[0]), len(lines)
        hori_scores = []
        for y in range(n):
            score = 0
            for x in range(m):
                score = (score << 1) + (lines[y][x] == '#')
            hori_scores.append(score)
        vert_scores = []
        for x in range(m):
            score = 0
            for y in range(n):
                score = (score << 1) + (lines[y][x] == '#')
            vert_scores.append(score)
        ans = 0
        for score_set, mult in ((vert_scores, 1), (hori_scores, 100)):
            for split_after_idx in range(0, len(score_set) - 1):
                mirror_zips = list(zip(score_set[split_after_idx + 1:], score_set[split_after_idx::-1]))
                mismatches = [i for i in mirror_zips if i[0] != i[1]]
                if (p == 1 and len(mismatches) == 0) or \
                        (p == 2 and len(mismatches) == 1 and bin(mismatches[0][0] ^ mismatches[0][1]).count('1') == 1):
                    ans += (split_after_idx + 1) * mult
        total += ans
    return total


s1 = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''

tests = {
    s1: (405, 400)
}

test_assertions(tests, solve)

input_data = get_data(day=13, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=13, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=13, year=2023)
