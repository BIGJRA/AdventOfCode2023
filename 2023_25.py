import random
import re
from collections import defaultdict
from copy import deepcopy

from aocd import get_data, post
from common import *


# Motivation https://en.wikipedia.org/wiki/Karger%27s_algorithm

def solve(data, p):
    lines = data.splitlines()
    e = {}
    for line in lines:
        node, *adjs = re.findall(r'[a-z]+', line)
        e.update({tuple(sorted([node, a])): 1 for a in adjs})
    while True:
        curr = deepcopy(e)
        # print(curr)
        while len(curr) > 1:
            if min(curr.values()) > 3:
                break
            node1, node2 = random.choice(list(curr.keys()))
            # print(node1, node2)
            _edge_score = curr[(node1, node2)]
            new_node = node1 + node2
            counts = defaultdict(int)
            for edge in curr:
                if node1 in edge or node2 in edge:
                    try:
                        other = list(filter(lambda x: x not in (node1, node2), edge))[0]
                    except IndexError:
                        continue
                    counts[other] += curr[edge]
            # print(counts)
            curr.pop(tuple(sorted((node1, node2))))
            for n in (node1, node2):
                for c in counts:
                    try:
                        curr.pop(tuple(sorted((n, c))))
                    except KeyError:
                        continue
            for c in counts:
                curr[tuple((sorted((new_node, c))))] = counts[c]
        # print(curr)
        if list(curr.values())[0] != 3:
            continue
        counts = list(curr.keys())
        return len(counts[0][0]) // 3 * len(counts[0][1]) // 3


s1 = '''jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr'''

tests = {
    s1: (54, None)
}

test_assertions(tests, solve)

input_data = get_data(day=25, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=25, year=2023)

# p2 = solve(input_data, p=2)
# print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=25, year=2023)
