"""Module for a Strava activity"""

class StravaActivity:
    """ Represents a Strava activity"""

    def __init__(self, name, activity_type, start_date_local, elapsed_time, description):
        """ Initializes a strava activity

        Args:
            name (str): The name of the activity.
            activity_type (str): Type of activity. For example - Run, Ride etc.
            start_date_local (Date): ISO 8601 formatted date time.
            elapsed_time (Int): In seconds
            description (str): Description of the activity.
        """
        self.name = name
        self.type = activity_type
        self.start_date_local = start_date_local
        self.elapsed_time = elapsed_time
        self.description = description

    def print(self):
        print(self.name)
        print(self.type)
        print(self.start_date_local)
        print(self.elapsed_time)
        print(self.description)
