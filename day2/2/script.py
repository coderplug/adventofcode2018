def input(filename):
    f = open(filename, "r", encoding="utf-8")
    lines = f.read().splitlines()
    return lines

def find_correct_box_ids(box_ids):
    box_count = len(box_ids)
    for i in range(box_count - 1):
        box1 = box_ids[i]
        for j in range(i + 1, box_count):
            box2 = box_ids[j]
            if are_correct_box_ids(box1, box2):
                return (box1, box2)
    return None

def are_correct_box_ids(box1, box2):
    diff_character_count = 0
    box_id_len = len(box1)
    for i in range(box_id_len):
        if box1[i] != box2[i]:
            diff_character_count += 1
    if diff_character_count != 1:
        return False
    return True

def find_common_letters(box1, box2):
    common_characters = []
    box_id_len = len(box1)
    for i in range(box_id_len):
        if box1[i] == box2[i]:
            common_characters.append(box1[i])
    return common_characters

def output(filename, text):
    f = open(filename, "w")
    f.write(text)

def main():
    lines = input("input.txt")
    (box1, box2) = find_correct_box_ids(lines)
    common_letters = find_common_letters(box1, box2)
    common_letters_str = ''.join(common_letters)
    print(box1, box2, common_letters_str)
    output("output.txt", common_letters_str)

main() 