def input(filename):
    with open(filename, "r", encoding="utf-8") as f_in:
        return f_in.read().splitlines()

def split_to_numbers(lines):
    number_list = []
    for line in lines:
        number_list.extend(line.split(' '))
    number_list = [int(i) for i in number_list]
    return number_list

def find_parent_value(numbers):
    new_list = numbers[:]
    (parent, _) = get_children(new_list)
    parent_value = find_value(parent)
    return parent_value

def find_value(node):
    value = 0
    if node.children == []:
        value = sum(node.metadata)
    else:
        for metadata in node.metadata:
            child_index = metadata - 1
            if child_exists(node.children, child_index):
                value += find_value(node.children[child_index])
    return value

def child_exists(list, index):
    list_length = len(list)
    if list_length > index and index >= 0:
        return True
    return False 

def get_children(num_list):
    children_count = num_list[0]
    metadata_count = num_list[1]
    index = 2
    children = []
    for _ in range(children_count):
        (child, child_index) = get_children(num_list[index:])
        children.append(child)
        index += child_index
    metadata = get_metadata(num_list[index:], metadata_count)
    index += metadata_count
    parent = Node(children, metadata)
    return (parent, index)

def get_metadata(num_list, count):
    return num_list[:count]

class Node:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

    def __repr__(self):
        return "{} {}".format(self.children, self.metadata)

    def __str__(self):
        return "{} {}".format(self.children, self.metadata)

def output(filename, text):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(text)

def main():
    lines = input("input.txt")
    numbers = split_to_numbers(lines)
    parent_value = find_parent_value(numbers)
    output("output.txt", str(parent_value))

main()