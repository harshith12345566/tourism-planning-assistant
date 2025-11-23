
import os
from agents.parent_agent import ParentAgent

os.environ['GEMINI_API_KEY'] = 'AIzaSyDwNP77GPVWYlrqfBpDCvYiegIqoQO3DRg'

agent = ParentAgent()

# Test 1: Weather only
print("TEST 1: Weather only query")
print("=" * 60)
query1 = "what is temperature in hampi"
result1 = agent.process_place(query1)
output1 = agent.format_output(result1)
print(f"Query: {query1}")
print(f"Intent: {result1.get('intent')}")
print(f"Output: {output1}")
print()

# Test 2: Plan trip only
print("TEST 2: Plan trip query")
print("=" * 60)
query2 = "I'm going to go to Bangalore let's plan my trip"
result2 = agent.process_place(query2)
output2 = agent.format_output(result2)
print(f"Query: {query2}")
print(f"Intent: {result2.get('intent')}")
print(f"Output: {output2[:150]}...")
print()

# Test 3: Combined
print("TEST 3: Combined query")
print("=" * 60)
query3 = "I'm going to go to Mumbai what is the temperature there? And what are the places I can visit?"
result3 = agent.process_place(query3)
output3 = agent.format_output(result3)
print(f"Query: {query3}")
print(f"Intent: {result3.get('intent')}")
print(f"Output: {output3[:150]}...")
