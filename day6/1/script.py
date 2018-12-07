#Might be wrong solution with different input

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
        return "{},{}".format(self.x, self.y)
    
    def __str__(self):
        return "{},{}".format(self.x, self.y)

def get_limits(coordinates):
    min_x = coordinates[0].x
    min_y = coordinates[0].y
    max_x = coordinates[0].x
    max_y = coordinates[0].y

    for coordinate in coordinates:
        if min_x > coordinate.x:
            min_x = coordinate.x
        if min_y > coordinate.y:
            min_y = coordinate.y
        if max_x < coordinate.x:
            max_x = coordinate.x
        if max_y < coordinate.y:
            max_y = coordinate.y
    return (min_x, min_y, max_x, max_y)

def paint_map(min_x, min_y, max_x, max_y, coordinates):
    map_list = [["x"] * (max_y + 1) for i in range(max_x + 1)]
    for coordinate in coordinates:
        map_list[coordinate.x][coordinate.y] = "*"
    string_list = []
    for line in map_list:
        string_list.append(''.join(line))
    map_string = '\n'.join(string_list)
    return map_string

def fill_map(min_x, min_y, max_x, max_y, coordinates):
    map_list = [[0] * (max_y + 1) for i in range(max_x + 1)]
    for coordinate in coordinates:
        map_list[coordinate.x][coordinate.y] = coordinate
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            nearest_coordinate = coordinates[0]
            length_count = 1
            length = distance_to_coordinate(x, y, coordinates[0])
            for index in range(1, len(coordinates)):
                distance = distance_to_coordinate(x, y, coordinates[index])
                if distance == length:
                    length_count += 1
                elif distance < length:
                    nearest_coordinate = coordinates[index]
                    length_count = 1
                    length = distance
            if length_count > 1:
                map_list[x][y] = 0
            else:
                map_list[x][y] = nearest_coordinate
    return map_list   

def distance_to_coordinate(x, y, coordinate):
    return abs(coordinate.x - x) + abs(coordinate.y - y)

def fill_coord_area_dict(min_x, min_y, max_x, max_y, coord_map):
    coord_area_dict = {}
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            coordinate = coord_map[x][y]
            if coordinate in coord_area_dict:
                coord_area_dict[coordinate] += 1
            else:
                coord_area_dict[coordinate] = 1
    return coord_area_dict

def remove_infinite_areas(min_x, min_y, max_x, max_y, coord_map, coord_area_dict):
    infinite_areas = set()
    for x in range(min_x, max_x + 1):
        infinite_areas.add(coord_map[x][min_y])
        infinite_areas.add(coord_map[x][max_y])
    for y in range(min_y, max_y + 1):
        infinite_areas.add(coord_map[min_x][y])
        infinite_areas.add(coord_map[max_x][y])
    no_infinite_area_dict = dict(coord_area_dict)
    for area in infinite_areas:
        del no_infinite_area_dict[area]
    return no_infinite_area_dict

def find_max_area(areas_dict):
    max = 0
    for key, value in areas_dict.items():
        if max < value:
            max = value
    return max

def output(filename, text):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(text)

def main():
    coordinates_str = input("input.txt")
    coordinates = str_to_coordinates(coordinates_str)
    (min_x, min_y, max_x, max_y) = get_limits(coordinates)
    #map_string = paint_map(min_x, min_y, max_x, max_y, coordinates)
    coord_map = fill_map(min_x, min_y, max_x, max_y, coordinates)
    coord_area_dict = fill_coord_area_dict(min_x, min_y, max_x, max_y, coord_map)
    no_infinite_areas_dict = remove_infinite_areas(min_x, min_y, max_x, max_y, coord_map, coord_area_dict)
    max_area_size = find_max_area(no_infinite_areas_dict)
    
    output("output.txt", str(max_area_size))

main()