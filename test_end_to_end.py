
import os
from agents.parent_agent import ParentAgent

os.environ['GEMINI_API_KEY'] = 'AIzaSyDwNP77GPVWYlrqfBpDCvYiegIqoQO3DRg'

agent = ParentAgent()

test_cases = [
    ("I'm going to go to Bangalore, let's plan my trip", "plan_trip"),
    ("I'm going to go to Bangalore, what is the temperature there?", "weather"),
    ("what is temperature in hampi", "weather"),
    ("I'm going to go to Bangalore what is the temperature there", "weather"),
    ("iam going to Mumbai let's plan my trip", "plan_trip"),
    ("I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?", "combined"),
]

print("=" * 80)
print("END-TO-END TEST - Query to Output")
print("=" * 80)

for query, expected_intent in test_cases:
    print(f"\n{'='*80}")
    print(f"Query: {query}")
    print(f"Expected Intent: {expected_intent}")
    print(f"{'='*80}")
    
    result = agent.process_place(query)
    
    actual_intent = result.get('intent')
    success = result.get('success')
    
    print(f"✓ Success: {success}")
    print(f"✓ Actual Intent: {actual_intent}")
    print(f"✓ Match: {'YES' if actual_intent == expected_intent else 'NO'}")
    
    if success:
        output = agent.format_output(result)
        print(f"\nFormatted Output:")
        print(f"{output[:200]}...")
        
        # Verify output correctness
        if expected_intent == 'weather':
            has_temp = 'temperature' in output.lower() or '°c' in output.lower()
            has_places = 'these are the places' in output.lower()
            print(f"\n✓ Has temperature: {has_temp}")
            print(f"✓ Has places: {has_places}")
            print(f"✓ Correct output: {'YES' if has_temp and not has_places else 'NO'}")
        elif expected_intent == 'plan_trip':
            has_temp = 'temperature' in output.lower() or '°c' in output.lower()
            has_places = 'these are the places' in output.lower()
            print(f"\n✓ Has temperature: {has_temp}")
            print(f"✓ Has places: {has_places}")
            print(f"✓ Correct output: {'YES' if has_places and not has_temp else 'NO'}")
        elif expected_intent == 'combined':
            has_temp = 'temperature' in output.lower() or '°c' in output.lower()
            has_places = 'these are the places' in output.lower()
            print(f"\n✓ Has temperature: {has_temp}")
            print(f"✓ Has places: {has_places}")
            print(f"✓ Correct output: {'YES' if has_temp and has_places else 'NO'}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
