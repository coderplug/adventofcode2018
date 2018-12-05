def input(filename):
    with open(filename, "r", encoding="utf-8") as f_in:
        line = f_in.read().replace('\n', '')
        return line

def polymer_reaction(polymer):
    new_polymer = polymer[:]
    temp = []
    index = 0
    while (index + 2) != len(new_polymer):
        if are_reactive(new_polymer[index], new_polymer[index+1]):
            new_polymer = new_polymer[:index] + new_polymer[index+2:]
            index = index - 1 if index != 0 else 0
        else:
            index += 1
    return new_polymer

#Slower alternative
""" def polymer_reaction(polymer):
    new_polymer = polymer[:]
    old_polymer = []
    while old_polymer != new_polymer:
        indexes = []
        old_polymer = new_polymer
        for index in range(len(old_polymer) - 1):
            if are_reactive(old_polymer[index], old_polymer[index+1]):
                new_polymer = old_polymer[:index] + old_polymer[index+2:]
                break
    return new_polymer """

def are_reactive(unit_1, unit_2):
    if unit_1.swapcase() == unit_2:
        return True
    return False

def get_discrete_polymer_units(polymer):
    discrete_units = set()
    for unit in polymer.lower():
        discrete_units.add(unit)
    return discrete_units

def find_smallest_modified_polymer(polymer, letters):
    min_length = len(polymer)
    min_length_polymer = polymer
    for letter in letters:
        modified_polymer = remove_letter(letter, polymer)
        final_modified_polymer = polymer_reaction(modified_polymer)
        final_modified_polymer_length = len(final_modified_polymer)
        if min_length > final_modified_polymer_length:
            min_length = final_modified_polymer_length
            min_length_polymer = final_modified_polymer
    return (min_length, min_length_polymer)

def remove_letter(letter, polymer):
    modified_polymer = polymer.replace(letter, "")
    final_modified_polymer = modified_polymer.replace(letter.upper(), "")
    return final_modified_polymer
    

def output(filename, text):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(text)

def main():
    polymer = input("input.txt")
    unmodified_final_polymer = polymer_reaction(polymer)
    letters = get_discrete_polymer_units(unmodified_final_polymer)
    (min_polymer_length, min_polymer) = find_smallest_modified_polymer(unmodified_final_polymer, letters)
    polymer_length_str = str(min_polymer_length)
    output("output.txt", polymer_length_str)

main()