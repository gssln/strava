import datetime
from activities.strava_activity import StravaActivity

class AdidasActivity:
    def __init__(self, file_id, start_time, end_time, calories, features, sport_type_id, duration):
        self.file_id = file_id
        self.start_time = datetime.datetime.fromtimestamp(start_time / 1000)  # Convert from milliseconds
        self.end_time = datetime.datetime.fromtimestamp(end_time / 1000)
        self.calories = calories
        self.features = features
        self.sport_type_id = sport_type_id
        self.duration = duration

    def convert_to_strava_activity(self) -> StravaActivity:
        # Get metrics from features
        track_metrics = next((f for f in self.features if f['type'] == 'track_metrics'), None)
        weather = next((f for f in self.features if f['type'] == 'weather'), None)
        
        # Determine activity type based on sport_type_id
        activity_type = self.get_activity_type()
        
        # Format description with available data
        description = self.format_description(track_metrics, weather)

        return StravaActivity(
            self.format_name(track_metrics),
            activity_type,
            self.start_time.isoformat(),
            int(self.duration / 1000),  # Convert from milliseconds to seconds
            description
        )

    def get_activity_type(self):
        # Map Runtastic sport types to Strava types
        # You might need to adjust these mappings
        sport_type_mapping = {
            "1": "Run",
            "2": "Ride",
            # Add more mappings as needed
        }
        return sport_type_mapping.get(self.sport_type_id, "Other")

    def format_description(self, track_metrics, weather):
        description = f"Calories: {self.calories}\n"
        
        if track_metrics:
            attrs = track_metrics['attributes']
            description += f"Distance: {attrs.get('distance', 0)}m\n"
            description += f"Elevation gain: {attrs.get('elevation_gain', 0)}m\n"
            
        if weather:
            attrs = weather['attributes']
            description += f"\nWeather: {attrs.get('conditions', 'unknown')}\n"
            description += f"Temperature: {attrs.get('temperature', 0)}°C\n"
            
        return description

    def format_name(self, track_metrics):
        if track_metrics:
            distance_km = track_metrics['attributes'].get('distance', 0) / 1000
            return f"{self.get_activity_type()} - {distance_km:.2f}km"
        return f"{self.get_activity_type()}"