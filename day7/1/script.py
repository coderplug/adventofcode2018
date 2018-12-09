def input(filename):
    with open(filename, "r", encoding="utf-8") as f_in:
        lines = f_in.read().splitlines()
        return lines

def parse_requirements(str_lines):
    step_requirements = {}
    for line in str_lines:
        words = line.split(" ")
        prerequisite = words[1]
        step = words[7]
        if step in step_requirements:
            step_requirements[step].append(prerequisite)
        else:
            step_requirements[step] = [prerequisite]
    return step_requirements

def get_instruction_order(step_requirements):
    available_steps = list(find_available_steps(step_requirements))
    instruction_order = []
    while available_steps != []:
        available_steps = sorted(available_steps)
        next_step = available_steps[0]
        instruction_order.append(next_step)
        available_steps.remove(next_step)
        unlocked_steps = find_unlocked_steps(instruction_order, step_requirements)
        available_steps.extend(unlocked_steps)
    return ''.join(instruction_order)

def find_available_steps(step_requirements):
    available_steps = set()
    for key, value in step_requirements.items():
        for step in value:
            if step not in step_requirements:
                available_steps.add(step)
    return available_steps

def find_unlocked_steps(instruction_order, step_requirements):
    unlocked_steps = []
    for key, value in step_requirements.items():
        if set(value).issubset(instruction_order):
            unlocked_steps.append(key)
    for step in unlocked_steps:
        del step_requirements[step]
    return unlocked_steps

def output(filename, text):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(text)

def main():
    lines = input("input.txt")
    step_requirements = parse_requirements(lines)
    instruction_order = get_instruction_order(step_requirements)
    output("output.txt", instruction_order)

main()