from route_optimizer import RouteOptimizer

def test_route_optimizer():
    """Test the route optimizer directly"""
    print("🚀 Testing Route Optimizer...")
    print("=" * 50)
    
    # Test data
    departure_point = "Vancouver, BC"
    destinations = [
        {"label": "SDM 0203", "address": "1301 Main St, Penticton, BC V2A 5E9"},
        {"label": "LD 0003", "address": "100 - 555 Sixth Street, New Westminster, BC V3L 5H1"}
    ]
    
    try:
        # Initialize optimizer
        print("🔧 Initializing RouteOptimizer...")
        optimizer = RouteOptimizer()
        print("✅ RouteOptimizer initialized")
        
        # Test full optimization
        print("\n🧪 Testing full CrewAI optimization...")
        result = optimizer.optimize_route(departure_point, destinations)
        
        print(f"📊 Result success: {result['success']}")
        
        if result['success']:
            print("✅ Full optimization worked!")
            print(f"📍 Route length: {len(result['route'])}")
            print(f"📊 Analysis: {result.get('analysis', {})}")
        else:
            print(f"❌ Full optimization failed: {result.get('error')}")
            
            # Test simplified optimization
            print("\n🧪 Testing simplified optimization...")
            simple_result = optimizer.get_simple_optimized_route(departure_point, destinations)
            
            print(f"📊 Simple result success: {simple_result['success']}")
            if simple_result['success']:
                print("✅ Simplified optimization worked!")
                print(f"📍 Route length: {len(simple_result['route'])}")
            else:
                print(f"❌ Simplified optimization also failed: {simple_result.get('error')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Exception during testing: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    test_route_optimizer() 