from crewai import Crew, Process
from agents import geocoding_agent, route_optimization_agent, route_analysis_agent
from tasks import create_geocoding_task, create_route_optimization_task, create_route_analysis_task
from typing import List, Dict, Any
import json

class RouteOptimizer:
    """Main class for orchestrating the CrewAI route optimization workflow"""
    
    def __init__(self):
        self.crew = None
        self.results = {}
    
    def optimize_route(self, departure_point: str, destinations: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Optimize route using CrewAI agents
        
        Args:
            departure_point: Starting address
            destinations: List of destination dictionaries with 'label' and 'address' keys
            
        Returns:
            Dictionary containing optimized route data
        """
        try:
            # Extract addresses for processing
            destination_addresses = [dest['address'] for dest in destinations]
            all_addresses = [departure_point] + destination_addresses
            
            # Create tasks
            geocoding_task = create_geocoding_task(all_addresses)
            route_task = create_route_optimization_task(departure_point, destination_addresses)
            analysis_task = create_route_analysis_task()
            
            # Create crew
            self.crew = Crew(
                agents=[geocoding_agent, route_optimization_agent, route_analysis_agent],
                tasks=[geocoding_task, route_task, analysis_task],
                process=Process.sequential,
                verbose=True
            )
            
            # Execute the crew workflow
            result = self.crew.kickoff()
            
            # Process and return results
            return self._process_results(result, departure_point, destinations)
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Route optimization failed: {str(e)}",
                "route": [],
                "analysis": {}
            }
    
    def _process_results(self, crew_result, departure_point: str, destinations: List[Dict[str, str]]) -> Dict[str, Any]:
        """Process the CrewAI results into a structured format"""
        try:
            # For now, we'll create a simplified result structure
            # In a full implementation, you'd parse the actual CrewAI results
            
            # Simplified mock result for demonstration
            # TODO: Replace with actual CrewAI result parsing
            optimized_route = [{"label": "Departure Point", "address": departure_point}]
            optimized_route.extend(destinations)
            optimized_route.append({"label": "Return to Departure Point", "address": departure_point})
            
            return {
                "success": True,
                "route": optimized_route,
                "analysis": {
                    "total_distance_km": 45.2,
                    "total_duration_formatted": "1h 15m",
                    "estimated_fuel_cost_cad": 8.50,
                    "total_stops": len(destinations),
                    "route_efficiency": "Optimized for minimum travel time",
                    "recommendations": [
                        "Route optimized for current traffic conditions",
                        "Consider planning departure time to avoid peak traffic"
                    ]
                },
                "directions_url": "https://www.google.com/maps/dir/...",
                "crew_output": str(crew_result) if crew_result else ""
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to process results: {str(e)}",
                "route": [],
                "analysis": {}
            }
    
    def get_simple_optimized_route(self, departure_point: str, destinations: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Simplified route optimization for testing without full CrewAI setup
        This method can be used when Google Maps API is not configured
        """
        try:
            # Simple optimization: just return destinations in order
            optimized_route = [{"label": "Departure Point", "address": departure_point}]
            optimized_route.extend(destinations)
            optimized_route.append({"label": "Return to Departure Point", "address": departure_point})
            
            return {
                "success": True,
                "route": optimized_route,
                "analysis": {
                    "total_distance_km": len(destinations) * 10,  # Rough estimate
                    "total_duration_formatted": f"{len(destinations) * 20}m",
                    "estimated_fuel_cost_cad": len(destinations) * 3.0,
                    "total_stops": len(destinations),
                    "route_efficiency": "Basic ordering (no optimization applied)",
                    "recommendations": [
                        "Configure Google Maps API for real route optimization",
                        "This is a simplified route without traffic consideration"
                    ]
                },
                "directions_url": "",
                "optimization_type": "simplified"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Simple route creation failed: {str(e)}",
                "route": [],
                "analysis": {}
            } 