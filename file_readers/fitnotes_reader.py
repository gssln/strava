import csv
import os
from activities.fitnotes_activity import FitNotesActivity

def get_fitnotes_activities(folder : str) -> list:
    fitnotes_activities = create_from_file(folder)

    return fitnotes_activities

def create_from_file(folder):
    all_files = os.listdir(folder)

    if len(all_files) == 1:
        filename = all_files[0]
    else:
        print("More than 1 valid file in the folder.")
        return None


    with open(folder + filename, mode='r') as csv_file:
        csv_data = csv.DictReader(csv_file)

        fitnotes_activities = []
        date = ''
        for exercise_line in csv_data:
            if date != exercise_line.get('Date'):
                # New activity
                date = exercise_line.get('Date')
                fitness_act = FitNotesActivity(date)
                fitnotes_activities.append(fitness_act)

            if fitness_act is None:
                print("\tError while processing activity. Skipping ...")
                continue

            fitness_act.add_exercise(exercise_line)


    return fitnotes_activities
