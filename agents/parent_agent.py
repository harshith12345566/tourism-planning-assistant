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
        
        # Step 0: Check for natural language query
        specific_questions = []
        original_query = place_name
        intent = 'combined' # Default intent
        category = 'tourism' # Default category
        
        # If the input seems like a sentence or has multiple words, try to extract intent
        if len(place_name.split()) > 3 or " and " in place_name or " what " in place_name:
            intent_data = self.gemini_agent.extract_intent(place_name)
            if intent_data and intent_data.get('place'):
                place_name = intent_data['place']
                intent = intent_data.get('intent', 'combined')
                specific_questions = intent_data.get('specific_questions', [])
                print(f"DEBUG: Extracted place '{place_name}', intent '{intent}' from query '{original_query}'")
                
                # Map intent to category
                if intent == 'food':
                    category = 'food'
                elif intent == 'accommodation':
                    category = 'accommodation'
        
        result['intent'] = intent
        
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
        
        # Fetch photo for the main place
        result['place_info']['photo'] = self.photo_agent.get_place_photo(clean_name)
        
        # Step 3 & 4: Fetch weather and attractions in parallel for faster response
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        def fetch_weather():
            return self.weather_agent.get_current_weather(latitude, longitude)
        
        def fetch_attractions():
            return self.places_agent.get_tourist_attractions_with_addresses(
                latitude,
                longitude,
                radius=20000,
                limit=attractions_limit,
                category=category
            )
        
        # Always fetch both - we'll control what to show in format_output
        with ThreadPoolExecutor(max_workers=2) as executor:
            weather_future = executor.submit(fetch_weather)
            attractions_future = executor.submit(fetch_attractions)
            
            weather_data = weather_future.result()
            attractions = attractions_future.result()
        
        result['weather'] = weather_data
        
        # Fetch photos for attractions in parallel
        if attractions:
            with ThreadPoolExecutor(max_workers=5) as executor:
                # Create a dictionary to map future to attraction index
                future_to_attr = {
                    executor.submit(
                        self.photo_agent.get_attraction_photo, 
                        attr['name'], 
                        clean_name
                    ): i for i, attr in enumerate(attractions)
                }
                
                for future in as_completed(future_to_attr):
                    idx = future_to_attr[future]
                    try:
                        photo_url = future.result()
                        attractions[idx]['photo'] = photo_url
                    except Exception as e:
                        print(f"Error fetching photo for attraction: {e}")
                        attractions[idx]['photo'] = None
                        
        result['attractions'] = attractions
        
        # Only generate AI content if Gemini is enabled and working
        if self.gemini_agent.enabled:
            try:
                # Generate AI content in parallel
                def fetch_summary():
                    return self.gemini_agent.generate_destination_summary(
                        clean_name,
                        weather_data,
                        attractions,
                        specific_questions
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
        Format the result into a readable output string based on intent.
        
        Args:
            result: The result dictionary from process_place
        
        Returns:
            Formatted string with all information
        """
        if not result['success']:
            return result.get('error_message', 'Unknown error occurred')
        
        place_name = result['place_info']['name']
        intent = result.get('intent', 'combined')
        weather = result['weather']
        attractions = result['attractions']
        
        # Helper to format weather string
        weather_str = ""
        if weather:
            temp = weather.get('temperature', 'N/A')
            wind = weather.get('windspeed', 'N/A')
            # We don't have rain probability in current weather data, so we'll use wind/condition
            weather_str = f"In {place_name} it's currently {temp}°C with wind speed of {wind} km/h."
        else:
            weather_str = f"In {place_name}, weather information is currently unavailable."

        # Helper to format attractions list
        attractions_str = ""
        if attractions:
            attractions_str = "\n".join([f"{attr['name']}" for attr in attractions])
        else:
            attractions_str = "No places found."

        # Format based on intent
        if intent == 'weather':
            return weather_str
            
        elif intent == 'plan_trip':
            return f"In {place_name} these are the places you can go, - - - - -\n{attractions_str}"
            
        elif intent == 'food':
            return f"In {place_name} these are the places you can eat, - - - - -\n{attractions_str}"
            
        elif intent == 'accommodation':
            return f"In {place_name} these are the places you can stay, - - - - -\n{attractions_str}"
            
        else: # combined or unknown
            return f"{weather_str} And these are the places you can go: - - - - -\n{attractions_str}"

