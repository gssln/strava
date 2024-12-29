import json
import os
from activities.adidas_activity import AdidasActivity

def get_adidas_activities(folder: str) -> list:
    activity_files = [f for f in os.listdir(folder) if f.endswith('.json')]
    print(f"{len(activity_files)} activity files found\n")

    adidas_activities = []
    for index, activity_file in enumerate(activity_files):
        print(f"{index + 1}/{len(activity_files)}\tProcessing activity: {activity_file}")
        try:
            (file_id, data) = read_from_file(folder, activity_file)
            adidas_act = create_adidas_activity_from_file(file_id, data)

            if adidas_act is None:
                print("\tError while processing activity. Skipping ...")
                continue

            adidas_activities.append(adidas_act)
        except IsADirectoryError:
            print(f"\tSkipping directory: {activity_file}")
        except Exception as e:
            print(f"\tError processing file: {e}")

    return adidas_activities

def read_from_file(folder, file_name):
    with open(os.path.join(folder, file_name)) as read_file:
        data = json.load(read_file)
    return (file_name, data)

def create_adidas_activity_from_file(file_id, data):
    try:
        activity = AdidasActivity(
            file_id,
            data['start_time'],
            data['end_time'],
            data.get('calories', 0),
            data.get('features', []),
            data.get('sport_type_id', 'unknown'),
            data.get('duration', 0)
        )
    except KeyError as exception:
        print(f"\tKey error - Reason: {exception}")
        return None

    return activity