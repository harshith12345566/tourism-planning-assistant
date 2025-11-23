
import os
from agents.gemini_agent import GeminiAgent

os.environ['GEMINI_API_KEY'] = 'AIzaSyDwNP77GPVWYlrqfBpDCvYiegIqoQO3DRg'

agent = GeminiAgent()
query = "I’m going to go to Bangalore, what is the temperature there"
print(f"Testing query: {query}")

try:
    result = agent.extract_intent(query)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
