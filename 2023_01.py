from aocd import get_data, post

lines = get_data().splitlines()

def solve(p):

    strings = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,"8": 8,"9": 9}
    if p == 2:
        strings |= {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

    total = 0
    for line in lines:
        n = 0
        l = r = 0

        # Loop from the left. Look for the first allowed number
        while True:
            for s in strings:
                try: # try-except just ensures we can get thru without a string being longer than the window
                    if line[l:l+len(s)] == s:
                        # First from the left is the first of two digits - mult by 10
                        n += 10 * strings[s]
                        break
                except IndexError:
                    pass
            if n > 0: # quits the loop once a number has been found. Note never 0 inputs
                break
            else:
                l += 1

        # Loop from the right. Look for the first allowed number
        while True:
            for s in strings:
                try:
                    # From the right the word numbers will be backwards
                    if line[::-1][r:r+len(s)] == s[::-1]:
                        n += strings[s] # from the right, assigns to rightmost digit
                        break
                except IndexError:
                    pass
            if (n % 10) > 0: # quits the loop once the one digit has been found
                break
            else:
                r += 1
        total += n
    return total

p1 = solve(1)
print(p1)
#post.submit(p1)

p2 = solve(2)
print(p2)
# post.submit(p2)

