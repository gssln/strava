import json
import os
from activities.adidas_activity import AdidasActivity

def get_adidas_activities(folder : str) -> list:
    all_activity_files = get_files_from_folder(folder)

    adidas_activities = []
    for index, activity_file in enumerate(all_activity_files):
        print("{}/{}\tProcessing activity: {}".format(index + 1,
              len(all_activity_files), activity_file))
        (file_id, data) = read_from_file(folder, activity_file)
        adidas_act = create_adidas_activity_from_file(file_id, data)

        if adidas_act is None:
            print("\tError while processing activity. Skipping ...")
            continue

        adidas_activities.append(adidas_act)

    return adidas_activities


def get_files_from_folder(folder):
    print("Reading folder: {}".format(folder))
    activity_files = os.listdir(folder)
    print("{} activity files found\n".format(len(activity_files)))
    return activity_files

def read_from_file(folder, file_name):
    with open(folder + file_name) as read_file:
        data = json.load(read_file)

    file_id = file_name.split('\\')[-1]
    return (file_id, data)

def create_adidas_activity_from_file(file_id, data):
    try:
        if 'current_training_plan_state' in data:
            activity = AdidasActivity(
                file_id,
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
            activity = AdidasActivity(
                file_id,
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
