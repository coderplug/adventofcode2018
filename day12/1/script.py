import re

def input(filename):
    with open(filename, "r", encoding="utf-8") as f_in:
        return f_in.read().splitlines()

def parse_text(lines):
    initial_state = get_initial_state(lines[0])
    rules = get_rules(lines[2:])
    return initial_state, rules

def get_initial_state(line):
    m = re.match(r"initial state: (.*)", line)
    initial_state =  m.group(1)   
    return initial_state

def get_rules(lines):
    rules = {}
    for line in lines:
        m = re.match(r"(.*) => (.*)", line)
        placements = m.group(1)
        result = m.group(2)
        rules[placements] = result
    return rules

def run_generations(gen_count, state, rule_dict):
    new_state = state[:]
    state_index = 0
    for _ in range(gen_count):
        (new_state, state_index) = run_generation(new_state, state_index, rule_dict)
    sum = plant_pos_sum(new_state, state_index)
    return sum

def run_generation(state, state_index, rule_dict):
    temp_state = list("...." + state + "....")
    new_state = temp_state[:]
    total_length = len(temp_state)
    start_index = 2
    end_index = total_length - 2
    
    for index in range(start_index, end_index):
        llcrr = ''.join(temp_state[index-2:index+3])
        if llcrr in rule_dict:
            new_state[index] = rule_dict[llcrr]
        else:
            new_state[index] = "."

    new_state_str = ''.join(new_state)

    new_state_index = find_new_state_index(new_state_str, state_index)

    new_state_strip = new_state_str.strip(".")
    
    return (new_state_strip, new_state_index)

def find_new_state_index(new_state_str, state_index):
    LEFT_POT_COUNT = 4
    first_plant_pos = new_state_str.index("#")
    return state_index + first_plant_pos - LEFT_POT_COUNT

def plant_pos_sum(state, state_index):
    sum = 0
    for index in range(len(state)):
        if state[index] == '#':
            sum += index + state_index
    return sum

def output(filename, text):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(text)

def main():
    GEN_COUNT = 20
    lines = input("input.txt")
    (initial_state, rule_dict) = parse_text(lines)
    sum = run_generations(GEN_COUNT, initial_state, rule_dict)
    output("output.txt", str(sum))

main()