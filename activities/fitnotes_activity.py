from datetime import datetime
from activities.strava_activity import StravaActivity


class FitNotesActivity:
    def __init__(self, date):
        self.date = date
        self.workout_data = WorkoutData()

    def convert_to_strava_activity(self) -> StravaActivity:
        return StravaActivity(
            self.format_name(),
            "Workout",
            datetime.strptime(self.date, '%Y-%m-%d').isoformat(),
            90*60, # 90 minutes * 60 seconds/minutes
            self.format_description()
        )

    def add_exercise(self, exercise_data):
        self.workout_data.add_exercise(exercise_data)

    def format_name(self):
        return 'Gym Workout'

    def format_description(self):
        return self.workout_data.get_str_description()

class WorkoutData:
    def __init__(self):
        self.exercises = {}

    def add_exercise(self, exercise_data):
        new_set = Set(weight=exercise_data.get('Weight (lbs)'),
                      reps=exercise_data.get('Reps'),
                      time = exercise_data.get('Time'))

        name = exercise_data.get('Exercise')
        if name not in self.exercises:
            self.exercises[name] = Exercise(name, exercise_data.get('Category'))

        self.exercises[name].add_set(new_set)

    def get_str_description(self):
        description = ''
        for e in self.exercises.values():
            description += e.get_description()

        return description

class Set:
    def __init__(self, weight = 0, reps = 0, time = 0):
        self.weight = weight
        self.reps = reps
        self.time = time

class Exercise:
    def __init__(self, name, category):
        self.exercise_name = name
        self.category = category
        self.sets = []

    def add_set(self, new_set : Set):
        self.sets.append(new_set)

    def get_description(self) -> str:
        descr = f'{self.exercise_name.upper()}  --> {self.category}\n'

        sets_str = ''
        for s in self.sets:
            if s.time != 0:
                sets_str += f'{s.reps} x {s.weight} lbs\n'
            else:
                sets_str += f'{s.reps} x {s.time} seconds\n'

        return f'{descr}{sets_str}\n'
