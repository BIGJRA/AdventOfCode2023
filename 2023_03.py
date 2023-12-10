from dataclasses import dataclass
from functools import lru_cache

from common import *
from aocd import get_data, post


def solve(data, p):
    lines = data.splitlines()

    @dataclass
    class Number:
        text: str
        row: int
        col: int
        active: bool

        def __key(self):
            return self.row, self.col

        def __hash__(self):
            return hash(self.__key())

        def addChar(self, char):
            self.text += char

        def getAdj(self):
            ans = [(self.row, self.col - 1), (self.row, self.col + len(self.text))]
            for j in range(self.col - 1, self.col + len(self.text) + 1):
                ans.append((self.row - 1, j))
                ans.append((self.row + 1, j))
            return ans

    @dataclass
    class Symbol:
        text: str
        row: int
        col: int
        adjacent_nums: list

        def __key(self):
            return self.row, self.col

        def __hash__(self):
            return hash(self.__key())

    @lru_cache
    def issymbol(s: str) -> bool:
        return not s.isdigit() and not s == "."

    symbols = set([])
    nums = set([])
    is_number = False
    n = None
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if not is_number:
                if char.isdigit():
                    is_number = True
                    n = Number(text=char, row=i, col=j, active=False)
            else:
                if char.isdigit():
                    n.addChar(char)
                else:
                    nums.add(n)
                    is_number = False
            if issymbol(char):
                symbols.add(Symbol(text=char, row=i, col=j, adjacent_nums=list()))
        if is_number:
            nums.add(n)

    for s in symbols:
        for n in nums:
            if (s.row, s.col) in n.getAdj():
                n.active = True
                s.adjacent_nums.append(int(n.text))

    total = 0
    if p == 1:
        for n in nums:
            if n.active:
                total += int(n.text)
    elif p == 2:
        for s in symbols:
            if s.text == "*" and len(s.adjacent_nums) == 2:
                total += s.adjacent_nums[0] * s.adjacent_nums[1]
    return total


s1 = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''

tests = {
    s1: (4361, 467835)
}

test_assertions(tests, solve)

input_data = get_data(day=3, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=3, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=3, year=2023)
