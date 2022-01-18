# Export-2-Strava

Import **FitNotes** workout data to Strava.

Import **Adidas** workouts to Strava.




## Export Adidas/Runtastic workout data
1. Navigate to `https://www.runtastic.com/` and log in
2. Go to the settings and export your data. Note that you may have to wait a couple of days before your data is available

## Export FitNotes workout data
Follow instructions from https://www.fitnotesapp.com/settings/#data

## Strava authentication

1. Create an application in your personal Strava account
2. Get your Strava code to allow the script to request tokens to the Strava API
   1. With your Strava client id, navigate to: http<span>:</span>//www<span>.</span>strava.com/oauth/authorize?client-id=<b><client_id></b>&response_type=code&redirect_uri=http<span>:</span>//localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all,activity:write
   2. Go through the consent form
   3. From the url, copy the code to your config.json
3. Fill in the config.json file with your client Id, client secret and the path to your adidas folder workout e.g. C:/<user_root>/2020-06-23/Sport-sessions/ and or your FitNotes exported csv data.
4. Run `python .\sports_app_importer.py`. Follow the prompt's instructions.

> Notes
>
> * You can modify the [scopes](https://developers.strava.com/docs/authentication/#detailsaboutrequestingaccess) requested in the url if you need different access.
> * [Strava API doc reference](https://developers.strava.com/docs/reference/)
> * Only 2 apps are supported: FitNotes (https://play.google.com/store/apps/details?id=com.github.jamesgay.fitnotes) and Adidas (https://play.google.com/store/apps/details?id=com.runtastic.android.results.lite)
