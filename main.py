import random

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
    # Add more professors as needed
}

subjects = {
    1: ['CS101', 'CS102'],
    2: ['CS201', 'CS202'],
    3: ['CS301'],
    4: ['CS401']
}

rooms = ['Room 101', 'Room 102', 'Room 103']
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
            for subject in subjects[year]:
                available_professors = [prof for prof in professors if subject in professors[prof][
                    'preferred_subjects'] and prof not in assigned_subjects]
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
    new_position = []
    for i in range(len(particle.position)):
        new_pos_num = round(convert_to_numeric(particle.position[i]) + particle.velocity[i])
        new_pos_num = new_pos_num % len(num_to_position)  # Ensure new_pos_num is a valid key
        new_pos = convert_from_numeric(new_pos_num)
        new_position.append(validate_position(new_pos))
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
    # Validate the position (e.g., no double-booking)
    return position


# Initialize swarm
swarm = initialize_swarm(swarm_size, sections, subjects, professors, time_slots, rooms)
gBest = None
gBest_fitness = float('-inf')

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

        if particle.fitness > particle.pBest_fitness:
            particle.pBest = particle.position
            particle.pBest_fitness = particle.fitness

        if particle.fitness > gBest_fitness:
            gBest = particle.position
            gBest_fitness = particle.fitness

# The gBest now holds the best found schedule
print("Optimized Schedule:\n" + '\n'.join(map(str, gBest)))
print("Fitness Score:", gBest_fitness)
