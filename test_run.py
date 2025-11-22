"""
Test script to demonstrate the tourism system with a sample place.
This runs the system programmatically without requiring user input.
"""

from agents.parent_agent import ParentAgent

def test_place(place_name: str):
    """Test the system with a given place name."""
    print("=" * 60)
    print("MULTI-AGENT TOURISM SYSTEM - TEST RUN")
    print("=" * 60)
    print(f"\nTesting with place: {place_name}\n")
    
    # Initialize the parent agent
    parent_agent = ParentAgent()
    
    # Process the place
    print("Processing your request...")
    result = parent_agent.process_place(place_name)
    
    # Display results
    output = parent_agent.format_output(result)
    print(output)

if __name__ == "__main__":
    # Test with a well-known place
    test_place("Paris")


