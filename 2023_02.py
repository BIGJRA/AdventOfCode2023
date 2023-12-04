from aocd import get_data, post

lines = get_data().splitlines()

def solve(p):
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

p1 = solve(1)
print(p1)
# post.submit(p1)

p2 = solve(2)
print(p2)
# post.submit(p2)

