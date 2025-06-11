import streamlit as st
from modules.fetch_data import get_weather, get_aqi
from modules.aqi_gauge import create_aqi_gauge
from modules.animated_trend import animated_aqi_temp_chart
from modules.forecast import get_forecast
from modules.twitter_feed import get_twitter_feed
from modules.multi_city_chart import create_multi_city_chart
from modules.aqi_leaderboard import get_aqi_leaderboard
from modules.wind_compass import create_wind_compass
from datetime import datetime
import time
import random

st.set_page_config(page_title="🌆 INDIAN LUNGS QUALITY", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for stylish title
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');

.title-container {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #4776E6 100%);
    padding: 25px 20px;
    border-radius: 15px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    margin-bottom: 30px;
    text-align: center;
    position: relative;
    overflow: hidden;
    border: 2px solid rgba(255, 255, 255, 0.1);
}

.title-container::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    animation: shine 3s infinite;
}

@keyframes shine {
    0% { left: -100%; }
    100% { left: 100%; }
}

.main-title {
    font-family: 'Orbitron', sans-serif;
    color: white;
    font-size: 48px;
    font-weight: 700;
    text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.4);
    margin: 0;
    letter-spacing: 2px;
    background: linear-gradient(to right, #ffffff, #91EAE4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #e0e0e0;
    font-size: 18px;
    margin-top: 15px;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
    font-style: italic;
}

.lung-icon {
    font-size: 36px;
    vertical-align: middle;
    margin-right: 10px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}
</style>

<div class="title-container">
    <h1 class="main-title"><span class="lung-icon"></span> INDIAN LUNGS QUALITY</h1>
    <p class="subtitle">Real-time air quality monitoring across major Indian cities</p>
</div>
""", unsafe_allow_html=True)

# Custom CSS for dashboard components
st.markdown("""
<style>
.city-selector {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}

/* Twitter feed styling */
.tweet {
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
    border-left: 3px solid #1DA1F2;
}
.tweet-header {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}
.tweet-profile-image {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
}
.tweet-username {
    font-weight: bold;
    color: #E0E0E0;
}
.tweet-text {
    font-size: 14px;
    line-height: 1.4;
    margin-bottom: 10px;
}
.tweet-time {
    font-size: 12px;
    color: #888;
}
.twitter-header {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
}
.twitter-icon {
    font-size: 24px;
    margin-right: 10px;
    color: #1DA1F2;
}

/* Custom styling for text input */
div[data-baseweb="input"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

div[data-baseweb="input"] input {
    color: white !important;
    font-size: 16px !important;
}

div[data-baseweb="input"] input::placeholder {
    color: rgba(255, 255, 255, 0.5) !important;
}

div[data-baseweb="input"]:focus-within {
    border-color: #4776E6 !important;
    box-shadow: 0 0 0 2px rgba(71, 118, 230, 0.3) !important;
}

.stMetric {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    border-left: 4px solid #4776E6;
    transition: transform 0.3s ease;
}

.stMetric:hover {
    transform: translateY(-5px);
}

.chart-container {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    margin-top: 20px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.refresh-btn {
    text-align: center;
    margin: 20px 0;
}

/* Custom refresh button styling */
.custom-button {
    background: linear-gradient(135deg, #4776E6 0%, #8E54E9 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.custom-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
}

.custom-button:active {
    transform: translateY(1px);
}

.spin-icon {
    display: inline-block;
    animation: spin 2s infinite linear;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.city-title {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 10px;
    color: #4776E6;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Sidebar with Twitter feed
st.sidebar.markdown("""
<div class="twitter-header">
    <span class="twitter-icon">📰<span>
    <h3>Live AQI News Feed</h3>
</div>
""", unsafe_allow_html=True)

# Display tweets in sidebar
if 'tweets' in st.session_state:
    tweets = st.session_state.tweets
    if tweets:
        for tweet in tweets:
            # Format the date
            try:
                created_at = datetime.strptime(tweet['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                time_str = created_at.strftime("%b %d, %Y · %I:%M %p")
            except:
                time_str = "Just now"
                
            st.sidebar.markdown(f"""
            <div class="tweet">
                <div class="tweet-header">
                    <img src="{tweet['profile_image']}" class="tweet-profile-image" onerror="this.src='https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png'">
                    <span class="tweet-username">@{tweet['username']}</span>
                </div>
                <div class="tweet-text">{tweet['text']}</div>
                <div class="tweet-time">{time_str}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.sidebar.info("No tweets found for this location.")
else:
    st.sidebar.info("Loading tweets...")

# City input with custom styling
st.markdown('<div class="city-selector">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_city = st.text_input("", "Mumbai", placeholder="Enter any city in India...", help="Type any city name in India")
st.markdown('</div>', unsafe_allow_html=True)

# Display city name with styling
st.markdown(f'<div class="city-title">Current Air Quality in {selected_city}</div>', unsafe_allow_html=True)

# Auto-refresh functionality (hidden)
if 'last_refresh_time' not in st.session_state:
    st.session_state.last_refresh_time = time.time()

# Auto-refresh every 60 seconds in the background
if time.time() - st.session_state.last_refresh_time > 60:
    st.session_state.last_refresh_time = time.time()
    st.rerun()

# Centered refresh button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    refresh = st.button("🔄 Refresh Now", key="refresh_button", use_container_width=True)
    if refresh:
        st.session_state.last_refresh_time = time.time()
    # Style the button
    st.markdown("""
    <style>
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #4776E6 0%, #8E54E9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 15px;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        margin: 10px 0 20px 0;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
    }
    div[data-testid="stButton"] > button:active {
        transform: translateY(1px);
    }
    div[data-testid="stButton"] > button:focus {
        outline: none;
        box-shadow: 0 0 0 2px rgba(71, 118, 230, 0.5), 0 6px 15px rgba(0, 0, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for data persistence
if 'weather' not in st.session_state or 'aqi' not in st.session_state or 'forecast' not in st.session_state or 'tweets' not in st.session_state or 'leaderboard' not in st.session_state or refresh:
    st.session_state.weather = get_weather(selected_city)
    st.session_state.aqi = get_aqi(selected_city)
    st.session_state.forecast = get_forecast(selected_city)
    st.session_state.tweets = get_twitter_feed(selected_city)
    st.session_state.leaderboard = get_aqi_leaderboard()

# Display metrics and charts
if st.session_state.weather and st.session_state.aqi is not None:
    weather = st.session_state.weather
    aqi = st.session_state.aqi
    
    # 7-Day Weather Forecast (moved to top)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="margin-bottom: 20px; text-align: center;">7-Day Weather Forecast</h3>', unsafe_allow_html=True)
    
    forecast = st.session_state.forecast
    if isinstance(forecast, list):
        # Create forecast cards
        forecast_cols = st.columns(7)
        
        # Custom CSS for weather icons
        st.markdown("""
        <style>
        .weather-icon {
            font-size: 32px;
            margin-bottom: 5px;
        }
        .forecast-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 15px 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            height: 100%;
        }
        .forecast-date {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .forecast-temp {
            font-size: 20px;
            font-weight: bold;
            margin: 5px 0;
            color: #4776E6;
        }
        .forecast-desc {
            font-size: 12px;
            color: #e0e0e0;
            margin-top: 5px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Weather icon mapping
        weather_icons = {
            "01d": "☀️", "01n": "🌙",  # clear sky
            "02d": "⛅", "02n": "☁️",  # few clouds
            "03d": "☁️", "03n": "☁️",  # scattered clouds
            "04d": "☁️", "04n": "☁️",  # broken clouds
            "09d": "🌧️", "09n": "🌧️",  # shower rain
            "10d": "🌦️", "10n": "🌧️",  # rain
            "11d": "⛈️", "11n": "⛈️",  # thunderstorm
            "13d": "❄️", "13n": "❄️",  # snow
            "50d": "🌫️", "50n": "🌫️",  # mist
        }
        
        for i, day in enumerate(forecast):
            with forecast_cols[i]:
                icon = weather_icons.get(day.get("icon", "01d"), "☁️")
                st.markdown(f"""
                <div class="forecast-card">
                    <div class="forecast-date">{day["date"]}</div>
                    <div class="weather-icon">{icon}</div>
                    <div class="forecast-temp">{day["temp"]}°C</div>
                    <div class="forecast-desc">{day["description"]}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.error("Unable to load forecast data.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add partition/divider after the forecast
    st.markdown("""
    <div style="border-top: 2px solid rgba(71, 118, 230, 0.3); margin: 30px 0; padding-top: 5px;"></div>
    """, unsafe_allow_html=True)
    
    # AQI Leaderboard (moved to appear after the forecast)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="margin-bottom: 20px; text-align: center;">Indian Cities AQI Leaderboard</h3>', unsafe_allow_html=True)
    
    if 'leaderboard' in st.session_state:
        leaderboard = st.session_state.leaderboard
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h4 style="text-align: center; color: #4CAF50;">🌿 Cities with Best Air Quality</h4>', unsafe_allow_html=True)
            
            # Create a table for best cities
            for i, city_data in enumerate(leaderboard["best"]):
                bg_color = "rgba(255, 255, 255, 0.05)"
                if i % 2 == 0:
                    bg_color = "rgba(255, 255, 255, 0.02)"
                    
                st.markdown(f"""
                <div style="display: flex; align-items: center; padding: 8px 15px; background-color: {bg_color}; border-radius: 5px; margin-bottom: 5px;">
                    <div style="width: 30px; font-weight: bold; color: #e0e0e0;">#{i+1}</div>
                    <div style="flex-grow: 1; font-weight: bold;">{city_data['city']}</div>
                    <div style="width: 50px; text-align: right; font-weight: bold; color: {city_data['color']};">{city_data['aqi']}</div>
                    <div style="width: 100px; text-align: right; color: {city_data['color']};">{city_data['category']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown('<h4 style="text-align: center; color: #F44336;">🏭 Cities with Worst Air Quality</h4>', unsafe_allow_html=True)
            
            # Create a table for worst cities
            for i, city_data in enumerate(leaderboard["worst"]):
                bg_color = "rgba(255, 255, 255, 0.05)"
                if i % 2 == 0:
                    bg_color = "rgba(255, 255, 255, 0.02)"
                    
                st.markdown(f"""
                <div style="display: flex; align-items: center; padding: 8px 15px; background-color: {bg_color}; border-radius: 5px; margin-bottom: 5px;">
                    <div style="width: 30px; font-weight: bold; color: #e0e0e0;">#{i+1}</div>
                    <div style="flex-grow: 1; font-weight: bold;">{city_data['city']}</div>
                    <div style="width: 50px; text-align: right; font-weight: bold; color: {city_data['color']};">{city_data['aqi']}</div>
                    <div style="width: 100px; text-align: right; color: {city_data['color']};">{city_data['category']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Loading leaderboard data...")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add another partition after the leaderboard
    st.markdown("""
    <div style="border-top: 2px solid rgba(71, 118, 230, 0.3); margin: 30px 0; padding-top: 5px;"></div>
    """, unsafe_allow_html=True)
    
    # Metrics with custom styling
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌡️ Temperature", f"{weather['temperature']}°C", delta=f"{round(weather['temperature']-25, 1)}°C from avg")
    with col2:
        st.metric("💧 Humidity", f"{weather['humidity']}%")
    with col3:
        st.metric("💨 Wind Speed", f"{weather['wind_speed']} m/s")
    with col4:
        aqi_delta = None
        if isinstance(aqi, int) and aqi > 100:
            aqi_delta = f"{aqi - 100} above safe level"
        st.metric("🌫️ AQI", aqi, delta=aqi_delta, delta_color="inverse")
        
    # Add wind direction to session state if not present
    if 'wind_direction' not in st.session_state:
        st.session_state.wind_direction = random.randint(0, 359)  # Random direction in degrees
    
    # Charts with container styling
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        gauge_fig = create_aqi_gauge(aqi)
        st.plotly_chart(gauge_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Create wind compass
        wind_compass = create_wind_compass(
            wind_speed=weather['wind_speed'],
            wind_degrees=st.session_state.wind_direction
        )
        st.plotly_chart(wind_compass, use_container_width=True)
        
        # Add explanation about wind and AQI
        st.markdown("""
        <div style="font-size: 14px; color: #e0e0e0; margin-top: -15px;">
            <p>Wind direction impacts how air pollutants move and disperse. 
            Downwind areas often experience higher pollution levels.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Close the chart container div that was opened before the columns
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Current Air Quality Category & Health Advisory
    if isinstance(aqi, int):
        # Determine AQI category and detailed advice
        if aqi <= 50:
            category = "Good"
            color = "green"
            icon = "😊"
            whats_happening = "Air pollution levels are low and pose little to no risk to health."
            health_effects = "No health effects are expected in healthy individuals."
            precautions = "No special precautions needed. Enjoy outdoor activities."
        elif aqi <= 100:
            category = "Moderate"
            color = "#B7950B"  # Dark yellow
            icon = "😐"
            whats_happening = "Air quality is acceptable but there may be some pollutants present."
            health_effects = "Unusually sensitive individuals may experience respiratory symptoms. People with respiratory or heart conditions might experience mild effects."
            precautions = "Sensitive people should consider reducing prolonged or heavy outdoor exertion."
        elif aqi <= 200:
            category = "Unhealthy"
            color = "orange"
            icon = "😷"
            whats_happening = "Increased amounts of air pollutants are present, potentially affecting public health."
            health_effects = "General public may not be affected. People with lung disease, older adults and children are at greater risk from exposure to ozone and particle pollution."
            precautions = "People with respiratory or heart conditions, elderly and children should limit prolonged outdoor activity."
        elif aqi <= 300:
            category = "Very Unhealthy"
            color = "red"
            icon = "🚫"
            whats_happening = "Air pollution levels are high and may trigger health alerts."
            health_effects = "Everyone may begin to experience health effects. Members of sensitive groups may experience more serious effects."
            precautions = "Everyone should avoid outdoor physical activities. Sensitive groups should remain indoors and keep windows closed."
        else:
            category = "Hazardous"
            color = "purple"
            icon = "☠️"
            whats_happening = "Air pollution has reached emergency levels that can affect everyone."
            health_effects = "Serious respiratory and cardiovascular effects can occur in all populations. Significant aggravation of heart or lung disease for sensitive groups."
            precautions = "Everyone should avoid all outdoor physical activities. Stay indoors with windows closed and use air purifiers if available."
            
        # Define background colors for each category
        bg_colors = {
            "Good": "rgba(0, 128, 0, 0.1)",
            "Moderate": "rgba(255, 255, 0, 0.1)",
            "Unhealthy": "rgba(255, 165, 0, 0.1)",
            "Very Unhealthy": "rgba(255, 0, 0, 0.1)",
            "Hazardous": "rgba(128, 0, 128, 0.1)"
        }
        
        # Health advisory section removed
    
    # AQI level explanation
    st.markdown("""
    <div style="margin-top: 10px; padding: 10px;">
        <h4 style="font-size: 18px; margin-bottom: 10px;">AQI Level Categories</h4>
        <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: space-between;">
            <div style="background-color: rgba(0, 128, 0, 0.2); border-left: 4px solid green; padding: 8px 15px; border-radius: 5px; flex: 1; min-width: 150px;">
                <span style="color: green; font-weight: bold;">0-50:</span> Good
            </div>
            <div style="background-color: rgba(255, 255, 0, 0.2); border-left: 4px solid yellow; padding: 8px 15px; border-radius: 5px; flex: 1; min-width: 150px;">
                <span style="color: #B7950B; font-weight: bold;">51-100:</span> Moderate
            </div>
            <div style="background-color: rgba(255, 165, 0, 0.2); border-left: 4px solid orange; padding: 8px 15px; border-radius: 5px; flex: 1; min-width: 150px;">
                <span style="color: orange; font-weight: bold;">101-200:</span> Unhealthy
            </div>
            <div style="background-color: rgba(255, 0, 0, 0.2); border-left: 4px solid red; padding: 8px 15px; border-radius: 5px; flex: 1; min-width: 150px;">
                <span style="color: red; font-weight: bold;">201-300:</span> Very Unhealthy
            </div>
            <div style="background-color: rgba(128, 0, 128, 0.2); border-left: 4px solid purple; padding: 8px 15px; border-radius: 5px; flex: 1; min-width: 150px;">
                <span style="color: purple; font-weight: bold;">301-500:</span> Hazardous
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    animated_fig = animated_aqi_temp_chart()
    st.plotly_chart(animated_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    

    

    
    # Multi-city comparison chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="margin-bottom: 20px; text-align: center;">Multi-City AQI Comparison</h3>', unsafe_allow_html=True)
    
    # City selection for comparison
    comparison_cities = st.multiselect(
        "Select cities to compare:",
        ["Mumbai", "Delhi", "Bangalore", "Kolkata", "Chennai", "Hyderabad"],
        default=["Mumbai", "Delhi", "Bangalore"],
        max_selections=3
    )
    
    if comparison_cities:
        multi_city_fig = create_multi_city_chart(comparison_cities)
        st.plotly_chart(multi_city_fig, use_container_width=True)
    else:
        st.info("Please select at least one city to compare.")
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background-color: rgba(255, 0, 0, 0.1); border-left: 5px solid #ff0000; 
                padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h3 style="color: #ff0000; margin: 0 0 10px 0;">⚠️ Data Fetch Error</h3>
        <p style="color: #ff0000; margin: 0;">Failed to fetch data. Please check city name or API rate limits.</p>
    </div>
    """, unsafe_allow_html=True)

# Display hospital information if AQI is severe
if st.session_state.aqi is not None and isinstance(st.session_state.aqi, int) and st.session_state.aqi > 200:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background-color: rgba(255, 0, 0, 0.1); border-left: 5px solid #ff0000; 
                padding: 15px; border-radius: 10px; margin: 15px 0;">
        <h4 style="color: #ff0000; margin: 0 0 10px 0;">⚠️ Air Quality Health Warning</h4>
        <p style="margin: 0 0 10px 0;">The current AQI level is {st.session_state.aqi}, which is considered 
        {'Very Unhealthy' if st.session_state.aqi <= 300 else 'Hazardous'}. 
        Please consider visiting a nearby hospital or respiratory care center if you experience breathing difficulties.</p>
    </div>
    """, unsafe_allow_html=True)
        
    # Show nearby hospitals without using folium
    st.markdown("<h4>Nearby Hospitals & Respiratory Care Centers</h4>", unsafe_allow_html=True)
    
    # Create two columns for hospital listings
    col1, col2 = st.columns(2)
    
    # Mock hospital data for the selected city
    hospitals = [
        {"name": "City General Hospital", "type": "General Hospital", "rating": 4.5, "distance": "2.3 km"},
        {"name": "Apollo Medical Center", "type": "Multi-Specialty Hospital", "rating": 4.8, "distance": "3.1 km"},
        {"name": "Respiratory Care Institute", "type": "Pulmonary Clinic", "rating": 4.2, "distance": "1.8 km"},
        {"name": "Fortis Hospital", "type": "Multi-Specialty Hospital", "rating": 4.7, "distance": "4.5 km"},
        {"name": "Chest & TB Specialty Center", "type": "Respiratory Care", "rating": 4.0, "distance": "2.7 km"},
        {"name": "Metro Healthcare", "type": "Emergency Care", "rating": 3.9, "distance": "1.5 km"}
    ]
    
    # Display hospitals in two columns
    for i, hospital in enumerate(hospitals):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div style="background-color: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                <h5 style="margin: 0 0 5px 0;">{hospital['name']}</h5>
                <p style="margin: 0 0 5px 0; font-size: 14px;"><b>Type:</b> {hospital['type']}</p>
                <p style="margin: 0 0 5px 0; font-size: 14px;"><b>Rating:</b> {"⭐" * int(hospital['rating'])} {hospital['rating']}/5</p>
                <p style="margin: 0; font-size: 14px;"><b>Distance:</b> {hospital['distance']} from city center</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="font-size: 12px; color: #888; text-align: right;">
        * Hospital information is for demonstration purposes only. Please search for actual medical facilities in your area.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(90deg, rgba(30, 60, 114, 0.2), rgba(71, 118, 230, 0.2));
            padding: 15px; border-radius: 10px; margin-top: 30px; text-align: center;">
    <p style="margin: 0; color: #e0e0e0; font-size: 14px;">
        Devloped By Bhushan Navsagar(StrimCoder)| 
        <span style="opacity: 0.8;">© 2023 Indian Lungs Quality Monitor</span>
    </p>
</div>
""", unsafe_allow_html=True)
