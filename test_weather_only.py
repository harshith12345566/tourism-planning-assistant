
import os
from agents.parent_agent import ParentAgent

os.environ['GEMINI_API_KEY'] = 'AIzaSyDwNP77GPVWYlrqfBpDCvYiegIqoQO3DRg'

agent = ParentAgent()
query = "I'm going to go to Bangalore, what is the temperature there"
print(f"Testing query: {query}\n")

result = agent.process_place(query)
output = agent.format_output(result)
print("OUTPUT:")
print(output)
print(f"\nIntent detected: {result.get('intent')}")
print(f"Attractions count: {len(result.get('attractions', []))}")
