from collections import defaultdict
from dataclasses import dataclass

from common import *
from aocd import get_data, post

def solve(data, p):
    @dataclass
    class Card:
        winners: set
        chosen: list
        index: int

        def scoreCard(self):
            score = 0
            matches = 0
            for pick in self.chosen:
                if pick in self.winners:
                    matches += 1
                    if score == 0:
                        score = 1
                    else:
                        score *= 2
            return score, matches

    lines = data.splitlines()
    cards = []
    count = defaultdict(int)
    for pos, line in enumerate(lines):
        index = pos + 1
        winners = line.split(': ')[1].split(' |')[0].split()
        chosen = line.split(': ')[1].split(' |')[1].split()
        cards.append(Card(winners=set(winners), chosen=chosen, index=index))
        count[pos + 1] += 1

    total_points = 0
    total_num_cards = 0

    for card in cards:
        score, matches = card.scoreCard()
        total_points += score

        # In order to count cards being played, no cards are added above so we can iterate and add as we go.
        total_num_cards += count[card.index]
        # Adds multiplicative number of cards to the next stacks
        for new_index in range(card.index + 1, card.index + matches + 1):
            count[new_index] += count[card.index]

    if p == 1:
        return total_points
    elif p == 2:
        return total_num_cards


s1 = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''

tests = {
    s1: (13, 30)
}

test_assertions(tests, solve)

input_data = get_data(day=4, year=2023)

p1 = solve(input_data, p=1)
print(f"Part 1: {p1}")
# post.submit(p1, part=1, day=4, year=2023)

p2 = solve(input_data, p=2)
print(f"Part 2: {p2}")
# post.submit(p2, part=2, day=4, year=2023)
