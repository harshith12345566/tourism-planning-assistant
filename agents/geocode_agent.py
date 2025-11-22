"""
Geocoding Agent

This agent handles geocoding of place names using the Nominatim API.
It converts place names to latitude and longitude coordinates.
"""

from typing import Optional, Dict, Any, Tuple
from utils.api_helpers import make_request


class GeocodeAgent:
    """Agent responsible for geocoding place names to coordinates."""
    
    NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org/search"
    
    def __init__(self):
        """Initialize the GeocodeAgent."""
        self.headers = {
            'User-Agent': 'Multi-Agent-Tourism-System/1.0'
        }
    
    def geocode(self, place_name: str) -> Optional[Dict[str, Any]]:
        """
        Geocode a place name to get its coordinates and details.
        
        Args:
            place_name: The name of the place to geocode
        
        Returns:
            Dictionary containing place information including:
            - lat: Latitude
            - lon: Longitude
            - display_name: Full display name
            - place_id: Nominatim place ID
            Returns None if place not found or error occurred
        """
        if not place_name or not place_name.strip():
            return None
        
        params = {
            'q': place_name.strip(),
            'format': 'json',
            'limit': 1,
            'accept-language': 'en'
        }
        
        try:
            response = make_request(
                url=self.NOMINATIM_BASE_URL,
                params=params,
                headers=self.headers,
                timeout=10
            )
            
            if response and isinstance(response, list) and len(response) > 0:
                result = response[0]
                return {
                    'lat': float(result.get('lat', 0)),
                    'lon': float(result.get('lon', 0)),
                    'display_name': result.get('display_name', place_name),
                    'place_id': result.get('place_id'),
                    'place_type': result.get('type', 'unknown')
                }
            else:
                return None
                
        except (ValueError, KeyError, TypeError) as e:
            print(f"Error parsing geocoding response: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error in geocoding: {str(e)}")
            return None
    
    def get_coordinates(self, place_name: str) -> Optional[Tuple[float, float]]:
        """
        Get only the coordinates for a place name.
        
        Args:
            place_name: The name of the place
        
        Returns:
            Tuple of (latitude, longitude) or None if not found
        """
        result = self.geocode(place_name)
        if result:
            return (result['lat'], result['lon'])
        return None


