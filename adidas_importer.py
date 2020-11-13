import requests
import json
import os
from termcolor import colored
import authentication_helper as auth
import activity_helper

####### Get strava code to fetch token
# 1. http://www.strava.com/oauth/authorize?client_id=55268&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all,activity:write"
# 2. Authorize

url = "https://www.strava.com/api/v3/activities"
code = ""
folder = ""

### Get access token for strava
access_token = auth.get_token(code)['access_token']
os.system('color')
all_activities = activity_helper.get_files_from_folder(folder)

for index, activity_file in enumerate(all_activities):
    print("{}/{}\tProcessing file: {}".format(index + 1, len(all_activities), activity_file))
    (file_id, data) = activity_helper.read_from_file(folder, activity_file)
    adidas_act = activity_helper.create_adidas_activity(file_id, data)

    if adidas_act is None:
        print(colored("\tActivity was skipped ...", "blue"))
        continue

    strava_act = activity_helper.transform_adidas_activity_to_strava_activity(adidas_act)

    params = strava_act.__dict__
    params['access_token'] = access_token

    ### Create activity
    response = requests.post(
        url = url,
        params = params
    )

    detailed_activity = json.loads(response.text)

    if response.status_code == 201:
        print(colored("\tActivity was created successfully. Strava activity id: {}\n", "green").format(detailed_activity['id']))
    elif response.status_code == 409:
        print(colored("\tActivity already exists in Strava. Skipping ...\n", "yellow"))
    else:
        print(colored("\tThere was a problem creating an activity.\n", "red"))