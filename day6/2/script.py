#Quite slow

def input(filename):
    with open(filename, "r", encoding="utf-8") as f_in:
        lines = f_in.read().splitlines()
        return lines

def str_to_coordinates(coordinates_str):
    coordinates = []
    for coordinate_line in coordinates_str:
        coordinate_list = coordinate_line.split(", ")
        coordinate = Coordinate(int(coordinate_list[0]), int(coordinate_list[1]))
        coordinates.append(coordinate)
    return coordinates

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({},{})".format(self.x, self.y)
    
    def __str__(self):
        return "({},{})".format(self.x, self.y)

def find_distances(coordinates):
    coords_total_distance = {}
    for coord in coordinates:
        coords_total_distance[coord] = find_total_distance(coord.x, coord.y, coordinates)
    return coords_total_distance

def find_total_distance(x, y, coords):
    total_distance = 0
    for coord in coords:
        total_distance += distance_to_coordinate(x, y, coord)
    return total_distance

def distance_to_coordinate(x, y, coordinate):
    return abs(coordinate.x - x) + abs(coordinate.y - y)

def find_min_total_distance(coords_dist, coords):
    min_dist = coords_dist[coords[0]]
    min_coord = None
    for coord in coords:
        if min_dist > coords_dist[coord]:
            min_dist = coords_dist[coord]
            min_coord = coord
    return (min_coord, min_dist)

def find_max_area(areas_dict):
    max = 0
    for key, value in areas_dict.items():
        if max < value:
            max = value
    return max

def find_area_dict(x, y, coords, area_size):
    coords_dict = {}
    stack = [(x, y)]
    depth_first_search(stack, coords, area_size, coords_dict)
    print(x, y, coords_dict[(x, y)])
    return coords_dict

def depth_first_search(stack, coords, area_size, coords_dict):
    while stack != []:
        (x, y) = stack[-1]
        total_distance = find_total_distance(x, y, coords)
        coords_dict[stack[-1]] = total_distance
        if total_distance < area_size:
            moves_list = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            back = True
            for move in moves_list:
                new_x = x + move[0]
                new_y = y + move[1]
                if (new_x, new_y) not in coords_dict:
                    stack.append((new_x, new_y))
                    back = False
                    break
            if back:
                stack.pop()
        else:
            stack.pop()

def find_area_size(area_dict, max_dist):
    count = 0
    for key, value in area_dict.items():
        if value < max_dist:
            count += 1
    return count

def output(filename, text):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(text)

def main():
    MAX_AREA_DIST = 10000
    coords_str = input("input.txt")
    coords = str_to_coordinates(coords_str)
    coords_dist = find_distances(coords)
    (min_coord, min_coord_dist) = find_min_total_distance(coords_dist, coords)
    area_dict = find_area_dict(min_coord.x, min_coord.y, coords, MAX_AREA_DIST)
    area_size = find_area_size(area_dict, MAX_AREA_DIST)
    output("output.txt", str(area_size))

main()