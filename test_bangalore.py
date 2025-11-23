
import os
from agents.parent_agent import ParentAgent

os.environ['GEMINI_API_KEY'] = 'AIzaSyDwNP77GPVWYlrqfBpDCvYiegIqoQO3DRg'

agent = ParentAgent()
query = "Bangalore,what is the temperature there?"

print(f"Query: {query}\n")
result = agent.process_place(query)

print(f"Intent detected: {result.get('intent')}")
print(f"Weather: {result.get('weather')}")
print(f"Attractions count: {len(result.get('attractions', []))}")
print(f"\nFormatted output:")
print(agent.format_output(result))
