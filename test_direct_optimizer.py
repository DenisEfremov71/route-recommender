from direct_route_optimizer import DirectRouteOptimizer

def test_direct_optimizer():
    print("🚀 Testing Direct Route Optimizer...")
    print("=" * 50)
    
    try:
        # Test the direct optimizer
        optimizer = DirectRouteOptimizer()
        result = optimizer.optimize_route(
            'Vancouver, BC',
            [
                {'label': 'SDM 0203', 'address': '1301 Main St, Penticton, BC V2A 5E9'},
                {'label': 'LD 0003', 'address': '100 - 555 Sixth Street, New Westminster, BC V3L 5H1'}
            ]
        )

        print('✅ Success:', result['success'])
        if result['success']:
            print('📍 Route length:', len(result['route']))
            print('📊 Distance:', result['analysis']['total_distance_km'], 'km')
            print('⏱️ Duration:', result['analysis']['total_duration_formatted'])
            print('💰 Fuel cost: $', result['analysis']['estimated_fuel_cost_cad'], 'CAD')
            print('🎯 Optimization:', result['analysis']['route_efficiency'])
            print('🔗 Maps URL available:', bool(result['directions_url']))
            print('🔗 Google Maps URL:', result['directions_url'])
            

            
            print('\n📋 Route order:')
            for i, stop in enumerate(result['route']):
                print(f"  {i+1}. {stop['label']}")
                
            print('\n💡 Recommendations:')
            for rec in result['analysis']['recommendations']:
                print(f"  • {rec}")
                
        else:
            print('❌ Error:', result.get('error'))
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_optimizer() 