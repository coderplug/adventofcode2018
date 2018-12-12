import collections

def input(filename):
    with open(filename, "r", encoding="utf-8") as f_in:
        return f_in.read().splitlines()

def parse_text(line):
    words = line.split(' ')
    player_count = int(words[0])
    last_marble_worth = int(words[6])
    return (player_count, last_marble_worth)

def find_high_score(players, last_marble_worth):
    last_marble_worth *= 100
    marble_deque = collections.deque()
    player = 1
    player_scores = [0] * players
    for marble in range(0, last_marble_worth):
        if marble % 23 != 0 or marble == 0:
            marble_deque.rotate(-2)
            marble_deque.appendleft(marble)
        else:
            marble_deque.rotate(7)
            removable_marble = marble_deque.popleft()
            score = marble + removable_marble
            player_scores[player - 1] += score
        player = player + 1 if players > player else 1
    return max(player_scores)

def output(filename, text):
    with open(filename, "w", encoding="utf-8") as f_out:
        return f_out.write(text)

def main():
    lines = input("input.txt")
    line = lines[0]
    (players, last_marble_worth) = parse_text(line)
    high_score = find_high_score(players, last_marble_worth)
    output("output.txt", str(high_score))

main()