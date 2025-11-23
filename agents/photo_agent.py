"""
Photo Agent

This agent fetches photos for places and attractions using the Wikimedia Commons API.
"""

from typing import Optional, Dict, Any, List
from utils.api_helpers import make_request
import urllib.parse


class PhotoAgent:
    """Agent responsible for providing photos using Wikimedia API."""
    
    WIKI_API_URL = "https://en.wikipedia.org/w/api.php"
    
    def __init__(self):
        """Initialize the PhotoAgent."""
        self.headers = {
            'User-Agent': 'Multi-Agent-Tourism-System/1.0'
        }

    def get_place_photo(self, place_name: str) -> Optional[str]:
        """
        Get a photo URL for a place.
        
        Args:
            place_name: Name of the place
            
        Returns:
            URL of the photo or None if not found
        """
        return self._fetch_wiki_image(place_name)
    
    def get_attraction_photo(self, attraction_name: str, city: str = "") -> Optional[str]:
        """
        Get a photo URL for a specific attraction.
        
        Args:
            attraction_name: Name of the attraction
            city: Optional city name to refine search
            
        Returns:
            URL of the photo or None if not found
        """
        query = f"{attraction_name} {city}".strip()
        return self._fetch_wiki_image(query)
    
    def _fetch_wiki_image(self, query: str) -> Optional[str]:
        """
        Helper to fetch image from Wikimedia.
        """
        if not query:
            return None
            
        params = {
            "action": "query",
            "format": "json",
            "prop": "pageimages",
            "generator": "search",
            "gsrsearch": query,
            "gsrlimit": 1,
            "piprop": "thumbnail",
            "pithumbsize": 600,  # Request a reasonable size
            "pilimit": 1
        }
        
        try:
            response = make_request(
                url=self.WIKI_API_URL,
                params=params,
                headers=self.headers,
                timeout=5
            )
            
            if response and 'query' in response and 'pages' in response['query']:
                pages = response['query']['pages']
                for page_id in pages:
                    page = pages[page_id]
                    if 'thumbnail' in page and 'source' in page['thumbnail']:
                        return page['thumbnail']['source']
            
            return None
            
        except Exception as e:
            print(f"Error fetching photo for {query}: {str(e)}")
            return None

