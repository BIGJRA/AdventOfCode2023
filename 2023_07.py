from collections import Counter
from dataclasses import dataclass

from aocd import get_data

sample = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''

lines = get_data().splitlines()

# lines = sample.splitlines()

@dataclass
class Hand:
    bid: int
    cards: list
    jokers: bool
    score: int
    type: int

    def __init__(self, bid, cards, jokers=False):
        self.bid = bid
        self.cards = cards
        self.jokers = jokers
        self.assign_type(jokers)
        self.assign_score(jokers)

    def assign_type(self, jokers=False):
        # 5OAK - 7 ; 40AK - 6, FH - 5, 3OAK - 4, 2P - 3, 2OAK - 2, HC - 1
        c = Counter(self.cards)
        if jokers:
            num_jokers = c["J"]
            del c["J"]
            if num_jokers > 0:
                if num_jokers == 5: # A hand of five jokers is a 5OAK, but won't work with other logic
                    self.type = 7
                    return self.type
                c[c.most_common(1)[0][0]] += num_jokers #Greedy: we can always add all jokers to longest rank
        counts = list(map(lambda x: x[1], c.most_common(n=2))) # Only top 2 ranks are most important.
        if counts[0] == 5: self.type = 7
        elif counts[0] == 4: self.type = 6
        elif counts[0] == 3 and counts[1] == 2: self.type = 5
        elif counts[0] == 3: self.type = 4
        elif counts[0] == 2 and counts[1] == 2: self.type = 3
        elif counts[0] == 2: self.type = 2
        else: self.type = 1
        return self.type

    def assign_score(self, jokers=False):

        card_vals = {"2": "02", "3": "03", "4": "04", "5": "05", "6": "06", "7": "07",
                     "8": "08", "9": "09", "T": "10","Q": "12", "K": "13", "A": "14",
                     "J": "01" if jokers else "11"}
        # score favors hand type first, card #1 next, card #2 next, etc.
        self.score = ''.join([str(self.type)] + [card_vals[card] for card in self.cards])
        return self.score

def solve(p):
    hands = [Hand(int(line.split()[1]), line.split()[0], jokers=(p == 2)) for line in lines]
    hands.sort(key=lambda x: x.score)
    return sum(hand.bid * (pos + 1) for pos, hand in enumerate(hands))



p1 = solve(1)
print(p1)
# post.submit(p1)

p2 = solve(2)
print(p2)
# post.submit(p2)

