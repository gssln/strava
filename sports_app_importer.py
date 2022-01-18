import json
import os
import requests
from termcolor import colored
from file_readers.adidas_reader import get_adidas_activities
from file_readers.fitnotes_reader import get_fitnotes_activities
from helpers.authentication_helper import StravaAuth

def adidas2strava(token, adidas_folder):
    all_adidas_activities = get_adidas_activities(adidas_folder)

    for adidas_act in all_adidas_activities:
        strava_act = adidas_act.convert_to_strava_activity()
        upload_to_strava(token, strava_act)


def fitnotes2strava(token, fitnotes_folder):
    all_fitnotes_activities = get_fitnotes_activities(fitnotes_folder)

    for fitnotes_act in all_fitnotes_activities:
        strava_act = fitnotes_act.convert_to_strava_activity()
        upload_to_strava(token, strava_act)



def upload_to_strava(token, activity):
    params = activity.__dict__
    params['access_token'] = token

    ### Create activity
    response = requests.post(
        url = URL,
        params = params
    )

    detailed_activity = json.loads(response.text)

    if response.status_code == 201:
        print(colored("\tActivity was created successfully. Strava activity id: {}\n", "green")
            .format(detailed_activity['id']))
    elif response.status_code == 409:
        print(colored("\tActivity already exists in Strava. Skipping ...\n", "yellow"))
    else:
        print(colored("\tThere was a problem creating an activity.\n", "red"))


####### Get strava code to fetch token
# 1. http://www.strava.com/oauth/authorize?client_id=55268&response_type=code&redirect_uri=
#       http://localhost/exchange_token&approval_prompt=force
#       &scope=profile:read_all,activity:read_all,activity:write"
# 2. Authorize
URL = "https://www.strava.com/api/v3/activities"

# Load configurations
with open("config.json") as config_file:
    configs = json.load(config_file)

# Setup authentication
auth = StravaAuth()
auth.configure_strava(configs)


# Get access token for strava
access_token = auth.get_token()['access_token']

os.system('color')

# Get user input
print('-' * 60)
print('STRAVA IMPORTER TOOL')
print('\t> Import unsupported sports app data to Strava.')
print('-' * 60)
print('')

print('1. Adidas')
print('\t> Exported workout data (keep original folder structure)')
print('2. FitNotes')
print('\t > Exported workout data (as CSV)')
print('')

user_choice = input('Which app data needs to be imported to Strava?\n')

if user_choice == '1':
    folder = configs["config"]["adidas_workout_folder"]
    adidas2strava(access_token, folder)
elif user_choice == '2':
    folder = configs["config"]["fitnotes_export_folder"]
    fitnotes2strava(access_token, folder)
