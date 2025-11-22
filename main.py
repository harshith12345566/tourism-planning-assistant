"""
Multi-Agent Tourism System

Main entry point for the tourism information system.
This system uses multiple agents to gather weather and tourist attraction
information for any given place.
"""

from agents.parent_agent import ParentAgent


def main():
    """Main function to run the tourism system."""
    print("=" * 60)
    print("MULTI-AGENT TOURISM SYSTEM")
    print("=" * 60)
    print("\nThis system provides weather and tourist attraction information")
    print("for any place in the world.\n")
    
    # Initialize the parent agent
    parent_agent = ParentAgent()
    
    # Main loop
    while True:
        try:
            # Get user input
            place_name = input("\nEnter a place name (or 'quit' to exit): ").strip()
            
            if not place_name:
                print("Please enter a valid place name.")
                continue
            
            if place_name.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for using the Multi-Agent Tourism System!")
                break
            
            # Process the place
            print("\nProcessing your request...")
            result = parent_agent.process_place(place_name)
            
            # Display results
            output = parent_agent.format_output(result)
            print(output)
            
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {str(e)}")
            print("Please try again with a different place name.")


if __name__ == "__main__":
    main()

