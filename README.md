# AI Route Recommender

An AI-powered route optimization system built with Streamlit that helps users plan the most efficient route to visit multiple store locations.

## Features

- **Departure Point Configuration**: Pre-filled from config file, user-editable
- **Dynamic Store Selection**: Choose retailer and store number from dropdowns
- **Route Optimization**: Calculate the most efficient route using AI agents
- **Google Maps Integration**: External route links with turn-by-turn directions
- **Email Route Sharing**: Send route details with Notes-compatible attachments
- **iPhone Notes Integration**: Attachments open directly in Notes app

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure APIs**: 
   - Google Maps API in `config.yaml` (see [SETUP_GUIDE.md](SETUP_GUIDE.md))
   - Email settings in `config.yaml` (see [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md))

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## File Structure

```
route_recommender/
├── app.py                 # Main Streamlit application
├── config.yaml           # Configuration file (departure address)
├── config_loader.py       # Config file loader utility
├── data_loader.py         # CSV data loader and utilities
├── models.py              # Pydantic data models
├── requirements.txt       # Python dependencies
├── inputs/
│   └── store_list.csv    # Store data (retailer, store_number, address)
└── README.md             # This file
```

## Configuration

### config.yaml
Contains the default departure address:
```yaml
departure_address: "123 Main St, Vancouver, BC V6B 1A1, Canada"
```

### inputs/store_list.csv
Contains store information with columns:
- `retailer`: Store chain identifier (SDM, LD, SEP, REX)
- `store_number`: Unique store identifier
- `address`: Full store address

## Usage

1. **Set Departure Point**: The departure address is pre-filled from config but can be modified
2. **Add Destinations**: 
   - Select a retailer from the dropdown
   - Choose a store number (filtered by retailer)
   - Click "Add Destination"
3. **Create Route**: Once you have at least 2 destinations, click "Create Route"
4. **View Results**: See the optimized route order and click to open in Google Maps
5. **Share Route**: Email route with Notes-compatible attachment for iPhone

## Next Steps

- [ ] Integrate CrewAI for route optimization
- [x] Google Maps API integration for route optimization and external links
- [x] Email functionality with Notes-compatible attachments
- [x] Geocoding and route optimization with real-time traffic data
- [ ] Enhance route optimization algorithms

## Technology Stack

- **Frontend**: Streamlit
- **Data**: Pandas, Pydantic
- **Configuration**: PyYAML
- **AI**: CrewAI (to be integrated)
- **Maps**: Google Maps API (integrated for route optimization and external navigation) 