"""
Weather Agent

This agent fetches current weather information using the Open-Meteo API.
"""

from typing import Optional, Dict, Any
from utils.api_helpers import make_request


class WeatherAgent:
    """Agent responsible for fetching weather information."""
    
    OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self):
        """Initialize the WeatherAgent."""
        pass
    
    def get_current_weather(self, latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
        """
        Fetch current weather for given coordinates.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
        
        Returns:
            Dictionary containing weather information including:
            - temperature: Current temperature in Celsius
            - windspeed: Wind speed in km/h
            - winddirection: Wind direction in degrees
            - weathercode: Weather condition code
            - time: Time of the observation
            Returns None if error occurred
        """
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current_weather': 'true'
        }
        
        try:
            response = make_request(
                url=self.OPEN_METEO_BASE_URL,
                params=params,
                timeout=10
            )
            
            if response and 'current_weather' in response:
                current_weather = response['current_weather']
                return {
                    'temperature': current_weather.get('temperature'),
                    'windspeed': current_weather.get('windspeed'),
                    'winddirection': current_weather.get('winddirection'),
                    'weathercode': current_weather.get('weathercode'),
                    'time': current_weather.get('time')
                }
            else:
                print("Error: Invalid weather response format")
                return None
                
        except (ValueError, KeyError, TypeError) as e:
            print(f"Error parsing weather response: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching weather: {str(e)}")
            return None
    
    def format_weather_info(self, weather_data: Dict[str, Any]) -> str:
        """
        Format weather data into a human-readable string.
        
        Args:
            weather_data: Dictionary containing weather information
        
        Returns:
            Formatted string with weather information
        """
        if not weather_data:
            return "Weather information not available"
        
        temp = weather_data.get('temperature', 'N/A')
        wind_speed = weather_data.get('windspeed', 'N/A')
        wind_dir = weather_data.get('winddirection', 'N/A')
        weather_code = weather_data.get('weathercode', 'N/A')
        
        return (
            f"Temperature: {temp}°C | "
            f"Wind Speed: {wind_speed} km/h | "
            f"Wind Direction: {wind_dir}° | "
            f"Weather Code: {weather_code}"
        )


