"""
Photo Agent

This agent is disabled - no images will be shown.
"""

from typing import Optional, Dict, Any, List


class PhotoAgent:
    """Agent responsible for providing photos - currently disabled."""
    
    def __init__(self):
        """Initialize the PhotoAgent."""
        pass

    def get_place_photo(self, place_name: str) -> Optional[str]:
        """Get a photo URL for a place."""
        return None
    
    def get_attraction_photo(self, attraction_name: str, city: str = "") -> Optional[str]:
        """Get a photo URL for a specific attraction."""
        return None
    
    def get_multiple_photos(self, place_name: str, count: int = 3) -> List[str]:
        """Get multiple photos for a place."""
        return []
