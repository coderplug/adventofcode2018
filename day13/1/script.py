from collections import deque

def input(filename):
    with open(filename, "r", encoding="utf-8") as f_in:
        return f_in.read().splitlines()

def parse_input(lines):
    rows, cols = get_input_dims(lines)
    map_list = [[" "] * cols for _ in range(rows)]
    carts = []
    for y in range(rows):
        for x in range(cols):
            cell = lines[y][x]
            if is_cart(cell):
                map_list[y][x] = get_under_cart_value(lines, x, y)
                cart = Cart((x, y), cell)
                carts.append(cart)
            else:
                map_list[y][x] = cell
    return map_list, carts

def get_input_dims(lines):
    rows = len(lines)
    cols = len(lines[0])
    return rows, cols

def is_cart(cell):
    if cell in ["^", "v", ">", "<"]:
        return True
    return False

def get_under_cart_value(lines, x, y):
    cart_track_dir = {
        "^":"|", 
        "v":"|", 
        ">":"-", 
        "<":"-"
    }
    if is_under_intersection(lines, x, y):
        return "+"
    elif is_under_slash_corner(lines, x, y):
        return "/"
    elif is_under_backslash_corner(lines, x, y):
        return "\\"
    return cart_track_dir[lines[y][x]]

def is_under_intersection(lines, x, y):
    hor_values = ["+", "-", "/", "\\"]
    vert_values = ["+", "|", "/", "\\"]

    if is_border_cell(lines, x, y):
        return False
    cell_up = lines[y-1][x]
    cell_down = lines[y+1][x]
    cell_right = lines[y][x+1]
    cell_left = lines[y][x-1]
    if cell_up in vert_values and cell_down in vert_values and cell_right in hor_values and cell_left in hor_values:
        return True
    return False  

def is_border_cell(lines, x, y):
    rows, cols = get_input_dims(lines)
    if x < 0 or x == (cols - 1) or y < 0 or y == (rows - 1):
        return False
    return True

def is_under_slash_corner(lines, x, y):
    hor_values = ["+", "-", "/", "\\"]
    vert_values = ["+", "|", "/", "\\"]
    cell_up = lines[y-1][x]
    cell_down = lines[y+1][x]
    cell_right = lines[y][x+1]
    cell_left = lines[y][x-1]
    cell = lines[y][x]
    if cell == "^":
        if cell_left in hor_values and cell_up in vert_values:
            return True
        return False
    elif cell == "v":
        if cell_right in hor_values and cell_down in vert_values:
            return True
        return False
    elif cell == ">":
        if cell_right in hor_values and cell_down in vert_values:
            return True
        return False
    else:
        if cell_left in hor_values and cell_up in vert_values:
            return True
        return False
    return False

def is_under_backslash_corner(lines, x, y):
    hor_values = ["+", "-", "/", "\\"]
    vert_values = ["+", "|", "/", "\\"]
    cell_up = lines[y-1][x]
    cell_down = lines[y+1][x]
    cell_right = lines[y][x+1]
    cell_left = lines[y][x-1]
    cell = lines[y][x]
    if cell == "^":
        if cell_right in hor_values and cell_up in vert_values:
            return True
        return False
    elif cell == "v":
        if cell_left in hor_values and cell_down in vert_values:
            return True
        return False
    elif cell == ">":
        if cell_right in hor_values and cell_up in vert_values:
            return True
        return False
    else:
        if cell_left in hor_values and cell_down in vert_values:
            return True
        return False
    return False

class Cart:
    def __init__(self, pos, value):
        self.pos = pos
        self.value = value
        self.next_move = deque(["left", "straight", "right"])

    def __repr__(self):
        (x, y) = self.pos
        return "Cart with pos ({},{}) with value {}".format(x, y, self.value)

    def __str__(self):
        (x, y) = self.pos
        return "Cart with pos ({},{}) with value {}".format(x, y, self.value)

def tick_loop(map_list, carts):
    while True:
        sort_carts_by_pos(carts)
        for idx, cart in enumerate(carts):
            move_cart(cart)
            check_if_change_direction(cart, map_list)
            if is_crash(idx, carts):
                return cart.pos

def sort_carts_by_pos(carts):
    # Bubble sort
    changed = True
    last_index = len(carts) - 1
    while changed:
        changed = False
        for index in range(last_index):
            curr_cart = carts[index]
            next_cart = carts[index+1]
            if is_fst_pos_bigger(curr_cart, next_cart):
                swap(carts[index], carts[index+1])
                changed = True
        last_index -= 1

def is_fst_pos_bigger(curr_cart, next_cart):
    (curr_x, curr_y) = curr_cart.pos
    (next_x, next_y) = next_cart.pos
    return (curr_y, curr_x) > (next_y, next_x)

def swap(t1, t2):
    t2, t1 = t1, t2

def move_cart(cart):
    move_dir = {
        "^": (0, -1),
        "v": (0, 1),
        ">": (1, 0),
        "<": (-1, 0)
    }
    (move_x, move_y) = move_dir[cart.value]
    (x, y) = cart.pos
    new_pos = (x + move_x, y + move_y)
    cart.pos = new_pos

def check_if_change_direction(cart, map_list):
    (x, y) = cart.pos
    if is_corner(x, y, map_list):
        change_dir_corner(cart, map_list)
    elif is_intersection(x, y, map_list):
        change_dir_intersection(cart)

def is_corner(x, y, map_list):
    if map_list[y][x] in ["\\", "/"]:
        return True
    return False

def change_dir_corner(cart, map_list):
    rotation_dir = {
        ("^", "\\") : "<",
        ("^", "/") : ">",
        ("v", "\\") : ">",
        ("v", "/") : "<",
        (">", "\\") : "v",
        (">", "/") : "^",
        ("<", "\\") : "^",
        ("<", "/") : "v"
    }
    (x, y) = cart.pos
    pos_value = map_list[y][x]
    cart.value = rotation_dir[(cart.value, pos_value)]

def is_intersection(x, y, map_list):
    if map_list[y][x] == "+":
        return True
    return False

def change_dir_intersection(cart):
    rotation_dir = {
        ("^", "left") : "<",
        ("^", "straight") : "^",
        ("^", "right") : ">",
        ("v", "left") : ">",
        ("v", "straight") : "v",
        ("v", "right") : "<",
        (">", "left") : "^",
        (">", "straight") : ">",
        (">", "right") : "v",
        ("<", "left") : "v",
        ("<", "straight") : "<",
        ("<", "right") : "^"
    }
    cart.value = rotation_dir[cart.value, cart.next_move[0]]
    cart.next_move.rotate(-1)

def is_crash(check_index, carts):
    check_cart = carts[check_index]
    for index, cart in enumerate(carts):
        if check_cart.pos == cart.pos and check_index != index:
            return True
    return False

def output(filename, text):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(text)

def main():
    lines = input("input.txt")
    map_list, carts = parse_input(lines)
    pos = tick_loop(map_list, carts)
    output("output.txt", str(pos))

main()