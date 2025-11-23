
import os
from agents.gemini_agent import GeminiAgent

os.environ['GEMINI_API_KEY'] = 'AIzaSyDwNP77GPVWYlrqfBpDCvYiegIqoQO3DRg'

agent = GeminiAgent()
print(f"Agent enabled: {agent.enabled}")

queries = [
    "I’m going to go to Bangalore, let’s plan my trip.",
    "I’m going to go to Bangalore, what is the temperature there",
    "I’m going to go to Bangalore, what is the temperature there? And what are the places I can visit?",
    "Show me restaurants in Mumbai",
    "Find hotels in Delhi"
]

for q in queries:
    print(f"\nTesting query: {q}")
    try:
        result = agent.extract_intent(q)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
