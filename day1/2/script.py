#SLOW (1 min runtime)

def input(filename):
    f = open(filename, "r", encoding="utf-8")
    lines = f.read().splitlines()
    return lines

def parse_to_int_list(str_list):
    int_list = []
    for item in str_list:
        integer = int(item)
        int_list.append(integer)
    return int_list

def find_first_duplicate_frequency(operations):
    INIT_VALUE = 0
    result = INIT_VALUE
    freq_list = [INIT_VALUE]
    dup_value = None
    while dup_value is None:
        for operation in operations:
            result += operation
            if result in freq_list:
                dup_value = result
                break
            else:
                freq_list.append(result)
    return dup_value

def output(filename, text):
    f = open(filename, "w")
    f.write(text)

def main():
    str_lines = input("input.txt")
    operations = parse_to_int_list(str_lines)
    first_duplicate = find_first_duplicate_frequency(operations)
    first_dup_str = str(first_duplicate)
    output("output.txt", first_dup_str)

main()
