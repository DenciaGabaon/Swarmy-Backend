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
    'Prof A': {'preferred_time': 'AM', 'preferred_subjects': ['CS101', 'CS201']},
    'Prof B': {'preferred_time': 'PM', 'preferred_subjects': ['CS102', 'CS202']},
    'Prof C': {'preferred_time': 'PM', 'preferred_subjects': ['CS102', 'CS202']},
    'Prof D': {'preferred_time': 'PM', 'preferred_subjects': ['CS102', 'CS202']},
    'Prof E': {'preferred_time': 'PM', 'preferred_subjects': ['CS102', 'CS202']},
    'Prof F': {'preferred_time': 'PM', 'preferred_subjects': ['CS102', 'CS202']},
    'Prof G': {'preferred_time': 'PM', 'preferred_subjects': ['CS102', 'CS202']},
    'Prof H': {'preferred_time': 'PM', 'preferred_subjects': ['CS102', 'CS202']},
    'Prof I': {'preferred_time': 'PM', 'preferred_subjects': ['CS102', 'CS202']},
    'Prof J': {'preferred_time': 'PM', 'preferred_subjects': ['CS102', 'CS202']},

    # Add more professors as needed
}

#First Semester
subjects = {
    1: ['CC113-M', 'CC131L-M', 'CC132-M', 'GEC1-M', 'GEC4-M', 'GEC7-M', 'MATHA05S-M', 'NSTP1-M', 'PE1-M'],
    2: ['CC211L-M', 'CC212-M', 'CS213-M', 'CS233-M', 'CS251L-M', 'CS252-M', 'CS271L-M',
        'CS272-M', 'GEC6-M', 'GEC8-M', 'PE3-M'],
    3: ['CC311L-M', 'CC312-M', 'CS313-M', 'CS333-M', 'CS351L-M', 'CS352-M', 'CS373-M', 'CSE1-M', 'CSE2-M'],
    4: ['CS413-M', 'CS433-M', 'GEE11D-M', 'GEE12D-M', 'GEE13D-M', 'GEM14-M']
}

rooms = ['Room 321', 'Room 322', 'Room 326', 'Room DOST', 'Room Lab', 'Room a', 'Room b', 'Room c']
time_slots = ['AM1', 'AM2', 'PM1', 'PM2']
swarm_size = 10
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


def initialize_particle(sections, subjects, professors, time_slots, rooms):
    schedule = []
    assigned_subjects = set()

    for year, year_sections in sections.items():
        for section in year_sections:
            subject_pool = subjects[year].copy()  # Create a copy of the subjects for this year
            while subject_pool:  # While there are still subjects to be scheduled
                subject = random.choice(subject_pool)
                subject_pool.remove(subject)  # Remove the subject from the pool

                available_professors = [prof for prof in professors if subject in professors[prof]['preferred_subjects'] and prof not in assigned_subjects]
                if not available_professors:
                    available_professors = [prof for prof in professors if prof not in assigned_subjects]
                if not available_professors:
                    available_professors = list(professors.keys())  # Fallback to any professor if still empty

                professor = random.choice(available_professors)
                assigned_subjects.add(professor)

                time_slot = random.choice(time_slots)
                room = random.choice(rooms)

                schedule.append((section, subject, professor, time_slot, room))

    return schedule


def initialize_swarm(swarm_size, sections, subjects, professors, time_slots, rooms):
    swarm = []
    for _ in range(swarm_size):
        position = initialize_particle(sections, subjects, professors, time_slots, rooms)
        velocity = [0] * len(position)  # Initial velocity
        swarm.append(Particle(position, velocity))
    return swarm


def preference_score(professor, time_slot):
    preferred_time = professors[professor]['preferred_time']
    if preferred_time in time_slot:
        return 10
    return 5


def calculate_conflicts(schedule):
    conflicts = 0
    time_room_usage = {}
    time_professor_usage = {}

    for (section, subject, professor, time_slot, room) in schedule:
        if (time_slot, room) in time_room_usage:
            conflicts += 1
        else:
            time_room_usage[(time_slot, room)] = True

        if (time_slot, professor) in time_professor_usage:
            conflicts += 1
        else:
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
    for i in range(len(particle.position)):
        r1 = random.random()
        r2 = random.random()

        pos_num = convert_to_numeric(particle.position[i])
        pBest_num = convert_to_numeric(particle.pBest[i])
        gBest_num = convert_to_numeric(gBest[i])

        cognitive = c1 * r1 * (pBest_num - pos_num)
        social = c2 * r2 * (gBest_num - pos_num)

        new_velocity.append(w * (particle.velocity[i] if particle.velocity else 0) + cognitive + social)
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
        #print(f"Current Position[{i}]: {current_pos}")  # Debug statement

        current_pos_num = convert_to_numeric(current_pos)
        #print(f"Current Numeric Position[{i}]: {current_pos_num}")  # Debug statement

        new_pos_num = round(current_pos_num + particle.velocity[i])
        #print(f"New Numeric Position[{i}] before modulo: {new_pos_num}")  # Debug statement

        new_pos_num = new_pos_num % len(num_to_position)
        #print(f"New Numeric Position[{i}] after modulo: {new_pos_num}")  # Debug statement

        new_pos = convert_from_numeric(new_pos_num)
        #print(f"New Position[{i}]: {new_pos}")  # Debug statement

        validated_pos = validate_position(new_pos)
        #print(f"Validated Position[{i}]: {validated_pos}")  # Debug statement

        if validated_pos:
            new_position.append(validated_pos)
        else:
            #print(f"Invalid position detected at index {i}, skipping update.")
            new_position.append(current_pos)  # Keep the current position if new position is invalid

    #print(f"Updated Position: {new_position}")  # Debug statement
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


'''def validate_position(position):
    """
    Validate the position to ensure there are no double bookings and double subjects.

    Parameters:
    position (list of tuples): A list where each tuple represents a scheduled event,
                               formatted as (section, subject, professor, time_slot, room).

    Returns:
    list or bool: The validated position if there are no double bookings and double subjects, False otherwise.
    """
    if not isinstance(position, list):
        print("Error: Position is not a list.")
        return False

    professor_schedule = defaultdict(set)
    room_schedule = defaultdict(set)
    section_subjects = defaultdict(set)

    for event in position:
        section, subject, professor, time_slot, room = event

        # Check for double booking for professors
        if professor in professor_schedule and time_slot in professor_schedule[professor]:
            print(f"Double booking detected for professor {professor} at {time_slot}")
            return False
        professor_schedule[professor].add(time_slot)

        # Check for double booking for rooms
        if room in room_schedule and time_slot in room_schedule[room]:
            print(f"Double booking detected for room {room} at {time_slot}")
            return False
        room_schedule[room].add(time_slot)

        # Check for double subjects per section
        if subject in section_subjects[section]:
            print(f"Double subject {subject} detected in section {section}")
            return False
        section_subjects[section].add(subject)

    return position'''

def validate_position(position):
    # Validate the position (e.g., no double-booking)
    return position






def group_schedule_by_section(schedule):
    grouped_schedule = defaultdict(list)
    for entry in schedule:
        section = entry[0]
        grouped_schedule[section].append(entry)
    return grouped_schedule


def main():
    # Initialize swarm
    swarm = initialize_swarm(swarm_size, sections, subjects, professors, time_slots, rooms)
    gBest = None
    gBest_fitness = float('-inf')
    n = 0

    # Evaluate initial fitness
    for particle in swarm:
        particle.fitness = calculate_fitness(particle.position)
        particle.pBest = particle.position
        particle.pBest_fitness = particle.fitness
        if particle.fitness > gBest_fitness:
            gBest = particle.position
            gBest_fitness = particle.fitness

    # Iterate
    for iteration in range(max_iterations):
        for particle in swarm:
            particle.velocity = update_velocity(particle, gBest, w, c1, c2)
            particle.position = update_position(particle)
            particle.position = validate_position(particle.position)
            particle.fitness = calculate_fitness(particle.position)
            #if false maintain the current sched and skip the update.
            #else, update the sched and calculate the fitness

            if particle.fitness > particle.pBest_fitness:
                particle.pBest = particle.position
                particle.pBest_fitness = particle.fitness

            if particle.fitness > gBest_fitness:
                gBest = particle.position
                gBest_fitness = particle.fitness



    # The gBest now holds the best found schedule
    # This print statement is for the division per section of the overall schedule
    n = 0
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

if __name__ == '__main__':
    main()

