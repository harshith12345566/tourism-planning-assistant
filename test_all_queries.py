
import os
from agents.parent_agent import ParentAgent

os.environ['GEMINI_API_KEY'] = 'AIzaSyDwNP77GPVWYlrqfBpDCvYiegIqoQO3DRg'

agent = ParentAgent()

test_cases = [
    "I'm going to go to Bangalore, what is the temperature there",
    "Plan my trip to Bangalore",
    "I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?"
]

for query in test_cases:
    print("=" * 60)
    print(f"Query: {query}")
    print("=" * 60)
    
    result = agent.process_place(query)
    output = agent.format_output(result)
    
    print(f"Intent: {result.get('intent')}")
    print(f"Attractions: {len(result.get('attractions', []))}")
    print(f"Weather: {'Yes' if result.get('weather') else 'No'}")
    print(f"\nOutput:\n{output}")
    print("\n")
