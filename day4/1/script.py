from datetime import datetime, timedelta

def input(filename):
    with open(filename, "r", encoding="utf-8") as f_in:
        lines = f_in.read().splitlines()
        return lines

def parse_entries(entries):
    parsed_entries = []
    for entry in entries:
        parts = entry.split(" ")
        
        date_parts = parts[0].split("-")
        year = int(date_parts[0][1:])
        month = int(date_parts[1])
        day = int(date_parts[2])

        time_parts = parts[1].split(":")
        hour = int(time_parts[0])
        minute = int(time_parts[1][:-1])

        action_parts = parts[2:]
        entry = Entry(year, month, day, hour, minute, action_parts)
        parsed_entries.append(entry)
    return parsed_entries

class Entry:
    def __init__(self, year, month, day, hour, minute, action):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.action = action

    def __repr__(self):
        return "[{}-{}-{} {}:{}] {}".format(self.year, self.month, self.day, self.hour, self.minute, ' '.join(self.action))
    
    def __str__(self):
        return "[{}-{}-{} {}:{}] {}".format(self.year, self.month, self.day, self.hour, self.minute, ' '.join(self.action))

    def get_date(self):
        return datetime(self.year, self.month, self.day, self.hour, self.minute)

def sort_entries(unsorted_entries):
    sorted_entries = entries_merge_sort(unsorted_entries)
    return sorted_entries

def entries_merge_sort(unsorted_list):
    list_length = len(unsorted_list)
    if list_length > 1:
        sorted_list = []
        
        #Divide: Divide the n-element sequence to be sorted into two subsequences of n=2 
        #        elements each.
        middle = list_length // 2
        
        left_half = unsorted_list[:middle]
        right_half = unsorted_list[middle:]

        #Conquer: Sort the two subsequences recursively using merge sort.
        sorted_left_half = entries_merge_sort(left_half)
        sorted_right_half = entries_merge_sort(right_half)

        left_index = 0
        right_index = 0

        #Combine: Merge the two sorted subsequences to produce the sorted answer.
        while len(sorted_list) != list_length:
            left_entry = sorted_left_half[left_index]
            right_entry = sorted_right_half[right_index]
            left_time = datetime(left_entry.year, left_entry.month, left_entry.day, left_entry.hour, left_entry.minute)
            right_time = datetime(right_entry.year, right_entry.month, right_entry.day, right_entry.hour, right_entry.minute)
            if left_time > right_time:
                sorted_list.append(right_entry)
                right_index += 1
            else:
                sorted_list.append(left_entry)
                left_index += 1
            if left_index == len(sorted_left_half):
                sorted_list.extend(sorted_right_half[right_index:])
            elif right_index == len(sorted_right_half):
                sorted_list.extend(sorted_left_half[left_index:])
        return sorted_list
    else:
        return unsorted_list

def find_guards_list(entries):
    mode = 0
    current_guard = None
    sleep = None
    wake = None
    shift_starts = None
    shift_ends = None
    guard_list = []
    for entry in entries:
        if entry.action[0] == "Guard" and entry.action[2] == "begins" and entry.action[3] == "shift":
            if current_guard is not None:
                shift_ends = entry.get_date()
                current_guard.shifts.append((shift_starts, shift_ends))
            guard_id = int(entry.action[1][1:])
            current_guard = find_guard(guard_list, guard_id)
            if current_guard is None:
                current_guard = Guard(guard_id)
                guard_list.append(current_guard)
            shift_starts = entry.get_date()
        elif entry.action[0] == "falls" and entry.action[1] == "asleep":
            sleep = entry.minute
        elif entry.action[0] == "wakes" and entry.action[1] == "up":
            wake = entry.minute
            current_guard.sleep_time.append((sleep, wake))
    return guard_list

def find_guard(guard_list, guard_id):
    for guard in guard_list:
        if guard.id == guard_id:
            return guard
    return None

class Guard:
    def __init__(self, id):
        self.sleep_time = []
        self.id = id
        self.shifts = []

    def calculate_total_sleep_time(self):
        total = 0
        for entry in self.sleep_time:
            total += self.calculate_sleep_time(entry)
        return total

    def calculate_sleep_time(self, sleep_entry):
        (sleep_from, sleep_to) = sleep_entry
        return sleep_to - sleep_from

def find_most_sleepy_guard(guards):
    most_sleepy = guards[0] if guards else None
    for guard in guards:
        if most_sleepy.calculate_total_sleep_time() < guard.calculate_total_sleep_time():
            most_sleepy = guard
    return most_sleepy

def find_most_sleepy_minute(guard):
    sleep_minute_count = [0] * 60
    for (sleep_from, sleep_to) in guard.sleep_time:
        for minute in range(sleep_from, sleep_to):
            sleep_minute_count[minute] += 1
    return find_index_max_count(sleep_minute_count)

def find_index_max_count(list):
    max_index = 0
    for index in range(len(list)):
        if list[max_index] < list[index]:
            max_index = index
    return max_index
        

def output(filename, text):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(text)

def main():
    unsorted_entries = input("input.txt")
    unsorted_parsed_entries = parse_entries(unsorted_entries)
    sorted_parsed_entries = sort_entries(unsorted_parsed_entries)
    guards = find_guards_list(sorted_parsed_entries)
    guard = find_most_sleepy_guard(guards)
    minute = find_most_sleepy_minute(guard)
    output("output.txt", str(guard.id * minute))

main()