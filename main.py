'''TO DO:

- VALIDATE SCHEDULES, ROOMS, AND TIMESLOTS: MAY NAG DDOUBLE PA TAS YUNG IBANG SUBJECTS
    DI NALALAGYAN NG SCHEDULE
    sa main function if false yung validate function
     maintain the current sched and skip the update
        else, update the sched and calculate the fitness
- UNCOMMENT THE VALIDATION FUNCTION TO SEE THE ERROR
- LAB AND LEC CONSTRAINTS
- MAX HOURS OF PROFESSORS PER WEEK
-

-There are 35 subjects in total:
    Total subjects for Year 1: 9
    Total subjects for Year 2: 11
    Total subjects for Year 3: 9
    Total subjects for Year 4: 6
-if there are 2 section in first yr and 2 sections in second yr,
    then there should be 55 list of subs in total'''

import random
from collections import defaultdict

# Example data structures
sections = {
    1: ['Section 1A', 'Section 1B'],
    2: ['Section 2A', 'Section 2B'],
    3: ['Section 3A'],
    4: ['Section 4A']
}

professors = {
    'Prof A': {'preferred_time': 'AM', 'preferred_subjects': ['CC113-M', 'CC131L-M']},
    'Prof B': {'preferred_time': 'PM', 'preferred_subjects': ['', '']},
    'Prof C': {'preferred_time': 'PM', 'preferred_subjects': ['', '']},
    'Prof D': {'preferred_time': 'PM', 'preferred_subjects': ['', '']},
    'Prof E': {'preferred_time': 'PM', 'preferred_subjects': ['', 'CS333-M']},
    'Prof F': {'preferred_time': 'PM', 'preferred_subjects': ['', '']},
    'Prof G': {'preferred_time': 'PM', 'preferred_subjects': ['CS433-M', '']},
    'Prof H': {'preferred_time': 'PM', 'preferred_subjects': ['', 'CS272-M']},
    'Prof I': {'preferred_time': 'PM', 'preferred_subjects': ['', '']},
    'Prof J': {'preferred_time': 'PM', 'preferred_subjects': ['', '']},

    # Add more professors as needed
}

#First Semester
subjects = {
    1: {'CC113-M': {'type': 'lec', 'units': 1}, 'CC131L-M': {'type': 'lab', 'units': 1}, 'CC132-M': {'type': 'lec', 'units': 2}, 'GEC1-M': {'type': 'lec', 'units': 3}, 'GEC4-M': {'type': 'lec', 'units': 3}, 'GEC7-M': {'type': 'lec', 'units': 3}, 'MATHA05S-M': {'type': 'lec', 'units': 5}, 'NSTP1-M': {'type': 'lec', 'units': 3}, 'PE1-M': {'type': 'lec', 'units': 2}},
    2: {'CC211L-M': {'type': 'lab', 'units': 1}, 'CC212-M': {'type': 'lec', 'units': 2}, 'CS213-M': {'type': 'lec', 'units': 3}, 'CS233-M': {'type': 'lec', 'units': 3}, 'CS251L-M': {'type': 'lab', 'units': 1}, 'CS252-M': {'type': 'lec', 'units': 2}, 'CS271L-M': {'type': 'lab', 'units': 1}, 'CS272-M': {'type': 'lec', 'units': 2}, 'GEC6-M': {'type': 'lec', 'units': 3}, 'GEC8-M': {'type': 'lec', 'units': 3}, 'PE3-M': {'type': 'lec', 'units': 2}},
    3: {'CC311L-M': {'type': 'lab', 'units': 1}, 'CC312-M': {'type': 'lec', 'units': 2}, 'CS313-M': {'type': 'lec', 'units': 3}, 'CS333-M': {'type': 'lec', 'units': 3}, 'CS351L-M': {'type': 'lab', 'units': 1}, 'CS352-M': {'type': 'lec', 'units': 2}, 'CS373-M': {'type': 'lec', 'units': 3}, 'CSE1-M': {'type': 'lec', 'units': 3}, 'CSE2-M': {'type': 'lec', 'units': 3}},
    4: {'CS413-M': {'type': 'lec', 'units': 3}, 'CS433-M': {'type': 'lec', 'units': 3}, 'GEE11D-M': {'type': 'lec', 'units': 3}, 'GEE12D-M': {'type': 'lec', 'units': 3}, 'GEE13D-M': {'type': 'lec', 'units': 3}, 'GEM14-M': {'type': 'lec', 'units': 3}}
}

rooms = ['Room 322', 'Room 324', 'Room 326','Room 328', 'Room DOST-A', 'Room DOST-B', 'Room BODEGA-A', 'Room BODEGA-b']
time_slots = {
    'H1': {'start': 7, 'end': 8},
    'H2': {'start': 8, 'end': 9},  # 8:00 AM to 9:00 AM
    'H3': {'start': 9, 'end': 10},  # 9:00 AM to 10:00 AM
    'H4': {'start': 10, 'end': 11},  # 10:00 AM to 11:00 AM
    'H5': {'start': 11, 'end': 12},  # 11:00 AM to 12:00 PM
    'H6': {'start': 12, 'end': 13},  # 12:00 PM to 1:00 PM
    'H7': {'start': 13, 'end': 14},  # 1:00 PM to 2:00 PM
    'H8': {'start': 14, 'end': 15},  # 2:00 PM to 3:00 PM
    'H9': {'start': 15, 'end': 16},  # 3:00 PM to 4:00 PM
    'H10': {'start': 16, 'end': 17},  # 4:00 PM to 5:00 PM
    'H11': {'start': 17, 'end': 18}  # 5:00 PM to 6:00 PM
}
swarm_size = 30
max_iterations = 100
w = 0.5
c1 = 1.5
c2 = 1.5


class Particle:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.fitness = float('-inf')
        self.pBest = position
        self.pBest_fitness = float('-inf')


def initialize_particle(sections, subjects, professors, time_slots, rooms, max_attempts=1000):
    for _ in range(max_attempts):
        schedule = []
        assigned_subjects = set()
        section_time_slots = defaultdict(list)  # Store the used time slots for each section

        for year, year_sections in sections.items():
            for section in year_sections:
                subject_pool = subjects[year].copy()  # Create a copy of the subjects for this year
                time_slots_copy = list(time_slots.keys())  # Create a copy of the time slots for this section
                while subject_pool:  # While there are still subjects to be scheduled
                    subject = random.choice(list(subject_pool.keys()))
                    del subject_pool[subject]  # Remove the subject from the pool

                    available_professors = [prof for prof in professors if subject in professors[prof]['preferred_subjects'] and prof not in assigned_subjects]
                    if not available_professors:
                        available_professors = [prof for prof in professors if prof not in assigned_subjects]
                    if not available_professors:
                        available_professors = list(professors.keys())  # Fallback to any professor if still empty

                    professor = random.choice(available_professors)
                    assigned_subjects.add(professor)

                    if not time_slots_copy:  # If all time slots have been used, reset the copy
                        time_slots_copy = list(time_slots.keys())

                    time_slot = random.choice(time_slots_copy)  # Choose a random time slot from the copied time_slots
                    subj_type=subjects[year][subject]['type']
                    print("SUBJECT TYPE", subj_type)
                    # If the subject is a lab, block the next 2 time slots
                    if subj_type == 'lab':
                        #print("INSIDE LAB")
                        next_time_slot_index = time_slots_copy.index(time_slot) + 1
                        if next_time_slot_index < len(time_slots_copy):
                            blocked_time_slot = time_slots_copy[next_time_slot_index]
                            section_time_slots[section].append(blocked_time_slot)
                            time_slots_copy.remove(blocked_time_slot)
                        if next_time_slot_index + 1 < len(time_slots_copy):
                            blocked_time_slot = time_slots_copy[next_time_slot_index + 1]
                            section_time_slots[section].append(blocked_time_slot)
                            time_slots_copy.remove(blocked_time_slot)
                    # If the subject is a lecture, block the next time slot
                    elif subj_type == 'lec':
                        print("UNITS NG LEC",subjects[year][subject]['units'])
                        if subjects[year][subject]['units'] == 3:
                            next_time_slot_index = time_slots_copy.index(time_slot) + 3
                            if next_time_slot_index < len(time_slots_copy):
                                blocked_time_slot = time_slots_copy[next_time_slot_index]
                                section_time_slots[section].append(blocked_time_slot)
                                time_slots_copy.remove(blocked_time_slot)
                        elif subjects[year][subject]['units'] == 2:
                            next_time_slot_index = time_slots_copy.index(time_slot) + 2
                            if next_time_slot_index < len(time_slots_copy):
                                blocked_time_slot = time_slots_copy[next_time_slot_index]
                                section_time_slots[section].append(blocked_time_slot)
                                time_slots_copy.remove(blocked_time_slot)

                    room = random.choice(rooms)

                    schedule.append((section, subject, professor, time_slot, room))
                    time_slots_copy.remove(time_slot)  # Remove the chosen time slot from the copy after it's used

        # Validate the generated schedule
        validated_schedule = validate_position(schedule)
        if validated_schedule:
            return validated_schedule

    # If no valid schedule is found after maximum attempts, return None
    return None


def initialize_swarm(swarm_size, sections, subjects, professors, time_slots, rooms):
    swarm = []
    for _ in range(swarm_size):
        position = None
        while position is None:
            position = initialize_particle(sections, subjects, professors, time_slots, rooms)
        velocity = [0] * len(position)  # Initial velocity
        swarm.append(Particle(position, velocity))
    return swarm



def preference_score(professor, time_slot):
    preferred_time = professors[professor]['preferred_time']
    if preferred_time in time_slot:
        return 10
    return 5

def get_subject_year(subject):
    for year, subjects_in_year in subjects.items():
        if subject in subjects_in_year:
            return year
    return None

def calculate_conflicts(schedule):
    conflicts = 0
    time_room_usage = {}
    time_professor_usage = {}

    for (section, subject, professor, time_slot, room) in schedule:
        year = get_subject_year(subject)
        if year is None:
            print(f"Error: Year not found for subject {subject}")
            continue

        time_slot_start = time_slots[time_slot]['start']
        if subjects[year][subject]['type'] == 'lec':
            time_slot_end = time_slot_start + subjects[year][subject]['units']  # 1 hour for lecture
        else:
            time_slot_end = time_slot_start + subjects[year][subject]['units'] * 3  # 3 hours for lab

        # Check for room conflict
        for (used_time_slot, used_room) in time_room_usage.keys():
            used_time_slot_start = time_slots[used_time_slot]['start']
            used_time_slot_end = time_slots[used_time_slot]['end']

            if room == used_room and not (time_slot_end <= used_time_slot_start or time_slot_start >= used_time_slot_end):
                conflicts += 1
        time_room_usage[(time_slot, room)] = True

        # Check for professor conflict
        for (used_time_slot, used_professor) in time_professor_usage.keys():
            used_time_slot_start = time_slots[used_time_slot]['start']
            used_time_slot_end = time_slots[used_time_slot]['end']

            if professor == used_professor and not (time_slot_end <= used_time_slot_start or time_slot_start >= used_time_slot_end):
                conflicts += 1
        time_professor_usage[(time_slot, professor)] = True

    return conflicts

def calculate_distribution(schedule):
    teacher_gaps = 0
    for professor in professors:
        times = [time_slot for (section, subject, prof, time_slot, room) in schedule if prof == professor]
        teacher_gaps += len(set(times))
    return -teacher_gaps


def calculate_fitness(schedule):
    preference_scores = sum(preference_score(prof, time_slot) for (section, subject, prof, time_slot, room) in schedule)
    conflict_penalty = calculate_conflicts(schedule)
    distribution_score = calculate_distribution(schedule)
    return preference_scores - conflict_penalty + distribution_score


def update_velocity(particle, gBest, w, c1, c2):
    new_velocity = []
    print("Particle Position: ", particle.position)
    for i in range(len(particle.position)):
        r1 = random.random()
        r2 = random.random()

        pos_num = convert_to_numeric(particle.position[i])
        pBest_num = convert_to_numeric(particle.pBest[i])
        gBest_num = convert_to_numeric(gBest[i])

        cognitive = c1 * r1 * (pBest_num - pos_num)
        social = c2 * r2 * (gBest_num - pos_num)

        new_velocity.append(w * (particle.velocity[i] if particle.velocity else 0) + cognitive + social)
    print("new velocity: ", new_velocity)
    return new_velocity


def update_position(particle):
    """
    Update the position of a particle based on its velocity and ensure it is valid.

    Parameters:
    particle (Particle): The particle whose position is being updated.

    Returns:
    list: The new, validated position of the particle.
    """
    new_position = []
    for i in range(len(particle.position)):
        current_pos = particle.position[i]
        current_pos_num = convert_to_numeric(current_pos)
        new_pos_num = round(current_pos_num + particle.velocity[i]) % len(num_to_position)
        new_pos = convert_from_numeric(new_pos_num)
        validated_pos = validate_position([new_pos])  # Validate the new position as a list
        if validated_pos:
            new_position.append(validated_pos[0])  # Add the validated position to the new position
        else:
            # If validation fails, adjust the event
            print(f"Conflict detected at index {i}, adjusting event.")
            adjusted_event = adjust_event(new_pos)
            new_position.append(adjusted_event)
    print("new position(BEFORE RETURN): ", new_position)
    return new_position


# Global variables to store the mappings
position_to_num = {}
num_to_position = {}

def convert_to_numeric(position):
    global position_to_num, num_to_position
    if position not in position_to_num:
        num = len(position_to_num)
        position_to_num[position] = num
        num_to_position[num] = position
    return position_to_num[position]

def convert_from_numeric(num):
    global num_to_position
    return num_to_position[num]


def validate_position(position):
    professor_schedule = defaultdict(set)
    room_schedule = defaultdict(set)
    section_subjects = defaultdict(set)

    i = 0
    while i < len(position):
        section, subject, professor, time_slot, room = position[i]

        # Check for double booking for professors
        if professor in professor_schedule and time_slot in professor_schedule[professor]:
            print(f"Double booking detected for professor {professor} at {time_slot}")
            adjusted_event = adjust_event(position[i])
            if not adjusted_event:  # If adjustment fails
                return None
            position[i] = adjusted_event  # Replace the conflicting event with the adjusted event
        professor_schedule[professor].add(time_slot)

        # Check for double booking for rooms
        if room in room_schedule and time_slot in room_schedule[room]:
            print(f"Double booking detected for room {room} at {time_slot}")
            adjusted_event = adjust_event(position[i])
            if not adjusted_event:  # If adjustment fails
                return None
            position[i] = adjusted_event  # Replace the conflicting event with the adjusted event
        room_schedule[room].add(time_slot)

        # Check for double subjects per section
        if subject in section_subjects[section]:
            print(f"Double subject {subject} detected in section {section}")
            del position[i]  # Remove the duplicate subject
            continue  # Skip the increment of i
        section_subjects[section].add(subject)

        # Validate the duration of each subject based on its units
        year = get_subject_year(subject)
        subject_units = subjects[year][subject]['units']
        subject_type = subjects[year][subject]['type']
        expected_duration = subject_units * 3 if subject_type == 'lab' else subject_units
        actual_duration = time_slots[time_slot]['end'] - time_slots[time_slot]['start']
        if actual_duration != expected_duration:
            print(f"Invalid duration for {subject_type} {subject} in section {section} at {time_slot}")
            adjusted_event = adjust_event(position[i])
            if not adjusted_event:  # If adjustment fails
                return None
            position[i] = adjusted_event  # Replace the conflicting event with the adjusted event

        i += 1  # Increment i

    return position

def adjust_schedule(schedule):
    conflicts_resolved = 0
    # Iterate through the schedule to identify conflicts
    for i, event1 in enumerate(schedule):
        for j, event2 in enumerate(schedule[i + 1:]):  # Avoid double-checking pairs
            j += i + 1  # Adjust index to account for slicing
            # Check for double booking
            if event1[3] == event2[3] and (event1[4] == event2[4] or event1[2] == event2[2]):
                # Resolve conflict by adjusting one of the events
                if random.choice([True, False]):  # Randomly choose which event to adjust
                    event1 = adjust_event(event1)
                else:
                    event2 = adjust_event(event2)
                schedule[i] = event1
                schedule[j] = event2
                conflicts_resolved += 1
    return schedule, conflicts_resolved

def adjust_event(event):
    section, subject, professor, time_slot, room = event
    year = get_subject_year(subject)
    subject_units = subjects[year][subject]['units']
    subject_type = subjects[year][subject]['type']
    expected_duration = subject_units * 3 if subject_type == 'lab' else subject_units

    # Adjust the event by changing its time slot or room
    event = list(event)  # Convert tuple to list for modification

    # Choose a new random time slot that can accommodate the expected duration
    available_time_slots = [ts for ts in time_slots if time_slots[ts]['end'] - time_slots[ts]['start'] >= expected_duration]
    if available_time_slots:
        event[3] = random.choice(available_time_slots)

    event[4] = random.choice(rooms)  # Choose a new random room

    return tuple(event)

# Example usage:



'''def validate_position(position):
    # Validate the position (e.g., no double-booking)
    return position'''






def group_schedule_by_section(schedule):
    grouped_schedule = defaultdict(list)
    for entry in schedule:
        section = entry[0]
        grouped_schedule[section].append(entry)
    return grouped_schedule


def main():
    # Initialize swarm
    swarm = initialize_swarm(swarm_size, sections, subjects, professors, time_slots, rooms)
    print("Swarm size:", swarm_size)
    #each particle in swarm is an instance or memory address of where the particle is located
    # Initialize gBest to the position of the first particle in the swarm
    gBest = None
    gBest_fitness = float('-inf')
    print("initial gBest: ", gBest)
    n = 0
    print("Swarm Initialized:", swarm)
    # Evaluate initial fitness
    for particle in swarm:
        particle.fitness = calculate_fitness(particle.position)
        particle.pBest = particle.position
        particle.pBest_fitness = particle.fitness
        if particle.fitness > gBest_fitness:
            gBest = particle.position
            gBest_fitness = particle.fitness
            print("particle.fitness > gBest_fitness: ", gBest)
        # Iterate
    for iteration in range(max_iterations):
        for particle in swarm:
            print(particle, gBest, w, c1, c2)
            print("Particle Position:", particle.position)
            print("Particle Velocity:", particle.velocity)

            particle.velocity = update_velocity(particle, gBest, w, c1, c2)
            print("PARTICLE.position TYPE: ", type(particle.position))
            print("before update: ", particle.position)
            #particle_instance = Particle(list(particle.), [0] * len(particle))  # Create a Particle instance
            particle.position = update_position(particle)
            print("after update: ", particle.position)
            particle.position = validate_position(particle.position)
            print("after validate: ", particle.position)

            if particle.position:
                particle.fitness = calculate_fitness(particle.position)
                if particle.fitness > particle.pBest_fitness:
                    particle.pBest = particle.position
                    particle.pBest_fitness = particle.fitness
                if particle.fitness > gBest_fitness:
                    print("particle position in >gBest:", particle.position)
                    gBest = particle.position
                    gBest_fitness = particle.fitness
            else:
                print("Skipping fitness calculation due to invalid position.")

    print("Final gBest:", gBest)

    # The gBest now holds the best found schedule
    # This print statement is for the division per section of the overall schedule
    grouped_schedule = group_schedule_by_section(gBest)
    print("Optimized Schedule:")
    for section, entries in grouped_schedule.items():
        print(f"\n{section}:")
        for entry in entries:
            n += 1
            print(f"{n}. {entry}")
    print("\nFitness Score:", gBest_fitness)


    # The gBest now holds the best found schedule
    # This print statement is for you to see the overall schedule
    '''print("Optimized Schedule:\n" + '\n'.join(f"{n+i+1}. {entry}" for i, entry in enumerate(gBest)))
    print("Fitness Score:", gBest_fitness)'''

if __name__ == "__main__":
    main()



