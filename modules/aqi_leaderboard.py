import random

def get_aqi_leaderboard():
    """
    Generate AQI data for major Indian cities and return best/worst rankings
    
    Returns:
        dict: Contains 'best' and 'worst' lists of cities with their AQI values
    """
    # List of major Indian cities
    cities = [
        # Major metros
        "Delhi", "Mumbai", "Kolkata", "Chennai", "Bangalore", "Hyderabad", 
        # North India
        "Lucknow", "Kanpur", "Agra", "Jaipur", "Chandigarh", "Amritsar", "Varanasi",
        # South India
        "Kochi", "Coimbatore", "Mysore", "Visakhapatnam", "Thiruvananthapuram", "Madurai",
        # East India
        "Patna", "Guwahati", "Bhubaneswar", "Ranchi", "Siliguri",
        # West India
        "Ahmedabad", "Surat", "Pune", "Nagpur", "Indore", "Bhopal"
    ]
    
    # Generate realistic AQI values for each city
    city_aqi_data = {}
    
    # Cities with typically high pollution
    high_pollution_cities = ["Delhi", "Kanpur", "Lucknow", "Patna", "Agra", "Varanasi"]
    # Cities with typically lower pollution
    low_pollution_cities = ["Kochi", "Mysore", "Thiruvananthapuram", "Coimbatore", "Visakhapatnam"]
    
    for city in cities:
        if city in high_pollution_cities:
            # Higher base AQI for typically polluted cities
            base_aqi = random.randint(150, 280)
        elif city in low_pollution_cities:
            # Lower base AQI for typically cleaner cities
            base_aqi = random.randint(30, 90)
        else:
            # Medium base AQI for other cities
            base_aqi = random.randint(70, 180)
            
        # Add some randomness
        variation = random.randint(-20, 20)
        aqi = max(0, min(500, base_aqi + variation))
        
        # Determine AQI category
        if aqi <= 50:
            category = "Good"
            color = "green"
        elif aqi <= 100:
            category = "Moderate"
            color = "#B7950B"  # Dark yellow
        elif aqi <= 200:
            category = "Unhealthy"
            color = "orange"
        elif aqi <= 300:
            category = "Very Unhealthy"
            color = "red"
        else:
            category = "Hazardous"
            color = "purple"
            
        city_aqi_data[city] = {
            "aqi": aqi,
            "category": category,
            "color": color
        }
    
    # Sort cities by AQI
    sorted_cities = sorted(city_aqi_data.items(), key=lambda x: x[1]["aqi"])
    
    # Get top 10 best (lowest AQI) and worst (highest AQI) cities
    best_cities = sorted_cities[:10]
    worst_cities = sorted_cities[-10:]
    worst_cities.reverse()  # Reverse to show highest AQI first
    
    # Format the data for display
    best_list = [{"city": city, "aqi": data["aqi"], "category": data["category"], "color": data["color"]} 
                for city, data in best_cities]
    worst_list = [{"city": city, "aqi": data["aqi"], "category": data["category"], "color": data["color"]} 
                 for city, data in worst_cities]
    
    return {
        "best": best_list,
        "worst": worst_list
    }