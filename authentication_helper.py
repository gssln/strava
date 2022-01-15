import json
import time
import requests

class StravaAuth:
    def __init__(self):
        self.code = ''
        self.client_id = ''
        self.client_secret = ''
        self.token_file_name = 'strava_token.json'

    def configure_strava(self, configs):
        self.client_id = configs["config"]["strava_client_id"]
        self.client_secret = configs["config"]["strava_client_secret"]
        self.code = configs["config"]["strava_code"]
        return


    def get_strava_token(self):
        if not self.client_id or not self.client_secret or not self.code:
            print("Strava authentication is not properly configured.")
            return None

        response = requests.post(
            url = 'https://www.strava.com/oauth/token',
            data = {
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'code': self.code,
                    'grant_type': 'authorization_code'
                }
        )

        return response

    def get_strava_refresh_token(self, refresh_token):
        if not self.client_id or not self.client_secret:
            print("Strava authentication is not properly configured.")
            return None

        print("Acquire token with: " + refresh_token)
        response = requests.post(
        url = 'https://www.strava.com/oauth/token',
        data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
        )

        return response

    def save_token_to_file(self, token):
        with open(self.token_file_name, 'w') as outfile:
            json.dump(token, outfile)

    def get_token_from_file(self):
        strava_token = None
        try:
            with open(self.token_file_name) as json_file:
                strava_token = json.load(json_file)
        except FileNotFoundError:
            print("No token file found.")

        return strava_token

    def is_token_expired(self, token):
        return token['expires_at'] < time.time()

    def get_token(self):
        if not self.client_id or not self.client_secret or not self.code:
            print("Strava authentication is not properly configured.")
            return None

        token = self.get_token_from_file()

        if token is None:
            print("File does not contain token or does not exists.")
            response = self.get_strava_token()

            if response.ok:
                print("Token was acquired with code.")
                self.save_token_to_file(response.json())
                return response.json()
            else:
                print("There was a problem acquiring a refresh token.")
                response.raise_for_status()
        elif self.is_token_expired(token):
            print("Token is expired.")
            response = self.get_strava_refresh_token(token['refresh_token'])

            if response.ok:
                print("Refresh token acquired.")
                self.save_token_to_file(response.json())
                return response.json()
            else:
                print("There was a problem acquiring a refresh token.")
                response.raise_for_status()
        else:
            print("Token was retrieved from file.")
            return token
