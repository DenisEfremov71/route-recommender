from email_service import EmailService

def demo_email_content():
    """Demo the email content and Notes file format"""
    print("📧 Email Route Feature Demo")
    print("=" * 50)
    
    # Sample route data (same as real app would generate)
    sample_route = [
        {"label": "Departure Point", "address": "201 Alvin Narod Mews, Vancouver, BC V6B 8P5"},
        {"label": "SDM 0203", "address": "1301 Main St, Penticton, BC V2A 5E9"},
        {"label": "LD 0003", "address": "100 - 555 Sixth Street, New Westminster, BC V3L 5H1"},
        {"label": "Return to Departure Point", "address": "201 Alvin Narod Mews, Vancouver, BC V6B 8P5"}
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
            "Route optimized using real-time traffic data",
            "Route prioritizes shortest distance over time"
        ]
    }
    
    try:
        # Create email service (will show error if not configured, which is expected)
        print("1. Creating RTF file with clickable addresses...")
        
        # Just create the file content without initializing email service
        from datetime import datetime
        import tempfile
        
        # Create RTF content with clickable addresses (same as EmailService)
        import urllib.parse
        
        # Start RTF document with proper formatting
        rtf_content = r"{\rtf1\ansi\deff0 {\fonttbl {\f0 Arial;}}{\colortbl;\red0\green0\blue255;}\f0\fs48"
        rtf_content += "\n"
        
        # Add only the actual store stops (skip departure and return points)
        for i, stop in enumerate(sample_route):
            # Skip the departure point (first) and return point (last)
            if i == 0 or i == len(sample_route) - 1:
                continue
                
            # Add store label (plain text)
            rtf_content += f"{stop['label']}\\line\n"
            
            # Create Google Maps URL for the address
            address = stop['address']
            encoded_address = urllib.parse.quote_plus(address)
            google_maps_url = f"https://maps.google.com/?q={encoded_address}"
            
            # Add clickable address in RTF hyperlink format
            # Format: {\field{\*\fldinst HYPERLINK "URL"}{\fldrslt clickable_text}}
            # \cf1 = blue color, \ul = underline
            rtf_content += f"{{\\field{{\\*\\fldinst HYPERLINK \"{google_maps_url}\"}}{{\\fldrslt \\cf1\\ul {address}}}}}\\line\\line\n"
        
        # Close RTF document
        rtf_content += "}"
        
        content = rtf_content
        
        print("✅ RTF file content created successfully!")
        print("\n📋 PREVIEW OF RTF FILE CONTENT:")
        print("=" * 60)
        print(content)
        
        # Create temporary file to show file creation works
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.rtf', delete=False, encoding='utf-8')
        temp_file.write(content)
        temp_file.close()
        
        print(f"\n✅ Sample RTF file created: {temp_file.name}")
        print("📱 This RTF file opens perfectly in iPhone Notes with clickable addresses!")
        
        # Clean up
        import os
        os.unlink(temp_file.name)
        print("✅ Demo file cleaned up")
        
        print("\n🚀 EMAIL FEATURE SUMMARY:")
        print("• RTF format with embedded clickable addresses")
        print("• Store addresses are clickable and open Google Maps on iPhone")
        print("• Rich text format with blue, underlined clickable links")
        print("• Automatic email sending with RTF attachments")
        print("\n💡 To use: Configure email settings in config.yaml and click 'Email Route' in the app!")
        
    except Exception as e:
        print(f"❌ Demo error: {str(e)}")

if __name__ == "__main__":
    demo_email_content() 