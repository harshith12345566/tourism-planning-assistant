
import os
from agents.parent_agent import ParentAgent

os.environ['GEMINI_API_KEY'] = 'AIzaSyDwNP77GPVWYlrqfBpDCvYiegIqoQO3DRg'

agent = ParentAgent()

test_cases = [
    ("Bangalore,what is the temperature there?", "weather"),
    ("I'm going to go to Bangalore, what is the temperature there", "weather"),
    ("Plan my trip to Bangalore", "plan_trip"),
    ("I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?", "combined"),
    ("Show me restaurants in Mumbai", "food"),
]

print("=" * 70)
print("COMPREHENSIVE TEST")
print("=" * 70)

for query, expected_intent in test_cases:
    print(f"\nQuery: {query}")
    print(f"Expected Intent: {expected_intent}")
    
    result = agent.process_place(query)
    actual_intent = result.get('intent')
    
    print(f"Actual Intent: {actual_intent}")
    print(f"Match: {'✓' if actual_intent == expected_intent else '✗'}")
    
    output = agent.format_output(result)
    print(f"Output: {output[:100]}...")
    print("-" * 70)
