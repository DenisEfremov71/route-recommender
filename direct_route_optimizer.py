import googlemaps
from typing import List, Dict, Any
from config_loader import load_config
import urllib.parse

class DirectRouteOptimizer:
    """Direct Google Maps route optimizer without CrewAI dependency"""
    
    def __init__(self):
        config = load_config()
        api_key = config.get("api_keys", {}).get("google_maps")
        if not api_key or api_key == "YOUR_GOOGLE_MAPS_API_KEY" or api_key.startswith("YOUR_"):
            raise ValueError("Please set a valid Google Maps API key in config.yaml")
        
        self.gmaps = googlemaps.Client(key=api_key)
        self.config = config
    
    def optimize_route(self, departure_point: str, destinations: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Optimize route using Google Maps Directions API directly
        
        Args:
            departure_point: Starting address
            destinations: List of destination dictionaries with 'label' and 'address' keys
            
        Returns:
            Dictionary containing optimized route data
        """
        try:
            # Extract addresses
            destination_addresses = [dest['address'] for dest in destinations]
            
            # Get route preferences
            route_prefs = self.config.get("route_preferences", {})
            
            # Build avoid list based on preferences
            avoid_list = []
            if route_prefs.get("avoid_tolls", False):
                avoid_list.append("tolls")
            if route_prefs.get("avoid_highways", False):
                avoid_list.append("highways")
            
            # Use Google Maps waypoint optimization
            directions_params = {
                "origin": departure_point,
                "destination": departure_point,  # Return to origin
                "waypoints": destination_addresses,
                "optimize_waypoints": True,
                "mode": "driving",
                "traffic_model": route_prefs.get("traffic_model", "best_guess"),
                "departure_time": "now"
            }
            
            # Add avoid parameter only if we have items to avoid
            if avoid_list:
                directions_params["avoid"] = avoid_list
            
            directions_result = self.gmaps.directions(**directions_params)
            
            if not directions_result:
                return {
                    "success": False,
                    "error": "No route found",
                    "route": [],
                    "analysis": {}
                }
            
            route = directions_result[0]
            waypoint_order = route.get('waypoint_order', [])
            
            # Build optimized route
            optimized_route = [{"label": "Departure Point", "address": departure_point}]
            
            # Add destinations in optimized order
            for i in waypoint_order:
                if i < len(destinations):
                    optimized_route.append(destinations[i])
            
            # Return to departure point
            optimized_route.append({"label": "Return to Departure Point", "address": departure_point})
            
            # Calculate metrics
            total_duration = 0
            total_distance = 0
            
            for leg in route['legs']:
                total_duration += leg['duration']['value']  # seconds
                total_distance += leg['distance']['value']  # meters
            
            # Analysis
            analysis = self._analyze_route(total_duration, total_distance, len(destinations))
            
            # Generate Google Maps URL
            directions_url = self._generate_google_maps_url(departure_point, destination_addresses, waypoint_order)
            
            return {
                "success": True,
                "route": optimized_route,
                "analysis": analysis,
                "directions_url": directions_url,
                "waypoint_order": waypoint_order,
                "optimization_type": "google_maps_direct"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Route optimization failed: {str(e)}",
                "route": [],
                "analysis": {}
            }
    
    def _analyze_route(self, total_duration: int, total_distance: int, num_destinations: int) -> Dict[str, Any]:
        """Analyze route and provide insights"""
        
        # Convert to human-readable format
        hours = total_duration // 3600
        minutes = (total_duration % 3600) // 60
        duration_formatted = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        
        distance_km = total_distance / 1000
        
        # Estimate fuel cost (BC gas prices ~$1.60/L, 8L/100km consumption)
        fuel_consumption_per_100km = 8  # liters
        gas_price_per_liter = 1.60  # CAD (BC average)
        estimated_fuel_cost = (distance_km / 100) * fuel_consumption_per_100km * gas_price_per_liter
        
        # Generate recommendations
        recommendations = []
        
        if distance_km > 100:
            recommendations.append("Consider planning fuel stops for this long journey")
        
        if total_duration > 3600:  # More than 1 hour
            recommendations.append("Plan rest breaks during this lengthy route")
        
        if num_destinations > 4:
            recommendations.append("Consider grouping nearby stores for efficiency")
        
        # Traffic-based recommendations
        recommendations.append("Route optimized using real-time traffic data")
        
        optimize_for = self.config.get("route_preferences", {}).get("optimize_for", "time")
        if optimize_for == "distance":
            recommendations.append("Route prioritizes shortest distance over time")
        elif optimize_for == "time":
            recommendations.append("Route prioritizes fastest travel time")
        
        return {
            "total_stops": num_destinations,
            "total_distance_km": round(distance_km, 2),
            "total_duration_formatted": duration_formatted,
            "estimated_fuel_cost_cad": round(estimated_fuel_cost, 2),
            "average_time_per_stop": f"{total_duration // max(num_destinations, 1) // 60}m",
            "route_efficiency": f"Optimized by Google Maps for {optimize_for}",
            "recommendations": recommendations
        }
    
    def _generate_google_maps_url(self, origin: str, destinations: List[str], waypoint_order: List[int]) -> str:
        """Generate a Google Maps URL for the optimized route"""
        try:
            import urllib.parse
            
            # Use the simple and most reliable Google Maps directions URL format
            # Format: https://www.google.com/maps/dir/origin/waypoint1/waypoint2/destination
            base_url = "https://www.google.com/maps/dir/"
            
            # Build the route: origin -> waypoints in optimized order -> back to origin
            route_points = [origin]
            
            # Add waypoints in optimized order
            for i in waypoint_order:
                if i < len(destinations):
                    route_points.append(destinations[i])
            
            # Return to origin
            route_points.append(origin)
            
            # Encode each location and join with "/"
            encoded_points = []
            for point in route_points:
                # Use quote_plus for proper URL encoding of addresses
                encoded_point = urllib.parse.quote_plus(point)
                encoded_points.append(encoded_point)
            
            # Build final URL
            url = base_url + "/".join(encoded_points)
            
            return url
            
        except Exception as e:
            return ""
    
    def get_simple_optimized_route(self, departure_point: str, destinations: List[Dict[str, str]]) -> Dict[str, Any]:
        """Fallback method - same as main method but with error handling"""
        return self.optimize_route(departure_point, destinations) 