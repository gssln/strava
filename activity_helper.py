import datetime
import json
import os

def get_files_from_folder(folder):
    print("Reading folder: {}".format(folder))
    activity_files = os.listdir(folder)
    print("{} activity files found\n".format(len(activity_files)))
    return activity_files

def read_from_file(folder, file_name):
    with open(folder + file_name) as read_file:
        data = json.load(read_file)
    
    id = file_name.split('\\')[-1]
    return (id, data)

def transform_adidas_activity_to_strava_activity(adidas_act):
    strava_act = strava_activity(
        adidas_act.format_name(),
        "Workout",
        adidas_act.start_time.isoformat(),
        (adidas_act.end_time - adidas_act.start_time).seconds,
        adidas_act.format_description(),
        0.0,
        0,
        0
    )

    return strava_act

def create_adidas_activity(id, data):
    try:
        if 'current_training_plan_state' in data:
            activity = adidas_activity(
                id,
                data['start_time'] / 1000,
                data['end_time'] / 1000,
                data['calories'],
                data['workout_data']['exercises'],
                data['current_training_plan_state']['training_plan_type'],
                data['current_training_plan_state']['day'],
                data['current_training_plan_state']['week'],
                data['current_training_plan_state']['days_per_week'],
                data['subjective_intensity'] if 'subjective_intensity' in data else None
            )
        else:
            activity = adidas_activity(
                id,
                data['start_time'] / 1000,
                data['end_time'] / 1000,
                data['calories'],
                data['workout_data']['exercises'],
                data['workout_data']['workout_id'],
                None,
                None,
                None,
                data['subjective_intensity'] if 'subjective_intensity' in data else None
            )
    except KeyError as exception:
        print("\tKey error - Reason: {}".format(exception))
        return None

    return activity

class strava_activity:
    def __init__(self, name, activity_type, start_date_local, elapsed_time, description, distance, trainer, commute):
        self.name = name
        self.type = activity_type
        self.start_date_local = start_date_local
        self.elapsed_time = elapsed_time
        self.description = description
        self.distance = distance
        self.trainer = trainer
        self.commute = commute

    def print(self):
        print(self.name)
        print(self.type)
        print(self.start_date_local)
        print(self.elapsed_time)
        print(self.description)
        print(self.distance)
        print(self.trainer)
        print(self.commute)

class adidas_activity:
    def __init__(self, file_id, start_time, end_time, calories, exercises, plan_name, day_nb, week_nb, nb_workout_per_week, subjective_intensity):
        self.file_id = file_id
        self.start_time = self.convert_time_to_iso8601(start_time)
        self.end_time = self.convert_time_to_iso8601(end_time)
        self.calories = calories
        self.exercises = exercises
        self.plan_name = plan_name
        self.day_nb = day_nb
        self.week_nb = week_nb
        self.nb_workout_per_week = nb_workout_per_week
        self.subjective_intensity = subjective_intensity

    def extract_exercises_string(self):
        exercise_dict = {}
        
        # Summarize exercises
        for ex in self.exercises:
            k = ex['exercise_id']
            
            if 'repetitions' in ex.keys():
                count = (ex['repetitions'], "reps")
            elif 'target_duration' in ex.keys():
                count = (int(ex['target_duration'] / 1000), "sec")
                
            if k in exercise_dict:
                exercise_dict[k] = (exercise_dict[k][0] + count[0], count[1])
            else:
                exercise_dict[k] = count
        
        exercise_str = ""
        for k,v in exercise_dict.items():
             exercise_str = exercise_str + "{} x {} {}\n".format(k.replace('_',' ').capitalize(), v[0], v[1])
        
        return exercise_str
    
    def format_description(self):
        return "Calories: {} - Perceived intensity: {}\n\n{}".format(
            self.calories, self.subjective_intensity, self.extract_exercises_string())

    def format_name(self):
        if self.week_nb == None and self.day_nb == None and self.nb_workout_per_week == None:
            return "Adidas {} workout".format(self.plan_name.replace('_',' ').capitalize())
        else: 
            return "Adidas {} -- Week {} : Day {}/{}".format(self.plan_name.replace('_',' ').capitalize(), self.week_nb, self.day_nb, self.nb_workout_per_week)

    def print(self):
        print("Start time: {}".format(self.start_time.isoformat())) # epoch to ISO8601
        print("End time: {}".format(self.end_time.isoformat())) # epoch to ISO8601
        print("Duration: {}".format((self.end_time - self.start_time).seconds))
        print(self.format_description())

    def convert_time_to_iso8601(self, epoch_time):
        return datetime.datetime.fromtimestamp(epoch_time)
