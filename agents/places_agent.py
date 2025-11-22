"""
Tourist Places Agent

This agent fetches tourist attractions near a location using the Overpass API.
"""

from typing import Optional, List, Dict, Any
from utils.api_helpers import make_post_request, make_request


class PlacesAgent:
    """Agent responsible for finding tourist attractions."""
    
    OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"
    
    def __init__(self):
        """Initialize the PlacesAgent."""
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    
    def get_tourist_attractions(
        self,
        latitude: float,
        longitude: float,
        radius: int = 5000,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Fetch tourist attractions near given coordinates.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            radius: Search radius in meters (default: 5000)
            limit: Maximum number of attractions to return (default: 5)
        
        Returns:
            List of dictionaries containing attraction information:
            - name: Name of the attraction
            - lat: Latitude
            - lon: Longitude
            - tourism: Type of tourism feature
            Returns empty list if no attractions found or error occurred
        """
        # Expanded Overpass QL query to find various types of tourist attractions
        # Including: attractions, viewpoints, museums, monuments, artwork, galleries, etc.
        query = f"""[out:json][timeout:30];
(
  node["tourism"~"attraction|viewpoint|museum|artwork|gallery|theme_park|zoo"](around:{radius},{latitude},{longitude});
  node["historic"~"monument|memorial|castle|ruins|archaeological_site"](around:{radius},{latitude},{longitude});
  node["natural"~"peak|waterfall|cave_entrance|hot_spring"](around:{radius},{latitude},{longitude});
  node["leisure"~"park|garden|nature_reserve"](around:{radius},{latitude},{longitude});
  way["tourism"~"attraction|viewpoint|museum|artwork|gallery|theme_park|zoo"](around:{radius},{latitude},{longitude});
  way["historic"~"monument|memorial|castle|ruins|archaeological_site"](around:{radius},{latitude},{longitude});
  way["natural"~"peak|waterfall|cave_entrance|hot_spring"](around:{radius},{latitude},{longitude});
  way["leisure"~"park|garden|nature_reserve"](around:{radius},{latitude},{longitude});
);
out center;"""
        
        try:
            print(f"DEBUG: Searching for attractions around {latitude}, {longitude} with radius {radius}m")
            # Overpass API expects the query as form data with key "data"
            response = make_post_request(
                url=self.OVERPASS_API_URL,
                data={'data': query},
                headers=self.headers,
                timeout=30
            )
            
            if response and 'elements' in response:
                elements = response['elements']
                print(f"DEBUG: Found {len(elements)} total elements")
                attractions = []
                
                for element in elements[:limit * 3]:  # Get more to filter later
                    tags = element.get('tags', {})
                    # Prefer English name, fallback to default name
                    name = tags.get('name:en') or tags.get('name')
                    
                    if not name:  # Skip unnamed attractions
                        continue
                    
                    # Get coordinates (for ways, use center)
                    if 'lat' in element and 'lon' in element:
                        att_lat = element.get('lat')
                        att_lon = element.get('lon')
                    elif 'center' in element:
                        att_lat = element['center'].get('lat')
                        att_lon = element['center'].get('lon')
                    else:
                        continue
                    
                    # Determine type
                    tourism_type = (tags.get('tourism') or 
                                  tags.get('historic') or 
                                  tags.get('natural') or 
                                  tags.get('leisure') or 
                                  'attraction')
                    
                    attractions.append({
                        'name': name,
                        'lat': att_lat,
                        'lon': att_lon,
                        'tourism': tourism_type
                    })
                    
                    if len(attractions) >= limit:
                        break
                
                print(f"DEBUG: Returning {len(attractions)} named attractions")
                return attractions
            else:
                print("DEBUG: No elements found in response")
                return []
                
        except (ValueError, KeyError, TypeError) as e:
            print(f"Error parsing places response: {str(e)}")
            return []
        except Exception as e:
            print(f"Unexpected error fetching tourist places: {str(e)}")
            return []
    
    def get_address(self, latitude: float, longitude: float) -> Optional[str]:
        """
        Get address for given coordinates using reverse geocoding.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
        
        Returns:
            Address string or None if not found
        """
        nominatim_url = "https://nominatim.openstreetmap.org/reverse"
        
        params = {
            'lat': latitude,
            'lon': longitude,
            'format': 'json',
            'accept-language': 'en'
        }
        
        headers = {
            'User-Agent': 'Multi-Agent-Tourism-System/1.0'
        }
        
        try:
            response = make_request(
                url=nominatim_url,
                params=params,
                headers=headers,
                timeout=10
            )
            
            if response and 'display_name' in response:
                return response['display_name']
            return None
            
        except Exception as e:
            print(f"Error getting address: {str(e)}")
            return None
    
    def get_tourist_attractions_with_addresses(
        self,
        latitude: float,
        longitude: float,
        radius: int = 5000,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Fetch tourist attractions with their addresses.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            radius: Search radius in meters (default: 5000)
            limit: Maximum number of attractions to return (default: 5)
        
        Returns:
            List of dictionaries containing attraction information with addresses
        """
        attractions = self.get_tourist_attractions(latitude, longitude, radius, limit)
        
        # Add addresses to each attraction
        for attraction in attractions:
            if 'lat' in attraction and 'lon' in attraction:
                address = self.get_address(attraction['lat'], attraction['lon'])
                attraction['address'] = address if address else "Address not available"
        
        return attractions
    
    def format_attractions(self, attractions: List[Dict[str, Any]]) -> str:
        """
        Format attractions list into a human-readable string.
        
        Args:
            attractions: List of attraction dictionaries
        
        Returns:
            Formatted string with attractions information
        """
        if not attractions:
            return "No tourist attractions found nearby"
        
        formatted = []
        for i, attr in enumerate(attractions, 1):
            name = attr.get('name', 'Unnamed')
            tourism_type = attr.get('tourism', 'attraction')
            formatted.append(f"{i}. {name} ({tourism_type})")
        
        return "\n".join(formatted)

