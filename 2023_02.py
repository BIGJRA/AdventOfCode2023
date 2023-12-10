from common import *
from aocd import get_data, post

def solve(data, p):
    lines = data.splitlines()
    results = [0,0]
    games = []
    for line in lines:
        game = {"id": int(line.split(': ')[0].split(' ')[1]), "pulls": []}
        for pull in line.split(': ')[1].split('; '):
            sets = {}
            for s in pull.split(', '):
                count, color = s.split(' ')
                count = int(count)
                sets[color] = count
            game["pulls"].append(sets)
        games.append(game)

    totals = {"red": 12, "green": 13, "blue": 14}
    for game in games:
        maxes = {"blue": 0, "green": 0, "red": 0}
        passed = True
        for pull in game["pulls"]:
            for color, count in pull.items():
                maxes[color] = max(maxes[color], count)
        if all([totals[color] >= maxes[color] for color in totals]):
            results[0] += game["id"]
        results[1] += maxes["blue"] * maxes["green"] * maxes["red"]
    return results[p-1]

s1 = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''

tests = {
    s1: (8, 2286)
}

test_assertions(tests, solve)

input_data = get_data(day=2, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
#post.submit(p1, part=1, day=2, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
#post.submit(p2, part=2, day=2, year=2023)
