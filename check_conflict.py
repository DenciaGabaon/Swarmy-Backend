import json

def check_conflicts(data):
  """
  Checks for conflicting schedules in the given data.

  Args:
    data: A list of tuples, where each tuple represents a class with the following format:
      (section, course, professor, day,  room)

  Returns:
    A list of tuples containing conflicting classes (section, course, professor)
  """
  conflicts = []
  for i, class1 in enumerate(data):
    for j, class2 in enumerate(data):
      if i != j and ((class1[2] == class2[2] and class1[3] == class2[3]) or (
              class1[3] == class2[3] and class1[4] == class2[4])):
        print(f"Conflict found between \n{class1[0]} {class1[1]} {class1[2]} {class1[3]} {class1[4]}\n and \n{class2[0]} {class2[1]} {class2[2]} {class2[3]} {class2[4]}\n")
        conflicts.append((class1[0], class1[1], class1[2], class1[3], class1[4]))
        conflicts.append((class2[0], class2[1], class2[2], class2[3], class2[4]))
  return conflicts

def main():
  # Load data from JSON file
  with open('schedule.json', 'r') as f:
      json_data = json.load(f)
  data = []

  for section, entries in json_data.items():
      for entry in entries:
          data.append(tuple(entry))
  #print(data[1])
  check_conflicts(data)
  if check_conflicts(data) == []:
    print("No conflicts found.")


if __name__ == '__main__':
  main()