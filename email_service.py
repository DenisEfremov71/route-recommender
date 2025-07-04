import smtplib
import os
import tempfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict, Any
from datetime import datetime
from config_loader import load_config

class EmailService:
    """Service for sending route emails with attachments"""
    
    def __init__(self):
        config = load_config()
        self.email_config = config.get("email", {})
        
        # Validate email configuration
        required_fields = ["recipient", "sender_email", "sender_password", "smtp_server", "smtp_port"]
        for field in required_fields:
            if not self.email_config.get(field) or str(self.email_config.get(field)).startswith("your-"):
                raise ValueError(f"Please configure email.{field} in config.yaml")
    
    def create_route_notes_file(self, route_data: List[Dict[str, str]], analysis: Dict[str, Any]) -> str:
        """
        Create an RTF file with clickable addresses that open Google Maps
        Returns the file path of the created file
        """
        import urllib.parse
        
        # Start RTF document with proper formatting
        rtf_content = r"{\rtf1\ansi\deff0 {\fonttbl {\f0 Arial;}}{\colortbl;\red0\green0\blue255;}\f0\fs48"
        rtf_content += "\n"
        
        # Add only the actual store stops (skip departure and return points)
        for i, stop in enumerate(route_data):
            # Skip the departure point (first) and return point (last)
            if i == 0 or i == len(route_data) - 1:
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
        
        # Create temporary RTF file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.rtf', delete=False, encoding='utf-8')
        temp_file.write(rtf_content)
        temp_file.close()
        
        return temp_file.name
    
    def send_route_email(self, route_data: List[Dict[str, str]], analysis: Dict[str, Any], directions_url: str = "") -> bool:
        """
        Send route email with Notes-compatible attachment
        Returns True if successful, False otherwise
        """
        try:
            # Create the route file
            route_file_path = self.create_route_notes_file(route_data, analysis)
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = self.email_config['recipient']
            msg['Subject'] = f"🗺️ Your Optimized Route - {datetime.now().strftime('%Y-%m-%d')}"
            
            # Email body
            body = f"""Hello!

Your optimized route has been generated and is ready to use.

📊 ROUTE SUMMARY:
• Total Distance: {analysis.get('total_distance_km', 'N/A')} km
• Travel Time: {analysis.get('total_duration_formatted', 'N/A')}
• Estimated Fuel Cost: ${analysis.get('estimated_fuel_cost_cad', 0):.2f} CAD
• Total Stops: {analysis.get('total_stops', 0)}

📋 STORE LOCATIONS:
The attached file contains your store list with clickable addresses that open directly in Google Maps on your iPhone.

🗺️ COMPLETE ROUTE:
{directions_url if directions_url else 'Google Maps link not available'}

Click the link above to open the complete optimized route with turn-by-turn directions.

---
Generated by AI Route Recommender
Powered by Google Maps API
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach the route file
            filename = f"Store_Locations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.rtf"
            
            with open(route_file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}',
            )
            msg.attach(part)
            
            # Send the email
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()  # Enable security
            server.login(self.email_config['sender_email'], self.email_config['sender_password'])
            text = msg.as_string()
            server.sendmail(self.email_config['sender_email'], self.email_config['recipient'], text)
            server.quit()
            
            # Clean up temporary file
            os.unlink(route_file_path)
            
            return True
            
        except Exception as e:
            # Clean up temporary file if it exists
            if 'route_file_path' in locals() and os.path.exists(route_file_path):
                os.unlink(route_file_path)
            
            print(f"Email sending failed: {str(e)}")
            return False
    
    def test_email_configuration(self) -> Dict[str, Any]:
        """
        Test email configuration
        Returns a dictionary with test results
        """
        try:
            # Test SMTP connection
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['sender_email'], self.email_config['sender_password'])
            server.quit()
            
            return {
                "success": True,
                "message": "Email configuration is valid and ready to use"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Email configuration error: {str(e)}"
            } 