"""
Gemini AI Agent

This agent uses Google's Gemini 1.5 API to provide AI-enhanced descriptions
and insights about tourist destinations and attractions.
"""

import os
from typing import Optional, Dict, Any, List
import google.generativeai as genai


class GeminiAgent:
    """Agent responsible for AI-enhanced content using Gemini 1.5."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the GeminiAgent.
        
        Args:
            api_key: Google API key for Gemini. If not provided, 
                    will try to get from GEMINI_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY') or 'AIzaSyDwNP77GPVWYlrqfBpDCvYiegIqoQO3DRg'
        
        print(f"DEBUG: GeminiAgent initialized. API Key present: {bool(self.api_key)}")
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.enabled = True
                print("DEBUG: Gemini model configured successfully.")
            except Exception as e:
                print(f"DEBUG: Error configuring Gemini: {e}")
                self.enabled = False
        else:
            self.model = None
            self.enabled = False
            print("Warning: Gemini API key not found. AI features will be disabled.")
    
    def generate_destination_summary(
        self,
        place_name: str,
        weather_info: Optional[Dict[str, Any]] = None,
        attractions: Optional[List[Dict[str, Any]]] = None
    ) -> Optional[str]:
        """
        Generate an AI-powered summary about a destination.
        
        Args:
            place_name: Name of the destination
            weather_info: Weather information dictionary
            attractions: List of tourist attractions
        
        Returns:
            AI-generated summary or None if API is not available
        """
        if not self.enabled:
            return None
        
        try:
            print(f"DEBUG: Generating summary for {place_name}")
            # Build context for the AI
            context = f"Destination: {place_name}\n\n"
            

            if weather_info:
                temp = weather_info.get('temperature', 'N/A')
                context += f"Current Weather: {temp}°C\n\n"
            
            if attractions:
                context += "Top Attractions:\n"
                for i, attr in enumerate(attractions[:5], 1):
                    context += f"{i}. {attr.get('name', 'Unknown')}\n"
            
            prompt = f"""Based on the following information about {place_name}, provide a brief, engaging 2-3 sentence summary for tourists. Focus on what makes this destination special and worth visiting.

{context}

Keep it concise, informative, and exciting."""
            
            response = self.model.generate_content(prompt)
            print(f"DEBUG: Summary generated successfully: {response.text[:50]}...")
            return response.text.strip()
            
        except Exception as e:
            print(f"DEBUG: Error generating destination summary: {str(e)}")
            return None
    
    def get_attraction_description(self, attraction_name: str, location: str) -> Optional[str]:
        """
        Get an AI-generated description for a specific attraction.
        
        Args:
            attraction_name: Name of the attraction
            location: Location/city where the attraction is located
        
        Returns:
            Brief description or None if API is not available
        """
        if not self.enabled:
            return None
        
        try:
            prompt = f"""Provide a single concise sentence (max 20 words) describing {attraction_name} in {location}. 
Focus on its main significance or what it's famous for."""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Error generating attraction description: {str(e)}")
            return None
    
    def get_travel_tips(self, place_name: str, weather_info: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Generate AI-powered travel tips for a destination.
        
        Args:
            place_name: Name of the destination
            weather_info: Current weather information
        
        Returns:
            Travel tips or None if API is not available
        """
        if not self.enabled:
            return None
        
        try:
            context = f"Destination: {place_name}\n"
            
            if weather_info:
                temp = weather_info.get('temperature', 'N/A')
                wind = weather_info.get('wind_speed', 'N/A')
                context += f"Current Temperature: {temp}°C, Wind Speed: {wind} km/h\n"
            
            prompt = f"""Based on the current conditions in {place_name}, provide 3 brief, practical travel tips (each in one short sentence). 
Consider the weather and general travel advice.

{context}

Format as a numbered list."""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Error generating travel tips: {str(e)}")
            return None
    
    def generate_itinerary(
        self,
        place_name: str,
        attractions: List[Dict[str, Any]],
        weather_info: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Generate a day-by-day itinerary for visiting attractions.
        
        Args:
            place_name: Name of the destination
            attractions: List of tourist attractions
            weather_info: Current weather information
        
        Returns:
            AI-generated itinerary or None if API is not available
        """
        if not self.enabled or not attractions:
            return None
        
        try:
            context = f"Destination: {place_name}\n\n"
            
            if weather_info:
                temp = weather_info.get('temperature', 'N/A')
                context += f"Current Temperature: {temp}°C\n\n"
            
            context += "Attractions to visit:\n"
            for i, attr in enumerate(attractions, 1):
                context += f"{i}. {attr.get('name', 'Unknown')}\n"
            
            prompt = f"""Create a practical day-by-day itinerary for visiting these attractions in {place_name}. 
Include suggested times (morning/afternoon/evening) for each attraction.
Keep it concise - 1-2 lines per attraction.
Format as:

Day 1:
- Morning: [Attraction] - [Brief tip]
- Afternoon: [Attraction] - [Brief tip]

{context}"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Error generating itinerary: {str(e)}")
            return None
    
    def extract_intent(self, query: str) -> Dict[str, Any]:
        """
        Extract place name, intent, and specific questions from natural language query.
        
        Args:
            query: Natural language query from user
            
        Returns:
            Dictionary with 'place', 'intent', and 'specific_questions'
        """
        # Use fallback as primary method - it's more reliable for our use case
        return self._fallback_extract_intent(query)
    
    def _fallback_extract_intent(self, query: str) -> Dict[str, Any]:
        """Fallback intent extraction using pattern matching."""
        place = query
        lower_query = query.lower()
        intent = 'combined'  # Default to combined
        
        # Check for specific intents in fallback
        # Priority order: weather > food > accommodation > plan_trip
        if 'temperature' in lower_query or 'weather' in lower_query:
            # Check if it's ONLY about weather (no trip planning keywords)
            if not any(word in lower_query for word in ['plan', 'trip', 'visit', 'places', 'attractions', 'go to']):
                intent = 'weather'
            else:
                intent = 'combined'
        elif 'hotel' in lower_query or 'stay' in lower_query:
            intent = 'accommodation'
        elif 'restaurant' in lower_query or 'food' in lower_query or 'eat' in lower_query:
            intent = 'food'
        elif 'plan' in lower_query or 'trip' in lower_query or 'visit' in lower_query:
            intent = 'plan_trip'
        
        # Extract place name - handle various formats
        # First, check if query starts with a place name followed by comma
        if ',' in query:
            # Format: "Bangalore, what is the temperature"
            parts = query.split(',', 1)
            if len(parts[0].split()) <= 3:  # Likely a place name
                place = parts[0].strip()
                return {'place': place, 'intent': intent, 'specific_questions': []}
        
        # Remove common prefixes and patterns (handle variations)
        patterns = [
            "i'm going to go to ", "i'm going to ", "i am going to go to ", "i am going to ",
            "iam going to go to ", "iam going to ", "im going to go to ", "im going to ",
            "going to go to ", "going to ",
            "plan my trip to ", "plan trip to ", "trip to ", "travel to ", "visit ", "go to ", "show me ",
            "find hotels in ", "hotels in ", "places to stay in ",
            "restaurants in ", "food in ", "places to eat in ",
            "what is the temperature in ", "what is temperature in ", "what is temp in ",
            "what is the weather in ", "what is weather in ",
            "whats the temperature in ", "whats temperature in ", "whats temp in ",
            "whats the weather in ", "whats weather in ",
            "temperature in ", "weather in ", "temp in ",
            "what is the temperature there", "what is temperature there",
            "temperature of ", "weather of "
        ]
        
        for pattern in patterns:
            if pattern in lower_query:
                # Find the index of the pattern and take everything after it
                idx = lower_query.find(pattern) + len(pattern)
                place = query[idx:]
                break
        
        # Remove common suffixes/continuations (including question marks)
        separators = [
            " what is the temperature there", " what is the weather there",
            " whats the temperature there", " whats the weather there",
            " what is the temperature", " what is the weather",
            " whats the temperature", " whats the weather",
            " and what are the places", " and what places",
            " and ", " with ", " for ", " where ", " when ", " but ", 
            ",", "?", "!", " what ", " how "
        ]
        earliest_sep_idx = len(place)
        
        for sep in separators:
            idx = place.lower().find(sep)
            if idx != -1 and idx < earliest_sep_idx:
                earliest_sep_idx = idx
        
        if earliest_sep_idx < len(place):
            place = place[:earliest_sep_idx]
        
        # Clean up any remaining punctuation
        place = place.strip().rstrip(',.?!')
        
        return {'place': place.strip(), 'intent': intent, 'specific_questions': []}
