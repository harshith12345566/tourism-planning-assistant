"""
Parent Agent

This agent orchestrates the entire multi-agent tourism system.
It coordinates the geocoding, weather, and places agents.
"""

from typing import Optional, Dict, Any
from agents.geocode_agent import GeocodeAgent
from agents.weather_agent import WeatherAgent
from agents.places_agent import PlacesAgent
from agents.gemini_agent import GeminiAgent
from agents.photo_agent import PhotoAgent


class ParentAgent:
    """Main orchestrator agent that coordinates all child agents."""
    
    def __init__(self):
        """Initialize the ParentAgent and all child agents."""
        self.geocode_agent = GeocodeAgent()
        self.weather_agent = WeatherAgent()
        self.places_agent = PlacesAgent()
        self.photo_agent = PhotoAgent()
        self.gemini_agent = GeminiAgent()
    
    def process_place(self, place_name: str, attractions_limit: int = 5) -> Dict[str, Any]:
        """
        Process a place name and gather all tourism information.
        
        Args:
            place_name: The name of the place to process
            attractions_limit: Maximum number of attractions to return (default: 5)
        
        Returns:
            Dictionary containing:
            - success: Boolean indicating if processing was successful
            - error_message: Error message if unsuccessful
            - place_info: Place information (name, coordinates)
            - weather: Weather information
            - attractions: List of tourist attractions with addresses
            - ai_summary: AI-generated destination summary (if available)
            - travel_tips: AI-generated travel tips (if available)
        """
        result = {
            'success': False,
            'error_message': None,
            'place_info': None,
            'weather': None,
            'attractions': [],
            'ai_summary': None,
            'travel_tips': None
        }
        
        # Step 1: Geocode the place
        geocode_result = self.geocode_agent.geocode(place_name)
        
        if not geocode_result:
            result['error_message'] = "I don't know this place."
            return result
        
        # Step 2: Extract coordinates
        latitude = geocode_result['lat']
        longitude = geocode_result['lon']
        display_name = geocode_result['display_name']
        
        
        # Use the user's input as the city name (properly capitalized)
        # This ensures we show what the user searched for, not technical geocoding names
        clean_name = place_name.title()
        
        result['place_info'] = {
            'name': clean_name,
            'full_name': display_name,
            'lat': latitude,
            'lon': longitude
        }
        
        # Fetch photo for the main place (skip for now, photos disabled)
        result['place_info']['photo'] = None
        
        # Step 3 & 4: Fetch weather and attractions in parallel for faster response
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        def fetch_weather():
            return self.weather_agent.get_current_weather(latitude, longitude)
        
        def fetch_attractions():
            return self.places_agent.get_tourist_attractions_with_addresses(
                latitude,
                longitude,
                radius=20000,
                limit=attractions_limit
            )
        
        # Run weather and attractions fetch in parallel
        with ThreadPoolExecutor(max_workers=2) as executor:
            weather_future = executor.submit(fetch_weather)
            attractions_future = executor.submit(fetch_attractions)
            
            weather_data = weather_future.result()
            attractions = attractions_future.result()
        
        result['weather'] = weather_data
        result['attractions'] = attractions
        
        # Skip photo fetching for attractions (photos disabled)
        
        # Only generate AI content if Gemini is enabled and working
        if self.gemini_agent.enabled:
            try:
                # Generate AI content in parallel
                def fetch_summary():
                    return self.gemini_agent.generate_destination_summary(
                        clean_name,
                        weather_data,
                        attractions
                    )
                
                def fetch_tips():
                    return self.gemini_agent.get_travel_tips(clean_name, weather_data)
                
                def fetch_itinerary():
                    return self.gemini_agent.generate_itinerary(clean_name, attractions, weather_data)
                
                with ThreadPoolExecutor(max_workers=3) as executor:
                    summary_future = executor.submit(fetch_summary)
                    tips_future = executor.submit(fetch_tips)
                    itinerary_future = executor.submit(fetch_itinerary)
                    
                    result['ai_summary'] = summary_future.result(timeout=5)  # 5 sec timeout
                    result['travel_tips'] = tips_future.result(timeout=5)
                    result['itinerary'] = itinerary_future.result(timeout=5)
            except Exception as e:
                print(f"Error generating AI content: {str(e)}")
                # Continue without AI content
        
        result['success'] = True
        return result
    
    def format_output(self, result: Dict[str, Any]) -> str:
        """
        Format the result into a readable output string.
        
        Args:
            result: The result dictionary from process_place
        
        Returns:
            Formatted string with all information
        """
        if not result['success']:
            return result.get('error_message', 'Unknown error occurred')
        
        output_lines = []
        
        # Place information
        place_info = result['place_info']
        output_lines.append("=" * 60)
        output_lines.append("TOURISM INFORMATION")
        output_lines.append("=" * 60)
        output_lines.append(f"\nPlace: {place_info['name']}")
        output_lines.append(f"Coordinates: {place_info['lat']:.4f}, {place_info['lon']:.4f}")
        
        # Weather information
        weather = result['weather']
        if weather:
            output_lines.append(f"\nWeather:")
            output_lines.append(f"   {self.weather_agent.format_weather_info(weather)}")
        else:
            output_lines.append("\nWeather: Information not available")
        
        # Tourist attractions
        attractions = result['attractions']
        output_lines.append(f"\nTourist Attractions (Top {len(attractions)}):")
        if attractions:
            for i, attr in enumerate(attractions, 1):
                output_lines.append(f"   {i}. {attr['name']} ({attr.get('tourism', 'attraction')})")
        else:
            output_lines.append("   No tourist attractions found nearby")
        
        output_lines.append("\n" + "=" * 60)
        
        return "\n".join(output_lines)

