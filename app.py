import streamlit as st
from config_loader import load_config
from data_loader import load_store_data, get_unique_retailers, get_store_numbers_for_retailer, get_store_address
from direct_route_optimizer import DirectRouteOptimizer
from email_service import EmailService

# Page configuration
st.set_page_config(
    page_title="AI Route Recommender",
    page_icon="🗺️",
    layout="wide"
)

# Load config and data on startup
@st.cache_data
def load_app_data():
    """Load configuration and store data."""
    try:
        config = load_config()
        store_data = load_store_data()
        return config, store_data
    except FileNotFoundError as e:
        st.error(f"Error loading data: {e}")
        st.stop()

# Initialize session state
def init_session_state():
    """Initialize session state variables."""
    if "config" not in st.session_state or "store_data" not in st.session_state:
        config, store_data = load_app_data()
        st.session_state["config"] = config
        st.session_state["store_data"] = store_data
    
    if "departure_point" not in st.session_state:
        st.session_state["departure_point"] = st.session_state["config"].get("departure_address", "")
    
    if "destinations" not in st.session_state:
        st.session_state["destinations"] = []
    
    if "show_route" not in st.session_state:
        st.session_state["show_route"] = False
    
    if "route" not in st.session_state:
        st.session_state["route"] = []

# Initialize the app
init_session_state()

# --- UI Layout ---
st.title("🗺️ AI Route Recommender")

# Departure Point Section
st.subheader("📍 Departure Point")
departure_point = st.text_input(
    "Enter Departure Point Address",
    value=st.session_state["departure_point"],
    help="This address is pre-filled from config.yaml but can be changed"
)
st.session_state["departure_point"] = departure_point

# Add Destinations Section
st.subheader("🏪 Add Destinations")

col1, col2, col3 = st.columns([1, 1, 1], vertical_alignment="bottom")

with col1:
    # Get unique retailers from store data in specific order
    all_retailers = get_unique_retailers(st.session_state["store_data"])
    # Define the desired order
    preferred_order = ["SDM", "LD", "SEP", "REX"]
    # Sort retailers: preferred order first, then any others alphabetically
    retailers = [r for r in preferred_order if r in all_retailers] + [r for r in sorted(all_retailers) if r not in preferred_order]
    selected_retailer = st.selectbox("Retailer", retailers, key="retailer_select")

with col2:
    # Get store numbers for selected retailer
    if selected_retailer:
        store_numbers = get_store_numbers_for_retailer(st.session_state["store_data"], selected_retailer)
        selected_store_number = st.selectbox("Store Number", store_numbers, key="store_select")
    else:
        selected_store_number = None
        st.selectbox("Store Number", [], key="store_select", disabled=True)

with col3:
    add_button = st.button("➕ Add Destination", type="primary")

# Add destination logic
if add_button and selected_retailer and selected_store_number:
    # Lookup address from store data
    address = get_store_address(st.session_state["store_data"], selected_retailer, selected_store_number)
    if address:
        label = f"{selected_retailer} {selected_store_number}"
        
        # Check if this exact retailer + store_number combination already exists
        existing_store = any(
            dest["retailer"] == selected_retailer and dest["store_number"] == selected_store_number 
            for dest in st.session_state["destinations"]
        )
        
        # Check if this address is already in destinations (disallow duplicates)
        existing_address = any(
            dest["address"] == address 
            for dest in st.session_state["destinations"]
        )
        
        if existing_store:
            st.warning(f"⚠️ Store {label} is already in your destinations list!")
        elif existing_address:
            # Find which store already has this address
            existing_dest = next(dest for dest in st.session_state["destinations"] if dest["address"] == address)
            st.warning(f"⚠️ This address is already selected for {existing_dest['label']}. Please choose a different store location.")
        else:
            st.session_state["destinations"].append({
                "label": label,
                "address": address,
                "retailer": selected_retailer,
                "store_number": selected_store_number
            })
            st.success(f"✅ Added: {label}")
    else:
        st.error(f"❌ Could not find address for {selected_retailer} store {selected_store_number}. Please check the store data.")

# Selected Destinations Section
st.subheader("📋 Selected Destinations")

if st.session_state["destinations"]:
    for i, dest in enumerate(st.session_state["destinations"]):
        col1, col2, col3 = st.columns([2, 6, 1], vertical_alignment="center")
        
        with col1:
            st.write(f"**{dest['label']}**")
        
        with col2:
            st.write(dest["address"])
        
        with col3:
            if st.button("🗑️", key=f"remove_{i}", help="Remove destination"):
                st.session_state["destinations"].pop(i)
                st.rerun()
else:
    st.info("No destinations selected. Please add at least 2 destinations to create a route.")

# Create Route Section
st.subheader("🚗 Route Creation")

# Validation: Need at least 2 destinations and valid departure point
destinations_count = len(st.session_state["destinations"])
has_departure = bool(st.session_state["departure_point"].strip())
can_create_route = destinations_count >= 2 and has_departure

# Show route summary before creation
if destinations_count > 0:
    st.info(f"📍 Current route: Departure → {destinations_count} store(s) → Return to departure")

if can_create_route:
    if st.button("🗺️ Create Route", type="primary", use_container_width=True):
        # Initialize direct route optimizer (no CrewAI dependency)
        optimizer = DirectRouteOptimizer()
        
        with st.spinner("🔍 Optimizing route with Google Maps..."):
            try:
                # Use direct Google Maps optimization
                result = optimizer.optimize_route(
                    departure_point=st.session_state["departure_point"],
                    destinations=st.session_state["destinations"]
                )
                
                if result["success"]:
                    st.session_state["route"] = result["route"]
                    st.session_state["route_analysis"] = result["analysis"]
                    st.session_state["directions_url"] = result.get("directions_url", "")
                    st.session_state["show_route"] = True
                    
                    # Success message based on optimization type
                    if result.get("optimization_type") == "google_maps_direct":
                        st.success("✅ Route optimized using Google Maps with traffic-aware routing!")
                    else:
                        st.success("✅ Route created successfully!")
                else:
                    st.error(f"❌ Route optimization failed: {result.get('error', 'Unknown error')}")
                    
                    # Fallback to simplified optimization
                    st.warning("⚠️ Using simplified routing as fallback...")
                    route = [{"label": "Departure Point", "address": st.session_state["departure_point"]}]
                    route.extend(st.session_state["destinations"])
                    route.append({"label": "Return to Departure Point", "address": st.session_state["departure_point"]})
                    st.session_state["route"] = route
                    st.session_state["show_route"] = True
                    
            except Exception as e:
                st.error(f"❌ Error during route optimization: {str(e)}")
                # Emergency fallback
                st.warning("Using emergency fallback routing...")
                route = [{"label": "Departure Point", "address": st.session_state["departure_point"]}]
                route.extend(st.session_state["destinations"])
                route.append({"label": "Return to Departure Point", "address": st.session_state["departure_point"]})
                st.session_state["route"] = route
                st.session_state["show_route"] = True
else:
    st.button("🗺️ Create Route", disabled=True, use_container_width=True)
    
    # Specific validation messages
    if destinations_count == 0:
        st.warning("⚠️ Please add at least 2 destinations to create a route.")
    elif destinations_count == 1:
        st.warning("⚠️ Please add at least 1 more destination (minimum 2 required).")
    
    if not has_departure:
        st.warning("⚠️ Please enter a valid departure point address.")

# Route Display Section (hidden until route is created)
if st.session_state.get("show_route") and st.session_state["route"]:
    st.divider()
    
    # Route Analysis Section (New!)
    if st.session_state.get("route_analysis"):
        st.subheader("📊 Route Analysis")
        analysis = st.session_state["route_analysis"]
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns([3, 3, 4, 2])
        with col1:
            st.metric("Total Distance", f"{analysis.get('total_distance_km', 0)} km")
        with col2:
            st.metric("Travel Time", analysis.get('total_duration_formatted', 'N/A'))
        with col3:
            st.metric("Estimated Fuel Cost", f"${analysis.get('estimated_fuel_cost_cad', 0):.2f} CAD")
        with col4:
            st.metric("Total Stops", analysis.get('total_stops', 0))
        
        # Show efficiency info
        st.info(f"🎯 **Optimization:** {analysis.get('route_efficiency', 'Route optimized')}")
        
        # Show recommendations
        if analysis.get('recommendations'):
            st.subheader("💡 AI Recommendations")
            for rec in analysis['recommendations']:
                st.write(f"• {rec}")
    
    # Google Maps Link
    if st.session_state.get("directions_url"):
        st.subheader("🗺️ Interactive Map")
        st.markdown(f"[🔗 Open route in Google Maps]({st.session_state['directions_url']})")
    
    # Route information message
    if st.session_state.get("directions_url"):
        st.info("📍 Click the Google Maps link above to view the interactive route with turn-by-turn directions")
    else:
        st.info("📍 Configure Google Maps API for interactive route visualization")



    # Route Order Section
    st.subheader("📋 Optimized Route Order")
    
    for i, stop in enumerate(st.session_state["route"]):
        if i == 0:
            st.write(f"🟢 **Start:** {stop['address']}")
        elif i == len(st.session_state["route"]) - 1:
            st.write(f"🔴 **End:** {stop['address']}")
        else:
            st.write(f"📍 **Stop {i}:** {stop['label']} - {stop['address']}")

    # Email Route Section
    st.subheader("📧 Email Route")
    
    if st.button("📧 Send Email", use_container_width=True):
        try:
            # Initialize email service
            email_service = EmailService()
            
            with st.spinner("📧 Sending route email..."):
                # Send email with route data
                success = email_service.send_route_email(
                    route_data=st.session_state["route"],
                    analysis=st.session_state.get("route_analysis", {}),
                    directions_url=st.session_state.get("directions_url", "")
                )
                
                if success:
                    st.success("✅ Route emailed successfully!")
                    st.info("📱 Check your inbox for the route details and Notes-compatible attachment")
                else:
                    st.error("❌ Failed to send email. Please check your email configuration in config.yaml")
                    
        except ValueError as e:
            st.error(f"❌ Email configuration error: {str(e)}")
            st.info("💡 Please configure email settings in config.yaml file")
        except Exception as e:
            st.error(f"❌ Email sending failed: {str(e)}")

    # Reset Route Button
    st.subheader("🔄 Create New Route")
    if st.button("↪️ Start Over"):
        st.session_state["show_route"] = False
        st.session_state["route"] = []
        st.session_state["destinations"] = []  # Clear all selected destinations
        st.rerun()

# Sidebar with additional info
with st.sidebar:
    st.header("ℹ️ About")
    st.write("This AI Route Recommender helps you plan the most efficient route to visit multiple store locations.")
    
    # Store Data Summary
    st.header("🏪 Available Stores")
    total_stores = len(st.session_state["store_data"].stores)
    retailers = get_unique_retailers(st.session_state["store_data"])
    
    st.metric("Total Stores", total_stores)
    st.metric("Retailers", len(retailers))
    
    # Show store count by retailer
    for retailer in sorted(retailers):
        count = len(get_store_numbers_for_retailer(st.session_state["store_data"], retailer))
        st.write(f"• {retailer}: {count} stores")
    
    st.header("📊 Current Session")
    st.metric("Departure Point", "✅" if st.session_state["departure_point"] else "❌")
    st.metric("Destinations", len(st.session_state["destinations"]))
    st.metric("Route Created", "✅" if st.session_state.get("show_route") else "❌")
    
    if st.session_state["destinations"]:
        st.header("📋 Selected Stores")
        for dest in st.session_state["destinations"]:
            st.write(f"• {dest['label']}")

# Footer
st.divider()
st.caption("Powered by CrewAI and Streamlit 🚀")