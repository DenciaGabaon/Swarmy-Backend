import numpy as np

# Constants
w = 0.5  # inertia
c1 = 1.5  # cognitive component
c2 = 1.5  # social component
num_particles = 30  # number of particles in the swarm
num_iterations = 100  # number of iterations
num_classes = 36  # total number of classes to schedule
num_rooms = 6
num_professors = 16  # total number of professors
time_slots_per_day = 10  # assume 10 time slots (hours) available per day
days_per_week = 5  # number of days per week
total_time_slots = time_slots_per_day * days_per_week  # total time slots in a week
lec_duration = 1  # duration of a lecture in hours
lab_duration = 3  # duration of a lab in hours
max_professor_hours = 33  # maximum hours a professor can teach

# Example professor availability (1 means available, 0 means not available)
professor_availability = np.random.randint(0, 2, (num_professors, total_time_slots))

# Predefined class types (0 for lecture, 1 for lab)
class_types = np.array([0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1,
                        0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0])


def initialize_particles():
    particles = np.random.randint(0, total_time_slots, (num_particles, num_classes, 4))  # Time assignment
    particles[:, :, 1] = np.random.randint(0, num_rooms, (num_particles, num_classes))  # Room assignment
    particles[:, :, 2] = np.random.randint(0, num_professors, (num_particles, num_classes))  # Professor assignment
    particles[:, :, 3] = class_types  # Class type (lec or lab)
    velocities = np.random.rand(num_particles, num_classes, 4)  # velocities
    return particles, velocities


def fitness_function(schedule):
    penalty = 0
    class_times = schedule[:, 0]
    class_rooms = schedule[:, 1]
    class_professors = schedule[:, 2]
    class_types = schedule[:, 3]

    # Track professor hours
    professor_hours = np.zeros(num_professors)

    for i in range(len(schedule)):
        duration_i = lec_duration if class_types[i] == 0 else lab_duration
        professor_hours[int(class_professors[i])] += duration_i  # Increment professor hours
        for j in range(i + 1, len(schedule)):
            duration_j = lec_duration if class_types[j] == 0 else lab_duration
            # Check room conflict
            if class_rooms[i] == class_rooms[j] and max(0, min(class_times[i] + duration_i,
                                                               class_times[j] + duration_j) - max(class_times[i],
                                                                                                  class_times[j])) > 0:
                penalty += 1
            # Check professor conflict
            if class_professors[i] == class_professors[j] and max(0, min(class_times[i] + duration_i,
                                                                         class_times[j] + duration_j) - max(
                    class_times[i], class_times[j])) > 0:
                penalty += 1
            # Check professor availability
            for t in range(duration_i):
                if class_times[i] + t < total_time_slots and professor_availability[
                    int(class_professors[i]), int(class_times[i]) + t] == 0:
                    penalty += 1
            for t in range(duration_j):
                if class_times[j] + t < total_time_slots and professor_availability[
                    int(class_professors[j]), int(class_times[j]) + t] == 0:
                    penalty += 1

    # Add penalty for exceeding maximum professor hours
    penalty += np.sum(professor_hours[professor_hours > max_professor_hours])

    return penalty


def update_particles(particles, velocities, personal_best_positions, global_best_position):
    for i in range(num_particles):
        r1, r2 = np.random.rand(), np.random.rand()
        velocities[i] = (w * velocities[i]
                         + c1 * r1 * (personal_best_positions[i] - particles[i])
                         + c2 * r2 * (global_best_position - particles[i]))
        particles[i] = np.round(particles[i] + velocities[i]).astype(int)

        # Ensure the particles stay within valid bounds
        particles[i][:, 0] = particles[i][:, 0] % total_time_slots  # Time slots
        particles[i][:, 1] = particles[i][:, 1] % num_rooms  # Room assignments
        particles[i][:, 2] = particles[i][:, 2] % num_professors  # Professor assignments
        particles[i][:, 3] = class_types  # Class types remain unchanged

    return particles, velocities


def pso():
    particles, velocities = initialize_particles()
    personal_best_positions = particles.copy()
    personal_best_fitness = np.array([fitness_function(p) for p in particles])
    global_best_position = personal_best_positions[np.argmin(personal_best_fitness)]
    global_best_fitness = min(personal_best_fitness)

    for _ in range(num_iterations):
        for i in range(num_particles):
            fitness = fitness_function(particles[i])
            if fitness < personal_best_fitness[i]:
                personal_best_fitness[i] = fitness
                personal_best_positions[i] = particles[i]
            if fitness < global_best_fitness:
                global_best_fitness = fitness
                global_best_position = particles[i]

        particles, velocities = update_particles(particles, velocities, personal_best_positions, global_best_position)

    return global_best_position


def format_schedule(schedule):
    formatted_schedule = []
    for cls in schedule:
        time_slot, room, professor, class_type = cls
        class_type_str = "Lec" if class_type == 0 else "Lab"
        formatted_schedule.append(f"Class: {class_type_str}, Time Slot {time_slot}, Room {room}, Professor {professor}")
    return formatted_schedule


def verify_schedule(schedule):
    penalty = 0
    class_times = schedule[:, 0]
    class_rooms = schedule[:, 1]
    class_professors = schedule[:, 2]
    class_types = schedule[:, 3]

    for i in range(len(schedule)):
        duration_i = lec_duration if class_types[i] == 0 else lab_duration
        for j in range(i + 1, len(schedule)):
            duration_j = lec_duration if class_types[j] == 0 else lab_duration

            # Check for room conflict
            if class_rooms[i] == class_rooms[j] and max(0, min(class_times[i] + duration_i,
                                                               class_times[j] + duration_j) - max(class_times[i],
                                                                                                  class_times[j])) > 0:
                print(f"Conflict: Room conflict between class {i} and class {j}")
                penalty += 1

            # Check for professor conflict
            if class_professors[i] == class_professors[j] and max(0, min(class_times[i] + duration_i,
                                                                         class_times[j] + duration_j) - max(
                    class_times[i], class_times[j])) > 0:
                print(f"Conflict: Professor conflict between class {i} and class {j}")
                penalty += 1

            # Check for overlapping professor hours
            if class_professors[i] == class_professors[j] and max(class_times[i], class_times[j]) < min(
                    class_times[i] + duration_i, class_times[j] + duration_j):
                print(
                    f"Conflict: Overlapping hours for professor {class_professors[i]} between class {i} and class {j}")
                penalty += 1

            # Check for professor availability
            for t in range(duration_i):
                if class_times[i] + t < total_time_slots and professor_availability[
                    int(class_professors[i]), int(class_times[i]) + t] == 0:
                    print(
                        f"Conflict: Professor {class_professors[i]} not available at time slot {class_times[i] + t} for class {i}")
                    penalty += 1
            for t in range(duration_j):
                if class_times[j] + t < total_time_slots and professor_availability[
                    int(class_professors[j]), int(class_times[j]) + t] == 0:
                    print(
                        f"Conflict: Professor {class_professors[j]} not available at time slot {class_times[j] + t} for class {j}")
                    penalty += 1

    return penalty


def main():
    optimal_schedule = pso()
    formatted_schedule = format_schedule(optimal_schedule)
    print("Optimal Schedule:")
    for entry in formatted_schedule:
        print(entry)
    penalty = verify_schedule(optimal_schedule)
    print(f"Total Penalty: {penalty}")

if __name__ == "__main__":
    main()
