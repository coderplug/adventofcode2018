def input(filename):
    with open(filename, "r", encoding="utf-8") as f_in:
        lines = f_in.read().splitlines()
        return lines

def parse_to_int_list(str_list):
    int_list = []
    for item in str_list:
        integer = int(item)
        int_list.append(integer)
    return int_list

def sum_of_operations(int_list):
    INIT_VALUE = 0
    result = INIT_VALUE
    for value in int_list:
        result += value
    return result

def output(filename, text):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(text)

def main():
    operations = input("input.txt")
    int_list = parse_to_int_list(operations)
    sum = sum_of_operations(int_list)
    str_sum = str(sum)
    output("output.txt", str_sum)

main()