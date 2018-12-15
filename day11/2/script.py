import sys, time, datetime

def input(filename):
    with open(filename, "r", encoding="utf-8") as f_in:
        return f_in.read().splitlines()

def get_serial_no(lines):
    return int(lines[0])

def fill_area(size, serial_no):
    area = [[0] * size[0] for _ in range(size[1])]
    for y in range(size[1]):
        for x in range(size[0]):
            area[y][x] = cell_power_level((x, y), serial_no)
    return area

def summed_area_table(area_values, sum_table, x, y):
    i_coord = area_values[y][x]
    north_sum = west_sum = north_east_sum = 0
    if sum_table[y][x] is not None:
        return sum_table[y][x]
    else:
        if y != 0:
            north_sum = summed_area_table(area_values, sum_table, x, y-1)
        if x != 0:
            west_sum = summed_area_table(area_values, sum_table, x-1, y)
        if x != 0 and y != 0:
            north_east_sum = summed_area_table(area_values, sum_table, x-1, y-1)
        sum_table[y][x] = (i_coord + north_sum + west_sum - north_east_sum)
    return sum_table[y][x]

def fill_summed_area_table(area):
    size = [len(area), len(area[0])]
    (x_size, y_size) = size
    sum_table = [[None] * x_size for _ in range(y_size)]
    for y in range(y_size):
        for x in range(x_size):
            summed_area_table(area, sum_table, x, y)
    return sum_table

def find_max_total_power_area(area, summed_table):
    max_area_value = -sys.maxsize -1
    max_area = None
    max_area_size = 0
    area_size = [len(area), len(area[0])]
    for y in range(area_size[0]):
        for x in range(area_size[1]):
            max_size = find_max_area(x, y, area_size)
            area_value = 0
            for size in range(1, max_size):
                area_value = find_area_value(x, y, size, area, summed_table)
                if max_area_value < area_value:
                    max_area_value = area_value
                    max_area = (y, x)
                    max_area_size = size
    return (max_area, max_area_value, max_area_size)

def find_area_value(x, y, size, area, sum_table):
    #A   B
    # |'''|
    #C|  D|
    # '''''
    a = b = c = d = 0
    
    if x != 0 and y != 0:
        a = sum_table[y-1][x-1]
    if y != 0:
        b = sum_table[y-1][x+size-1]
    if x != 0:
        c = sum_table[y+size-1][x-1] 
    d = sum_table[y+size-1][x+size-1]
    area_sum = d - c - b + a
    return area_sum

def find_max_area(x, y, size):
    max_area = min([size[0] - x, size[1] - y])
    return max_area

def cell_power_level(coordinate, serial_no):
    (x, y) = coordinate
    rack_id = find_rack_id(x)
    start_power_level = find_starting_power_level(rack_id, y)
    final_power_level = find_final_power_level(rack_id, start_power_level, serial_no)
    return final_power_level

def find_rack_id(x):
    return x + 10

def find_starting_power_level(rack_id, y):
    return rack_id * y

def find_final_power_level(rack_id, start_power_level, serial_no):
    power_level = start_power_level + serial_no
    power_level *= rack_id
    hundreds_digit = (power_level // 100) % 10
    final_power_level = int(hundreds_digit) - 5
    return final_power_level

def output_area(filename, area):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.writelines([(str(line) + "\n") for line in area])

def output(filename, text):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(text)

def main():
    AREA_SIZE = [300, 300]
    lines = input("input.txt")
    serial_no = get_serial_no(lines)
    area = fill_area(AREA_SIZE, serial_no)
    summed_table = fill_summed_area_table(area)
    (start_coord, value, size) = find_max_total_power_area(area, summed_table)
    
    (y, x) = start_coord
    print(x, y)
    print(value)
    print(size)
    output("output.txt", str(start_coord))

main()