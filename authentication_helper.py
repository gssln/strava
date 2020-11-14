import requests
import json
import time

code = ""
client_id = ""
client_secret = ""
token_file_name = "strava_token.json"

def configure_strava(configs):
    global client_id, client_secret, code
    client_id = configs["config"]["strava_client_id"]
    client_secret = configs["config"]["strava_client_secret"]
    code = configs["config"]["strava_code"]
    return
    

def get_strava_token(code):
    if not client_id or not client_secret or not code:
        print("Strava authentication is not properly configured.")
        return None

    response = requests.post(
        url = 'https://www.strava.com/oauth/token',
        data = {
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code,
                'grant_type': 'authorization_code'
            }
    )

    return response

def get_strava_refresh_token(refresh_token):
    if not client_id or not client_secret:
        print("Strava authentication is not properly configured.")
        return None

    print("Acquire token with: " + refresh_token)
    response = requests.post(
    url = 'https://www.strava.com/oauth/token',
    data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
    )

    return response

def save_token_to_file(token):
    with open(token_file_name, 'w') as outfile:
        json.dump(token, outfile)

def get_token_from_file():
    strava_token = None
    try:
        with open(token_file_name) as json_file:
            strava_token = json.load(json_file)
    except FileNotFoundError:
        print("No token file found.")

    return strava_token

def is_token_expired(token):
    return token['expires_at'] < time.time()

def get_token():
    if not client_id or not client_secret or not code:
        print("Strava authentication is not properly configured.")
        return None

    token = get_token_from_file()

    if token is None:
        print("File does not contain token or does not exists.")
        response = get_strava_token(code)

        if response.ok:
            print("Token was acquired with code.")
            save_token_to_file(response.json())
            return response.json()
        else:
            print("There was a problem acquiring a refresh token.")
            response.raise_for_status()
    elif is_token_expired(token):
        print("Token is expired.")
        response = get_strava_refresh_token(token['refresh_token'])
        
        if response.ok:
            print("Refresh token acquired.")
            save_token_to_file(response.json())
            return response.json()
        else:
            print("There was a problem acquiring a refresh token.")
            response.raise_for_status()
    else:
        print("Token was retrieved from file.")
        return token