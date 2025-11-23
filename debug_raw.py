
import requests
import json

def test_raw_overpass():
    url = "https://overpass-api.de/api/interpreter"
    
    # Very simple query: find any node within 1000m of Bangalore center
    query = """
    [out:json][timeout:25];
    node(around:1000,12.9716,77.5946);
    out body 5;
    """
    
    print("Sending raw query...")
    try:
        response = requests.post(url, data={'data': query})
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            elements = data.get('elements', [])
            print(f"Found {len(elements)} elements")
            if elements:
                print("First element:", elements[0])
        else:
            print("Error response:", response.text)
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_raw_overpass()
