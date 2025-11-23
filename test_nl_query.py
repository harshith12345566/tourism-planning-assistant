"""
Test script to demonstrate the tourism system with various natural language queries.
"""

from agents.parent_agent import ParentAgent
import os

# Ensure API key is set
os.environ['GEMINI_API_KEY'] = 'AIzaSyDwNP77GPVWYlrqfBpDCvYiegIqoQO3DRg'

def test_query(query: str):
    """Test the system with a given natural language query."""
    print("\n" + "=" * 60)
    print(f"Query: {query}")
    print("=" * 60)
    
    # Initialize the parent agent
    parent_agent = ParentAgent()
    
    # Process the place
    print("Processing...")
    result = parent_agent.process_place(query)
    
    # Display results
    output = parent_agent.format_output(result)
    print("\nOUTPUT:")
    print(output)

if __name__ == "__main__":
    queries = [
        "I’m going to go to Bangalore, let’s plan my trip.",
        "I’m going to go to Bangalore, what is the temperature there",
        "I’m going to go to Bangalore, what is the temperature there? And what are the places I can visit?",
        "Show me restaurants in Mumbai",
        "Find hotels in Delhi"
    ]
    
    for q in queries:
        test_query(q)
