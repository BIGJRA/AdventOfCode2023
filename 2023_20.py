from collections import defaultdict, deque

from aocd import get_data, post
from common import *


def solve(data, p):
    lines = data.splitlines()
    modules = {"button": 'broadcaster'}
    flips = {}
    conjs = {}
    for line in lines:
        name, dests = line.split(' -> ')
        if line[0] == '%':
            modules[name[1:]] = dests.split(', ')
            flips[name[1:]] = False
        elif line[0] == '&':
            modules[name[1:]] = dests.split(', ')
            conjs[name[1:]] = dict()
        else:
            modules[name] = dests.split(', ')
    for module in conjs:
        for other_module, dests in modules.items():
            if module in dests:
                conjs[module][other_module] = "lo"

    num_pulses = {"lo": 0, "hi": 0}
    if p == 1:
        for n in range(1000):
            q = deque([("broadcaster", "lo", "button")])  # current place, what it has received, prev module
            while q:
                module, pulse, prev = q.popleft()
                num_pulses[pulse] += 1
                if module not in modules:
                    continue
                elif module in flips and pulse == "hi":
                    continue
                elif module in flips:
                    if flips[module]:
                        nxt_pulse = "lo"
                    elif not flips[module]:
                        nxt_pulse = "hi"
                    flips[module] = not flips[module]
                elif module in conjs:
                    conjs[module][prev] = pulse
                    if all(conjs[module][inp] == "hi" for inp in conjs[module]):
                        nxt_pulse = "lo"
                    else:
                        nxt_pulse = "hi"
                elif module == "broadcaster":
                    nxt_pulse = pulse
                for adj in modules[module]:
                    q.append((adj, nxt_pulse, module))
        return num_pulses["lo"] * num_pulses["hi"]
    if p == 2:
        # Here I have to abuse the structure of the specific test data input given. It is a sequence of
        # four straight paths from broadcast to two subsequent conj modules that then each point to one last
        # conj module that points at rx. Each of the straight paths from broadcast to each conj module consists
        # of flipflops that point at only the next in the path, and sometimes the first conj module in its row.
        # This means once the conj module fires, it resets the entire path up to it to default, so it is fired
        # at a fixed period. Hence LCM works.........

        ans = 1
        for n in modules["broadcaster"]:
            bits = []
            curr = n
            while curr not in conjs:
                if len(modules[curr]) == 2: # we count the bits that also point at the & module
                    bits.append("1")
                    curr = list(filter(lambda x: x not in conjs, modules[curr]))[0]
                elif len(modules[curr]) == 1 and modules[curr][0] in conjs:
                    bits.append("1")
                    curr = modules[curr][0] # now the last node points at the &
                else: # we don't count bits that don't point at the & module
                    bits.append("0")
                    curr = modules[curr][0]
            score = int(''.join(bits)[::-1], 2)
            ans *= score
        return ans



    return 0

s1 = '''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a'''

s2 = '''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output'''

s3 = '''broadcaster -> a
%a -> inv, con
&inv -> b, res
%b -> con
&con -> res
&res -> rx'''

tests = {
    s1: (32000000, None),
    s2: (11687500, None),
}

test_assertions(tests, solve)

input_data = get_data(day=20, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=20, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=20, year=2023)
