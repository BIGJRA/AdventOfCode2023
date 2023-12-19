import re
from collections import deque
from dataclasses import dataclass

from aocd import get_data, post
from common import *


def solve(data, p):
    @dataclass
    class Workflow:
        name: str
        conditions: list
        previous: list

        def add_condition(self, var, compare_func, number, result):
            def invert(o, n):
                assert o in ["<", ">"]
                return (">", (n - 1)) if o == "<" else ("<", (n + 1))

            list_of_rules = []
            if self.conditions:
                prev, _ = self.conditions[-1]
                modified_last = prev[-1][0], *invert(prev[-1][1], prev[-1][2])
                list_of_rules = prev[:-1] + [modified_last]
            if compare_func is not None:
                list_of_rules.append((var, compare_func, number,))
            self.conditions.append((list_of_rules, result))

    lines = data.splitlines()
    workflows = {}
    items = []
    for line in lines:
        if line == '': continue
        if line[0] != '{':
            name, chunk = line[:-1].split('{')
            w = Workflow(name, list(), list())
            for case in chunk.split(','):
                if '<' not in case and '>' not in case:  # default case
                    w.add_condition(None, None, None, case)
                else:
                    var, n, res = re.split(r'<|>|:', case)
                    w.add_condition(var, '<' if '<' in case else '>', int(n), res)
            workflows[name] = w
        else:
            items.append(dict(zip('xmas', map(int, re.findall(r'\d+', line)))))

    workflows['A'] = Workflow('A', list(), list())
    workflows['R'] = Workflow('R', list(), list())

    for w_name, w in workflows.items():
        for c in w.conditions:
            workflows[c[1]].previous.append((w_name, c[0]))
            # Here we store all the ways to get to each node

    q = deque([("A", list())])
    answers = ['_', 0, 0]
    while q:
        location, conds = q.popleft()
        for neighbor, neighboring_conds in workflows[location].previous:
            q.append((neighbor, conds + neighboring_conds))
        if location == 'in':
            # Each time we enter here, we have completed a path back from A to in.
            # We have a list of conditions that need to have been met along the way
            mult = 1
            extrema = {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]}
            for letter, expr, number in conds:
                if expr == '>':
                    extrema[letter][0] = max(extrema[letter][0], number + 1)
                elif expr == '<':
                    extrema[letter][1] = min(extrema[letter][1], number - 1)

            new_items = []
            for item in items:
                if all(extrema[l][0] <= item[l] <= extrema[l][1] for l in extrema):
                    answers[1] += sum(item.values())
                else:
                    new_items.append(item)
            items = new_items

            for letter, (m, M) in extrema.items():
                mult *= (M - m + 1)
            answers[2] += mult

    return answers[p]


s1 = '''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}'''

tests = {
    s1: (19114, 167409079868000)
}

test_assertions(tests, solve)

input_data = get_data(day=19, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=19, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=19, year=2023)
