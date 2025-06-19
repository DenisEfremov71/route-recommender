import googlemaps
from typing import List, Dict, Any
import os
from config_loader import load_config

class GeocodingTool:
    """Tool for geocoding addresses using Google Maps API"""
    
    def __init__(self):
        config = load_config()
        api_key = config.get("api_keys", {}).get("google_maps")
        if not api_key or api_key == "YOUR_GOOGLE_MAPS_API_KEY" or api_key.startswith("YOUR_"):
            raise ValueError("Please set a valid Google Maps API key in config.yaml")
        self.gmaps = googlemaps.Client(key=api_key)
        self.name = "Address Geocoder"
        self.description = "Converts addresses to latitude/longitude coordinates using Google Maps Geocoding API"
    
    def _run(self, address: str) -> Dict[str, Any]:
        """Geocode a single address"""
        try:
            geocode_result = self.gmaps.geocode(address)
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                formatted_address = geocode_result[0]['formatted_address']
                return {
                    "success": True,
                    "address": address,
                    "formatted_address": formatted_address,
                    "lat": location['lat'],
                    "lng": location['lng'],
                    "coordinates": (location['lat'], location['lng'])
                }
            else:
                return {
                    "success": False,
                    "address": address,
                    "error": "Address not found"
                }
        except Exception as e:
            return {
                "success": False,
                "address": address,
                "error": str(e)
            }


class RouteOptimizationTool:
    """Tool for optimizing routes using Google Maps Directions API"""
    
    def __init__(self):
        config = load_config()
        api_key = config.get("api_keys", {}).get("google_maps")
        if not api_key or api_key == "YOUR_GOOGLE_MAPS_API_KEY" or api_key.startswith("YOUR_"):
            raise ValueError("Please set a valid Google Maps API key in config.yaml")
        self.gmaps = googlemaps.Client(key=api_key)
        self.config = config
        self.name = "Route Optimizer"
        self.description = "Optimizes route order for multiple destinations using Google Maps Directions API with waypoint optimization"
    
    def _run(self, origin: str, destinations: List[str], return_to_origin: bool = True) -> Dict[str, Any]:
        """Optimize route for multiple destinations"""
        try:
            route_prefs = self.config.get("route_preferences", {})
            
            # Prepare waypoints (all destinations except the last one if not returning to origin)
            if return_to_origin:
                waypoints = destinations
                destination = origin  # Return to origin
            else:
                waypoints = destinations[:-1] if len(destinations) > 1 else []
                destination = destinations[-1] if destinations else origin
            
            # Get directions with waypoint optimization
            directions_result = self.gmaps.directions(
                origin=origin,
                destination=destination,
                waypoints=waypoints,
                optimize_waypoints=True,
                mode="driving",
                avoid_tolls=route_prefs.get("avoid_tolls", False),
                avoid_highways=route_prefs.get("avoid_highways", False),
                traffic_model=route_prefs.get("traffic_model", "best_guess"),
                departure_time="now"
            )
            
            if not directions_result:
                return {
                    "success": False,
                    "error": "No route found"
                }
            
            route = directions_result[0]
            
            # Extract optimized waypoint order
            waypoint_order = route.get('waypoint_order', [])
            
            # Build optimized route
            optimized_route = [origin]
            
            # Add waypoints in optimized order
            for i in waypoint_order:
                if i < len(destinations):
                    optimized_route.append(destinations[i])
            
            # Add remaining destinations that weren't in waypoints
            if not return_to_origin and len(destinations) > len(waypoints):
                optimized_route.append(destinations[-1])
            elif return_to_origin:
                optimized_route.append(origin)
            
            # Calculate total time and distance
            total_duration = 0
            total_distance = 0
            
            for leg in route['legs']:
                total_duration += leg['duration']['value']  # in seconds
                total_distance += leg['distance']['value']  # in meters
            
            return {
                "success": True,
                "optimized_route": optimized_route,
                "waypoint_order": waypoint_order,
                "total_duration_seconds": total_duration,
                "total_duration_text": route['legs'][0]['duration']['text'] if route['legs'] else "0 mins",
                "total_distance_meters": total_distance,
                "total_distance_text": route['legs'][0]['distance']['text'] if route['legs'] else "0 km",
                "directions_url": self._generate_google_maps_url(optimized_route),
                "detailed_directions": route
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_google_maps_url(self, route_addresses: List[str]) -> str:
        """Generate a Google Maps URL for the optimized route"""
        if len(route_addresses) < 2:
            return ""
        
        origin = route_addresses[0]
        destination = route_addresses[-1]
        waypoints = route_addresses[1:-1] if len(route_addresses) > 2 else []
        
        base_url = "https://www.google.com/maps/dir/"
        url = base_url + origin.replace(" ", "+")
        
        for waypoint in waypoints:
            url += "/" + waypoint.replace(" ", "+")
        
        if destination != origin:
            url += "/" + destination.replace(" ", "+")
        
        return url


class RouteAnalysisTool:
    """Tool for analyzing route efficiency and providing insights"""
    
    def __init__(self):
        self.name = "Route Analyzer"
        self.description = "Analyzes route efficiency and provides insights about the optimized route"
    
    def _run(self, route_data: Dict[str, Any], addresses: List[str]) -> Dict[str, Any]:
        """Analyze route and provide insights"""
        try:
            if not route_data.get("success"):
                return {
                    "success": False,
                    "error": "Invalid route data provided"
                }
            
            total_duration = route_data.get("total_duration_seconds", 0)
            total_distance = route_data.get("total_distance_meters", 0)
            
            # Convert to human-readable format
            hours = total_duration // 3600
            minutes = (total_duration % 3600) // 60
            duration_formatted = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
            
            distance_km = total_distance / 1000
            
            # Estimate fuel cost (rough calculation)
            # Assuming average car fuel consumption: 8L/100km, gas price: $1.50/L
            fuel_consumption_per_100km = 8  # liters
            gas_price_per_liter = 1.50  # CAD
            estimated_fuel_cost = (distance_km / 100) * fuel_consumption_per_100km * gas_price_per_liter
            
            analysis = {
                "success": True,
                "total_stops": len(addresses),
                "total_distance_km": round(distance_km, 2),
                "total_duration_formatted": duration_formatted,
                "estimated_fuel_cost_cad": round(estimated_fuel_cost, 2),
                "average_time_per_stop": f"{total_duration // len(addresses) // 60}m" if addresses else "0m",
                "route_efficiency": "Optimized for minimum travel time",
                "recommendations": []
            }
            
            # Add recommendations based on analysis
            if distance_km > 50:
                analysis["recommendations"].append("Consider grouping nearby stores for future trips")
            
            if total_duration > 3600:  # More than 1 hour
                analysis["recommendations"].append("Plan breaks during this lengthy route")
            
            if len(addresses) > 5:
                analysis["recommendations"].append("Consider splitting into multiple shorter trips")
            
            return analysis
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 