import re

def input(filename):
    with open(filename, "r", encoding="utf-8") as f_in:
        return f_in.read().splitlines()

def parse_points(lines):
    points = []
    for line in lines:
        m = re.match(r'position=<(.*), (.*)> velocity=<(.*),(.*)>', line)
        pos_x = int(m.group(1))
        pos_y = int(m.group(2))
        vel_x = int(m.group(3))
        vel_y = int(m.group(4))

        position = (pos_x, pos_y)
        velocity = (vel_x, vel_y)

        point = Point(position, velocity)
        points.append(point)
    return points

class Point:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

def cycle(points):
    cycled_points = points[:]
    for second in range(1, 100000):
        for point in cycled_points:
            (x, y) = point.position
            (vel_x, vel_y) = point.velocity
            x += vel_x
            y += vel_y
            point.position = (x, y)
        text = points_to_text(cycled_points)
        if text is not(None):
            output("output"+str(second)+".txt", text)
    return cycled_points

def points_to_text(points):
    (min_xy, max_xy) = get_min_max(points)
    
    (min_x, min_y) = min_xy
    (max_x, max_y) = max_xy

    size_x = max_x - min_x + 1
    size_y = max_y - min_y + 1

    if size_x < 100 and size_y < 100:
        array = [['.'] * size_x for y in range(size_y)]

        for point in points:
            (x, y) = point.position
            (array_x, array_y) = (x - min_x, y - min_y)
            array[array_y][array_x] = '#'
        
        string_list = []
        for line in array:
            string_list.append(''.join(line))
        text = '\n'.join(string_list)
        return text
    return None

def get_min_max(points):
    (min_x, min_y) = points[0].position
    (max_x, max_y) = points[0].position
    for point in points:
        (x, y) = point.position
        if min_x > x:
            min_x = x
        elif max_x < x:
            max_x = x
        if min_y > y:
            min_y = y
        elif max_y < y:
            max_y = y
    min_xy = (min_x, min_y)
    max_xy = (max_x, max_y)
    return (min_xy, max_xy)

    
def output(filename, text):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(text)

def main():
    lines = input("input.txt")
    points = parse_points(lines)
    cycle(points)

main()