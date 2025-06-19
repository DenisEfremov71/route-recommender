from email_service import EmailService

def test_email_service():
    """Test email service configuration and functionality"""
    print("🧪 Testing Email Service...")
    print("=" * 50)
    
    try:
        # Initialize email service
        email_service = EmailService()
        print("✅ Email service initialized successfully")
        
        # Test configuration
        config_test = email_service.test_email_configuration()
        if config_test["success"]:
            print("✅ Email configuration is valid")
        else:
            print(f"❌ Email configuration error: {config_test['message']}")
            return False
        
        # Test with sample route data
        sample_route = [
            {"label": "Departure Point", "address": "Vancouver, BC"},
            {"label": "SDM 0203", "address": "1301 Main St, Penticton, BC V2A 5E9"},
            {"label": "LD 0003", "address": "100 - 555 Sixth Street, New Westminster, BC V3L 5H1"},
            {"label": "Return to Departure Point", "address": "Vancouver, BC"}
        ]
        
        sample_analysis = {
            "total_distance_km": 839.86,
            "total_duration_formatted": "9h 7m",
            "estimated_fuel_cost_cad": 107.50,
            "total_stops": 2,
            "route_efficiency": "Optimized by Google Maps for distance",
            "recommendations": [
                "Consider planning fuel stops for this long journey",
                "Plan rest breaks during this lengthy route",
                "Route optimized using real-time traffic data"
            ]
        }
        
        sample_directions_url = "https://www.google.com/maps/dir/Vancouver%2C+BC/1301+Main+St%2C+Penticton%2C+BC+V2A+5E9/100+-+555+Sixth+Street%2C+New+Westminster%2C+BC+V3L+5H1/Vancouver%2C+BC"
        
        # Test file creation
        file_path = email_service.create_route_notes_file(sample_route, sample_analysis)
        print(f"✅ Route notes file created: {file_path}")
        
        # Show file content preview
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print("\n📋 File Content Preview:")
            print("-" * 30)
            print(content[:300] + "..." if len(content) > 300 else content)
        
        # Clean up test file
        import os
        os.unlink(file_path)
        print("✅ Test file cleaned up")
        
        # Ask user if they want to send a test email
        print("\n🚀 Email service is ready!")
        
        send_test = input("\nDo you want to send a test email? (y/n): ").lower().strip()
        
        if send_test == 'y':
            print("\n📧 Sending test email...")
            success = email_service.send_route_email(sample_route, sample_analysis, sample_directions_url)
            
            if success:
                print("✅ Test email sent successfully!")
                print("📱 Check your inbox and the Notes app compatibility")
            else:
                print("❌ Failed to send test email")
                return False
        else:
            print("⏭️ Skipping test email send")
        
        return True
        
    except Exception as e:
        print(f"❌ Email service test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_email_service() 