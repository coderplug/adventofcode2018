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

def output(filename, text):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(text)

def main():
    polymer = input("input.txt")
    final_polymer = polymer_reaction(polymer)
    polymer_length = str(len(final_polymer))
    output("output.txt", polymer_length)

main()