from crewai import Task
from agents import geocoding_agent, route_optimization_agent, route_analysis_agent

def create_geocoding_task(addresses):
    """Create a task for geocoding all addresses"""
    return Task(
        description=f"""
        Geocode the following addresses to obtain precise coordinates:
        
        Addresses to geocode: {addresses}
        
        For each address:
        1. Convert to latitude/longitude coordinates
        2. Validate the address format and accuracy
        3. Return formatted address information
        4. Flag any addresses that cannot be geocoded
        
        Ensure all coordinates are accurate for route optimization.
        """,
        agent=geocoding_agent,
        expected_output="""A JSON object containing geocoded information for each address, 
        including coordinates, formatted addresses, and any validation warnings."""
    )

def create_route_optimization_task(origin, destinations):
    """Create a task for optimizing the route"""
    return Task(
        description=f"""
        Calculate the most efficient route for the following trip:
        
        Origin: {origin}
        Destinations: {destinations}
        
        Requirements:
        1. Find the optimal order to visit all destinations
        2. Return to the origin point at the end
        3. Minimize total travel time considering current traffic
        4. Consider fuel efficiency in the optimization
        5. Generate a Google Maps URL for the optimized route
        
        Use real-time traffic data and Google Maps waypoint optimization.
        """,
        agent=route_optimization_agent,
        expected_output="""A JSON object containing the optimized route order, 
        total travel time, distance, and a shareable Google Maps URL."""
    )

def create_route_analysis_task():
    """Create a task for analyzing the optimized route"""
    return Task(
        description="""
        Analyze the optimized route and provide comprehensive insights:
        
        1. Calculate total distance and estimated travel time
        2. Estimate fuel costs based on current gas prices
        3. Provide efficiency metrics (time per stop, etc.)
        4. Generate actionable recommendations for the user
        5. Identify potential improvements or considerations
        
        Focus on practical insights that help the user understand the 
        cost and time implications of their route.
        """,
        agent=route_analysis_agent,
        expected_output="""A comprehensive analysis including travel metrics, 
        cost estimates, and practical recommendations for the trip."""
    ) 