import re

from aocd import get_data, post

from common import *

import numpy as np


def solve(data, p):
    lines = data.splitlines()
    hailstones = []
    bounds = [200000000000000, 400000000000000]
    if lines[0] == '19, 13, 30 @ -2,  1, -2':
        bounds = [7, 27]  # for test input
    for line in lines:
        x0, y0, z0, dx, dy, dz = map(int, re.findall(r'-*\d+', line))
        hailstones.append((x0, y0, z0, dx, dy, dz))
    total = 0
    if p == 1:
        for pos, stone1 in enumerate(hailstones):
            x1, y1, z1, dx1, dy1, dz1 = stone1
            for stone2 in hailstones[pos + 1:]:
                x2, y2, z2, dx2, dy2, dz2 = stone2
                # print(f"Hailstone A: {x1}, {y1}, {z1} @ {dx1}, {dy1}, {dz1}")
                # print(f"Hailstone B: {x2}, {y2}, {z2} @ {dx2}, {dy2}, {dz2}")
                A = [[1, 0, -dx1, 0], [1, 0, 0, -dx2], [0, 1, -dy1, 0], [0, 1, 0, -dy2]]
                B = [[x1], [x2], [y1], [y2]]
                if np.linalg.det(A) == 0:
                    # print("Hailstones' paths are parallel; they never intersect.\n")
                    # Test input seems to not have any cases of collinearity - if it did, part 2 would be impossible
                    # unless the hailstones occupied the exact same space, which contradicts reality lol
                    continue
                ((int_x), (int_y), (t1), (t2)) = np.linalg.solve(A, B)
                if t1 < 0 and t2 < 0:
                    # print("Hailstones' paths crossed in the past for both hailstones.\n")
                    continue
                if t1 < 0:
                    # print("Hailstones' paths crossed in the past for hailstone A.\n")
                    continue
                if t2 < 0:
                    # print("Hailstones' paths crossed in the past for hailstone B.\n")
                    continue
                if bounds[0] <= int_x <= bounds[1] and bounds[0] <= int_y <= bounds[1]:
                    # print(f"Hailstones' paths will cross inside the test area (at x={int_x}, y={int_y}).\n")
                    total += 1
                else:
                    # print(f"Hailstones' paths will cross outside the test area (at x={int_x}, y={int_y}).\n")
                    continue

    if p == 2:
        # reassign origin to be hailstone, so position xn, yn, zn, and relative velocity to dxn, dyn, dzn
        # x - xn = t(dx - dxn), y - yn = t(dy - dyn) => (x - xn)(dy - dyn) = (y - yn)(dx - dxn)
        # => for any two hailstones h1, h2;
        # xn(dy2 - dy1) + yn(dx1 - dx2) + dxn(y1 - y2) + dyn(x2 -  x1) = x1dy1 - x2dy2 - y1dx1 + y2dx2
        x1, y1, z1, dx1, dy1, dz1 = hailstones[0]
        coeffs = []
        for (x2, y2, z2, dx2, dy2, dz2) in hailstones[1:5]:
            # use four combinations of hailstones to get 4 equations to solve for these four unknowns
            coeffs.append([dy2 - dy1, dx1 - dx2, y1 - y2, x2 - x1, (x2 * dy2) - (x1 * dy1) + (y1 * dx1) - (y2 * dx2)])
        A = np.array([c[:4] for c in coeffs])
        B = np.array([c[4] for c in coeffs])
        xn, yn, dxn, dyn = np.linalg.solve(A, B).flat
        x2, y2, z2, dx2, dy2, dz2 = hailstones[1]
        # Solve for zn and dzn now
        t1 = (xn - x1) / (dx1 - dxn)
        t2 = (xn - x2) / (dx2 - dxn)
        # Get times from x coordinate movement, use them to solve for zn and dzn
        A = np.array([[1, -t1], [1, -t2]])
        B = np.array([dz1 * t1 + z1, dz2 * t2 + z2])
        zn, dzn = np.linalg.solve(A, B).flat
        total += xn + yn + zn
    return int(total)
    # Total was off by 0.2 estimated, using int works for sample input but may need to be
    # made more precise with better typing throughout the process.


s1 = '''19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3'''

tests = {
    s1: (2, 47)
}

test_assertions(tests, solve)

input_data = get_data(day=24, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
#post.submit(p1, part=1, day=24, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=24, year=2023)
