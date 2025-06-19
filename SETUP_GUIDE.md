# AI Route Recommender Setup Guide

This guide will help you set up the complete AI Route Recommender with Google Maps API integration and CrewAI optimization.

## 🔧 Prerequisites

1. **Python 3.8+** installed on your system
2. **Google Cloud Platform account** (for Maps API)
3. **Internet connection** (for API calls)

## 📋 Step-by-Step Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Google Maps API Key

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a new project** or select existing one
3. **Enable APIs**:
   - Go to "APIs & Services" > "Library"
   - Enable these APIs:
     - Maps JavaScript API
     - Directions API
     - Geocoding API
     - Distance Matrix API
4. **Create API Key**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the generated API key
5. **Secure your API Key** (Recommended):
   - Click on your API key to edit it
   - Add application restrictions (HTTP referrers)
   - Add API restrictions (limit to Maps APIs only)

### 3. Configure the Application

1. **Edit `config.yaml`**:
   ```yaml
   departure_address: "201 Alvin Narod Mews, Vancouver, BC V6B 8P5"

   # API Configuration
   api_keys:
     google_maps: "YOUR_ACTUAL_API_KEY_HERE"  # Replace with your API key
     
   # Route Optimization Preferences
   route_preferences:
     optimize_for: "time"  # Options: "time", "distance", "fuel"
     avoid_tolls: false
     avoid_highways: false
     traffic_model: "best_guess"  # Options: "best_guess", "pessimistic", "optimistic"
   ```

2. **Replace the placeholder** `YOUR_ACTUAL_API_KEY_HERE` with your actual Google Maps API key

### 4. Test Your Setup

1. **Run the application**:
   ```bash
   streamlit run app.py
   ```

2. **Test basic functionality**:
   - Add 2+ destinations
   - Click "Create Route"
   - Check if route optimization works

## 🎯 Features Overview

### With Google Maps API Configured:
- ✅ **Real route optimization** using AI agents
- ✅ **Accurate time/distance calculations**
- ✅ **Traffic-aware routing**
- ✅ **Interactive Google Maps links**
- ✅ **Precise fuel cost estimates**

### Without API (Fallback Mode):
- ✅ **Basic route ordering**
- ✅ **Simplified time estimates**
- ✅ **Store selection and validation**
- ⚠️ **Limited optimization accuracy**

## 🚨 Troubleshooting

### Common Issues:

#### 1. "API Key Error"
```
ValueError: Please set a valid Google Maps API key in config.yaml
```
**Solution**: Ensure your API key is correctly set in `config.yaml`

#### 2. "API Not Enabled"
```
This API project is not authorized to use this API
```
**Solution**: Enable the required APIs in Google Cloud Console

#### 3. "Quota Exceeded"
```
You have exceeded your daily request quota
```
**Solution**: Check your API usage in Google Cloud Console and increase quotas if needed

#### 4. "Route Optimization Failed"
**Solution**: The app will automatically fall back to simplified routing

### 4. Getting Help

- Check the **sidebar metrics** in the app for diagnostics
- Look for **warning/error messages** in the app interface
- Review the **Google Cloud Console** for API usage and errors

## 💰 Cost Considerations

### Google Maps API Pricing (as of 2024):
- **Directions API**: $5 per 1,000 requests
- **Geocoding API**: $5 per 1,000 requests
- **Free tier**: $200 credit per month

### Cost Example:
- Creating 100 routes with 3 destinations each ≈ $3-4/month
- Well within the free tier for typical usage

## 🔒 Security Best Practices

1. **Restrict your API key** to specific APIs only
2. **Add HTTP referrer restrictions** if deploying publicly
3. **Monitor API usage** regularly
4. **Never commit API keys** to version control
5. **Use environment variables** in production

## 🚀 Advanced Configuration

### Custom Route Preferences:
Edit `config.yaml` to customize routing behavior:

```yaml
route_preferences:
  optimize_for: "distance"     # Prioritize shorter routes
  avoid_tolls: true           # Avoid toll roads
  avoid_highways: true        # Use local roads
  traffic_model: "pessimistic" # Account for heavy traffic
```

### Multiple Departure Points:
You can change the departure address in the UI or modify the default in `config.yaml`.

## 📞 Support

If you encounter issues:
1. Check this setup guide
2. Review error messages in the app
3. Verify your Google Cloud Console settings
4. Test with simplified routing first

---

**You're all set! Enjoy optimizing your routes with AI! 🎉** 