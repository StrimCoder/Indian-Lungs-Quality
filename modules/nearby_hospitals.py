import folium
import random
import streamlit as st
from streamlit_folium import folium_static

# In a real implementation, you would use this API key with Google Places API
# GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"

def get_city_coordinates(city):
    """Get approximate coordinates for major Indian cities"""
    city_coords = {
        "Mumbai": [19.0760, 72.8777],
        "Delhi": [28.6139, 77.2090],
        "Bangalore": [12.9716, 77.5946],
        "Kolkata": [22.5726, 88.3639],
        "Chennai": [13.0827, 80.2707],
        "Hyderabad": [17.3850, 78.4867],
        "Pune": [18.5204, 73.8567],
        "Ahmedabad": [23.0225, 72.5714],
        "Jaipur": [26.9124, 75.7873],
        "Lucknow": [26.8467, 80.9462],
        "Kanpur": [26.4499, 80.3319],
        "Nagpur": [21.1458, 79.0882],
        "Indore": [22.7196, 75.8577],
        "Thane": [19.2183, 72.9781],
        "Bhopal": [23.2599, 77.4126],
        "Visakhapatnam": [17.6868, 83.2185],
        "Patna": [25.5941, 85.1376],
        "Vadodara": [22.3072, 73.1812],
        "Ghaziabad": [28.6692, 77.4538],
        "Ludhiana": [30.9010, 75.8573],
        "Agra": [27.1767, 78.0081],
        "Nashik": [19.9975, 73.7898],
        "Ranchi": [23.3441, 85.3096],
        "Coimbatore": [11.0168, 76.9558],
        "Kochi": [9.9312, 76.2673],
        "Mysore": [12.2958, 76.6394],
        "Guwahati": [26.1445, 91.7362],
        "Bhubaneswar": [20.2961, 85.8245],
        "Thiruvananthapuram": [8.5241, 76.9366],
        "Amritsar": [31.6340, 74.8723],
        "Varanasi": [25.3176, 82.9739],
        "Srinagar": [34.0837, 74.7973],
        "Chandigarh": [30.7333, 76.7794],
        "Jodhpur": [26.2389, 73.0243],
        "Madurai": [9.9252, 78.1198],
        "Siliguri": [26.7271, 88.3953]
    }
    
    return city_coords.get(city, [20.5937, 78.9629])  # Default to center of India if city not found

def generate_nearby_hospitals(lat, lng, count=10):
    """Generate mock hospital data around the given coordinates"""
    hospitals = []
    
    hospital_types = [
        "General Hospital", "Respiratory Care Center", "Pulmonary Clinic", 
        "Multi-Specialty Hospital", "Medical College Hospital", "Community Health Center",
        "Chest & TB Hospital", "ENT Specialty Hospital", "Emergency Care Center"
    ]
    
    for i in range(count):
        # Generate a random offset (within ~3km)
        lat_offset = random.uniform(-0.03, 0.03)
        lng_offset = random.uniform(-0.03, 0.03)
        
        # Generate a hospital name
        name_prefix = random.choice([
            "City", "Metro", "Central", "Apollo", "Fortis", "Max", "Medanta", 
            "Artemis", "Narayana", "AIIMS", "Manipal", "Columbia Asia", "Wockhardt",
            "Lilavati", "Jaslok", "Kokilaben", "Ruby Hall", "Tata Memorial", "Hinduja"
        ])
        
        name_suffix = random.choice([
            "Hospital", "Medical Center", "Healthcare", "Clinic", "Institute", 
            "Super Specialty Hospital", "Memorial Hospital"
        ])
        
        hospital_name = f"{name_prefix} {name_suffix}"
        hospital_type = random.choice(hospital_types)
        
        # Generate a rating between 3.0 and 5.0
        rating = round(random.uniform(3.0, 5.0), 1)
        
        hospitals.append({
            "name": hospital_name,
            "lat": lat + lat_offset,
            "lng": lng + lng_offset,
            "rating": rating,
            "type": hospital_type,
            "address": f"123 Hospital Road, {random.randint(100000, 999999)}"
        })
    
    return hospitals

def create_hospital_map(city, aqi_level):
    """Create a map with nearby hospitals if AQI is severe"""
    # Only show hospitals if AQI is Very Unhealthy or Hazardous
    if aqi_level < 201:  # Below "Very Unhealthy" threshold
        return None
        
    # Get city coordinates
    lat, lng = get_city_coordinates(city)
    
    # Create a map centered on the city
    m = folium.Map(location=[lat, lng], zoom_start=12, 
                  tiles="cartodbpositron")
    
    # Add a marker for the city center
    folium.Marker(
        [lat, lng],
        popup=f"<b>{city}</b>",
        tooltip=city,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)
    
    # Generate and add hospital markers
    hospitals = generate_nearby_hospitals(lat, lng)
    
    for hospital in hospitals:
        # HTML for the popup
        popup_html = f"""
        <div style="width: 200px">
            <h4>{hospital['name']}</h4>
            <p><b>Type:</b> {hospital['type']}</p>
            <p><b>Rating:</b> {'⭐' * int(hospital['rating'])} {hospital['rating']}/5</p>
            <p><b>Address:</b> {hospital['address']}</p>
        </div>
        """
        
        # Add marker
        folium.Marker(
            [hospital['lat'], hospital['lng']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=hospital['name'],
            icon=folium.Icon(color="red", icon="plus", prefix="fa")
        ).add_to(m)
    
    return m

def display_hospital_map(city, aqi):
    """Display the hospital map in Streamlit if AQI is severe"""
    if aqi > 200:  # Very Unhealthy or worse
        st.markdown(f"""
        <div style="background-color: rgba(255, 0, 0, 0.1); border-left: 5px solid #ff0000; 
                    padding: 15px; border-radius: 10px; margin: 15px 0;">
            <h4 style="color: #ff0000; margin: 0 0 10px 0;">⚠️ Air Quality Health Warning</h4>
            <p style="margin: 0;">The current AQI level is {aqi}, which is considered 
            {'Very Unhealthy' if aqi <= 300 else 'Hazardous'}. 
            Below is a map of nearby hospitals and respiratory care centers that can assist with breathing issues.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create and display the map
        hospital_map = create_hospital_map(city, aqi)
        if hospital_map:
            folium_static(hospital_map, width=800, height=500)
            
            st.markdown("""
            <div style="font-size: 12px; color: #888; text-align: right; margin-top: -15px;">
                * Hospital locations are approximate and for demonstration purposes only.
            </div>
            """, unsafe_allow_html=True)
    
    return None