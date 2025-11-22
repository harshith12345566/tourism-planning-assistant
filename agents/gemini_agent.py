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
