import datetime
from activities.strava_activity import StravaActivity

class AdidasActivity:
    def __init__(self, file_id, start_time, end_time, calories, exercises, plan_name,
                 day_nb, week_nb, nb_workout_per_week, subjective_intensity):
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

    def convert_to_strava_activity(self) -> StravaActivity:
        return StravaActivity(
            self.format_name(),
            "Workout",
            self.start_time.isoformat(),
            (self.end_time - self.start_time).seconds,
            self.format_description()
        )


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
        for key, value in exercise_dict.items():
            exercise_str = exercise_str + "{} x {} {}\n".format(key.replace('_',' ')
            .capitalize(), value[0], value[1])

        return exercise_str

    def format_description(self):
        return "Calories: {} - Perceived intensity: {}\n\n{}".format(
            self.calories, self.subjective_intensity, self.extract_exercises_string())

    def format_name(self):
        if self.week_nb is None and self.day_nb is None and self.nb_workout_per_week is None:
            return "Adidas {} workout".format(self.plan_name.replace('_',' ').capitalize())
        else:
            return "Adidas {} -- Week {} : Day {}/{}".format(self.plan_name.replace('_',' ')
            .capitalize(), self.week_nb, self.day_nb, self.nb_workout_per_week)

    def print(self):
        print("Start time: {}".format(self.start_time.isoformat())) # epoch to ISO8601
        print("End time: {}".format(self.end_time.isoformat())) # epoch to ISO8601
        print("Duration: {}".format((self.end_time - self.start_time).seconds))
        print(self.format_description())

    def convert_time_to_iso8601(self, epoch_time):
        return datetime.datetime.fromtimestamp(epoch_time)
