# Adidas2Strava importer
Import Adidas workouts to Strava using Adidas exported data.

## Strava authentication
1. Create an application in your personal Strava account
2. Get your Strava code to allow the script to request tokens to the Strava API
   1. With your Strava client id, navigate to: http<span>:</span>//www<span>.<span>strava.com/oauth/authorize?client_id=<b><client_id></b>&response_type=code&redirect_uri=http<span>:</span>//localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all,activity:write
   2. Go through the consent form
   3. From the url, copy the code to your config.json
3. Fill in the config.json file with your client Id, client secret and the path to your adidas folder workout e.g. C:/<user_root>/2020-06-23/Sport-sessions/
4. Run `python adidas_importer.py`


> Notes
>
> * You can modify the [scopes](https://developers.strava.com/docs/authentication/#detailsaboutrequestingaccess) requested in the url if you need different access.
> * [Strava API doc reference](https://developers.strava.com/docs/reference/)
