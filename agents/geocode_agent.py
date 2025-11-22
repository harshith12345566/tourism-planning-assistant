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
        
        # Get multiple results to find the most relevant one
        params = {
            'q': place_name.strip(),
            'format': 'json',
            'limit': 5,  # Get top 5 results instead of just 1
            'accept-language': 'en',
            'addressdetails': 1  # Get detailed address info
        }
        
        try:
            response = make_request(
                url=self.NOMINATIM_BASE_URL,
                params=params,
                headers=self.headers,
                timeout=10
            )
            
            if response and isinstance(response, list) and len(response) > 0:
                # Choose the most relevant result based on importance score
                # Nominatim returns results sorted by relevance, but we'll also check importance
                best_result = response[0]
                best_importance = float(best_result.get('importance', 0))
                
                # Check if any other result has significantly higher importance
                for result in response[1:]:
                    importance = float(result.get('importance', 0))
                    if importance > best_importance * 1.2:  # 20% higher importance threshold
                        best_result = result
                        best_importance = importance
                
                print(f"DEBUG: Geocoded '{place_name}' to {best_result.get('display_name')}")
                
                return {
                    'lat': float(best_result.get('lat', 0)),
                    'lon': float(best_result.get('lon', 0)),
                    'display_name': best_result.get('display_name', place_name),
                    'place_id': best_result.get('place_id'),
                    'place_type': best_result.get('type', 'unknown')
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


