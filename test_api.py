import googlemaps
from config_loader import load_config

def test_google_maps_api():
    """Test if Google Maps API is working correctly"""
    try:
        # Load config
        config = load_config()
        api_key = config.get("api_keys", {}).get("google_maps")
        
        print(f"🔑 API Key loaded: {api_key[:20]}..." if api_key else "❌ No API key found")
        
        if not api_key:
            print("❌ No API key found in config.yaml")
            return False
        
        # Initialize Google Maps client
        gmaps = googlemaps.Client(key=api_key)
        print("✅ Google Maps client initialized")
        
        # Test 1: Geocoding
        print("\n🧪 Testing Geocoding API...")
        test_address = "Vancouver, BC, Canada"
        geocode_result = gmaps.geocode(test_address)
        
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            print(f"✅ Geocoding works: {test_address} -> {location['lat']}, {location['lng']}")
        else:
            print(f"❌ Geocoding failed for {test_address}")
            return False
        
        # Test 2: Directions API
        print("\n🧪 Testing Directions API...")
        directions_result = gmaps.directions(
            origin="Vancouver, BC",
            destination="Burnaby, BC",
            mode="driving"
        )
        
        if directions_result:
            route = directions_result[0]
            duration = route['legs'][0]['duration']['text']
            distance = route['legs'][0]['distance']['text']
            print(f"✅ Directions works: Vancouver -> Burnaby ({distance}, {duration})")
        else:
            print("❌ Directions API failed")
            return False
        
        # Test 3: Directions with Waypoint Optimization
        print("\n🧪 Testing Waypoint Optimization...")
        optimized_directions = gmaps.directions(
            origin="Vancouver, BC",
            destination="Vancouver, BC",
            waypoints=["Burnaby, BC", "Richmond, BC"],
            optimize_waypoints=True,
            mode="driving"
        )
        
        if optimized_directions:
            waypoint_order = optimized_directions[0].get('waypoint_order', [])
            print(f"✅ Waypoint optimization works: Order = {waypoint_order}")
        else:
            print("❌ Waypoint optimization failed")
            return False
        
        print("\n🎉 All API tests passed! Your Google Maps integration should work.")
        return True
        
    except googlemaps.exceptions.ApiError as e:
        print(f"❌ Google Maps API Error: {e}")
        return False
    except Exception as e:
        print(f"❌ General Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Google Maps API Integration...")
    print("=" * 50)
    
    success = test_google_maps_api()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ SUCCESS: Your Google Maps API is properly configured!")
        print("The app should now use full AI-powered optimization.")
    else:
        print("❌ FAILURE: Please check your Google Cloud setup.")
        print("The app will continue using simplified optimization.") 