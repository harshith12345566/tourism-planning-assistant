
from agents.places_agent import PlacesAgent
from agents.geocode_agent import GeocodeAgent
import sys

def debug_places(place_name):
    with open("debug_log.txt", "w", encoding="utf-8") as f:
        sys.stdout = f
        print(f"Debugging places for: {place_name}")
        
        # 1. Geocode
        geo = GeocodeAgent()
        loc = geo.geocode(place_name)
        
        if not loc:
            print("Geocoding failed")
            return
            
        print(f"Location: {loc['display_name']}")
        print(f"Coords: {loc['lat']}, {loc['lon']}")
        
        # 2. Fetch Places
        places_agent = PlacesAgent()
        
        # Test default tourism
        print("\n--- Testing Tourism Category ---")
        attractions = places_agent.get_tourist_attractions(
            loc['lat'], loc['lon'], radius=10000, limit=10, category='tourism'
        )
        print(f"Found {len(attractions)} attractions")
        for a in attractions:
            print(f"- {a['name']} ({a.get('tourism')})")

        # Test food
        print("\n--- Testing Food Category ---")
        food = places_agent.get_tourist_attractions(
            loc['lat'], loc['lon'], radius=5000, limit=5, category='food'
        )
        print(f"Found {len(food)} food places")
        for f in food:
            print(f"- {f['name']}")

if __name__ == "__main__":
    debug_places("Bangalore")
