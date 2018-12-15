import sys

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
    
def find_max_total_power_area(area):
    max_area_value = -sys.maxsize -1
    max_area = None
    area_size = [len(area), len(area[0])]
    for y in range(1, area_size[0] - 1):
        for x in range(1, area_size[1] - 1):
            neighbor_cells = find_neighbor_cells(x, y)
            area_value = 0
            for line in neighbor_cells:
                for cell in line:
                    area_value += area[cell[0]][cell[1]]
            if max_area_value < area_value:
                max_area = neighbor_cells
                max_area_value = area_value
    return max_area

def find_neighbor_cells(x, y):
    neighbor_cells = []
    for y_off in range(-1, 2):
        line = []
        for x_off in range(-1, 2):
            line.append([y + y_off, x + x_off])
        neighbor_cells.append(line)
    return neighbor_cells

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

def output(filename, text):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(text)

def main():
    AREA_SIZE = [300, 300]
    lines = input("input.txt")
    serial_no = get_serial_no(lines)
    area = fill_area(AREA_SIZE, serial_no)
    max_area = find_max_total_power_area(area)
    (y, x) = max_area[0][0]
    output("output.txt", str((x, y)))

main()