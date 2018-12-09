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

def get_instruction_order(worker_count, step_requirements):
    workers = get_workers(worker_count)
    seconds = 0
    available_steps = list(find_available_steps(step_requirements))
    instruction_order = []
    done = False
    while not(done):
        available_steps = sorted(available_steps)
        add_completed_steps(workers, instruction_order)
        unlocked_steps = find_unlocked_steps(instruction_order, step_requirements)
        available_steps.extend(unlocked_steps)
        assign_steps(workers, available_steps)
        done = is_done(workers)
        #print_status(seconds, workers)
        seconds = pass_second(seconds, workers)
    return (seconds - 1, ''.join(instruction_order))

def get_workers(count):
    workers = []
    for number in range(count):
        worker = Worker()
        workers.append(worker)
    return workers

def find_available_steps(step_requirements):
    available_steps = set()
    for key, value in step_requirements.items():
        for step in value:
            if step not in step_requirements:
                available_steps.add(step)
    return available_steps

def add_completed_steps(workers, instruction_order):
    for worker in workers:
        if worker.time_left == 0 and worker.step is not(None):
            instruction_order.append(worker.step)
            worker.step = None

def find_unlocked_steps(instruction_order, step_requirements):
    unlocked_steps = []
    for key, value in step_requirements.items():
        if set(value).issubset(instruction_order):
            unlocked_steps.append(key)
    for step in unlocked_steps:
        del step_requirements[step]
    return unlocked_steps

def assign_steps(workers, available_steps):
    for worker in workers:
        if worker.step is None and available_steps != []:
            worker.step = available_steps[0]
            available_steps.remove(worker.step)
            worker.time_left = 60 + letter_to_position(worker.step)

def letter_to_position(letter):
    UPPER_CASE_A = 65
    UPPER_CASE_Z = 90
    upper_case_pos = ord(letter.upper())
    if upper_case_pos > UPPER_CASE_Z or upper_case_pos < UPPER_CASE_A:
        return 0
    else:
        return upper_case_pos - UPPER_CASE_A + 1

class Worker:
    def __init__(self, step = None, time_left = 0):
        self.step = step
        self.time_left = time_left
    
    def pass_second(self):
        if self.time_left > 0:
            self.time_left -= 1
        return self.time_left

def pass_second(seconds, workers):
    for worker in workers:
        worker.pass_second()
    return seconds + 1

def is_done(workers):
    for worker in workers:
        if worker.step is not(None):
            return False
    return True

def print_status(seconds, workers):
    result = str(seconds)
    for worker in workers:
        step_value = str(worker.step) if worker.step is not(None) else "None"
        result = result + " " + step_value
    print(result)

def output(filename, text):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(text)

def main():
    WORKER_COUNT = 5
    lines = input("input.txt")
    step_requirements = parse_requirements(lines)
    (seconds, instruction_order) = get_instruction_order(WORKER_COUNT, step_requirements)
    output("output.txt", "{} {}".format(seconds, instruction_order))

main()