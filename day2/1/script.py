def input(filename):
    f = open(filename, "r", encoding="utf-8")
    lines = f.read().splitlines()
    return lines

def get_checksum(words):
    two_letter_count = 0
    three_letter_count = 0
    for word in words:
        dict = count_letters(word)
        two_letter_count = two_letter_count + 1 if is_dup_letters(dict, 2) else two_letter_count
        three_letter_count = three_letter_count + 1 if is_dup_letters(dict, 3) else three_letter_count
    result = checksum(two_letter_count, three_letter_count)
    return result

def count_letters(word):
    letter_dict = {}
    for letter in word:
        letter_dict[letter] = (letter_dict[letter] + 1) if letter in letter_dict else 1
    return letter_dict

def is_dup_letters(dict, count):
    for key, value in dict.items():
        if value == count:
            return True
    return False

def checksum(two_count, three_count):
    return two_count * three_count

def output(filename, text):
    f = open(filename, "w")
    f.write(text)

def main():
    lines = input("input.txt")
    checksum = get_checksum(lines)
    checksum_str = str(checksum)
    output("output.txt", checksum_str)

main()