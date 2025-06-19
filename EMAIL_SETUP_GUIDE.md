# Email Setup Guide for Route Recommender

This guide will help you configure email functionality to send optimized routes directly to your inbox with Notes-compatible attachments.

## 📧 Email Features

- **Automatic Email Sending**: Click "Email Route" to send route details instantly
- **Notes App Compatibility**: Attachments open directly in iPhone Notes app
- **Complete Route Information**: Distance, time, cost, recommendations, and Google Maps link
- **Professional Formatting**: Clean, organized email layout

## 🔧 Gmail Setup (Recommended)

### 1. Enable 2-Factor Authentication
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable "2-Step Verification" if not already enabled

### 2. Generate App Password
1. In Google Account Security, click "2-Step Verification"
2. Scroll down to "App passwords"
3. Click "Select app" → "Other (Custom name)"
4. Enter: "Route Recommender"
5. Click "Generate"
6. **Copy the 16-character password** (you'll need this)

### 3. Configure config.yaml

Update your `config.yaml` file with your email settings:

```yaml
# Email Configuration
email:
  recipient: "your-recipient@gmail.com"     # Where to send routes
  smtp_server: "smtp.gmail.com"            # Gmail SMTP server
  smtp_port: 587                           # Gmail SMTP port
  sender_email: "your-sender@gmail.com"    # Your Gmail address
  sender_password: "abcd efgh ijkl mnop"   # Your 16-character App Password
```

### 4. Important Notes

- **Use App Password**: Never use your regular Gmail password
- **Sender Email**: Must be the same Gmail account that generated the App Password
- **Recipient Email**: Can be any email address (Gmail, iCloud, etc.)
- **Security**: App passwords are specific to this application

## 🧪 Testing Email Configuration

Run the email test to verify your setup:

```bash
python test_email_service.py
```

### Expected Output:
```
🧪 Testing Email Service...
==================================================
✅ Email service initialized successfully
✅ Email configuration is valid
✅ Route notes file created: /tmp/tmpXXXXXX.txt

📋 File Content Preview:
------------------------------
📍 AI Route Recommendation
Generated: 2024-01-15 14:30:00

🚗 ROUTE SUMMARY
==================================================
Total Distance: 839.86 km
Travel Time: 9h 7m
...

🚀 Email service is ready!

Do you want to send a test email? (y/n):
```

## 📱 iPhone Notes Integration

The attached `.txt` files are specifically formatted to work perfectly with iPhone Notes:

- **Direct Import**: Tap the attachment to open in Notes
- **Formatted Content**: Emojis and structure preserved
- **Searchable**: All route details are searchable in Notes
- **Shareable**: Easily share routes from Notes to others

## 🔒 Security Best Practices

1. **App Passwords**: Only use App Passwords, never your main password
2. **Limited Scope**: App passwords only work for this specific application
3. **Revoke Access**: You can revoke App Passwords anytime in Google Account settings
4. **Environment Variables**: For production, consider using environment variables

## 🚨 Troubleshooting

### "Authentication failed" Error
- Double-check your App Password (16 characters with spaces)
- Ensure 2-Factor Authentication is enabled
- Verify the sender email matches the App Password account

### "SMTP connection failed" Error
- Check internet connection
- Verify SMTP settings (smtp.gmail.com:587)
- Try temporarily disabling firewall/VPN

### "Email configuration error" 
- Ensure all fields in config.yaml are filled out
- Remove any placeholder text like "your-email@gmail.com"
- Check YAML formatting (proper indentation)

### Config File Template

Copy this template to your `config.yaml`:

```yaml
departure_address: "Your departure address here"

# API Configuration
api_keys:
  google_maps: "YOUR_GOOGLE_MAPS_API_KEY"

# Email Configuration
email:
  recipient: ""                    # Email to receive routes
  smtp_server: "smtp.gmail.com"   # Don't change this for Gmail
  smtp_port: 587                  # Don't change this for Gmail  
  sender_email: ""                # Your Gmail address
  sender_password: ""             # Your 16-character App Password

# Route Optimization Preferences
route_preferences:
  optimize_for: "distance"
  avoid_tolls: false
  avoid_highways: false
  traffic_model: "best_guess"
```

## 🎯 Usage in App

Once configured:

1. Create your optimized route
2. Click "📧 Email Route" 
3. Wait for "✅ Route emailed successfully!" message
4. Check your inbox for the route email with attachment
5. On iPhone: Tap attachment → "Copy to Notes" → Opens in Notes app

## 💰 Cost

- **Gmail SMTP**: Free for personal use
- **No additional charges** for sending route emails
- **No limits** on number of routes you can email

---

**Need Help?** If you encounter issues, verify your App Password setup and ensure all config.yaml fields are properly filled out. 