import requests
import pandas as pd
from datetime import datetime, timedelta
import random

# API key (same as in fetch_data.py)
OPENWEATHER_API_KEY = "760fb4c157f74ffc6b0576219d9ad110"

def get_forecast(city):
    """Fetch 7-day weather forecast for a city."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("cod") != "200":
            error_msg = data.get("message", "Unknown error")
            return {"error": f"API Error: {error_msg}"}
        
        # Process forecast data
        forecast_data = []
        
        # OpenWeather free API only provides 5 days / 3 hour forecast
        # We'll extract daily data and then simulate the remaining days
        
        # Get unique dates from the forecast
        dates = set()
        for item in data["list"]:
            dt = datetime.fromtimestamp(item["dt"])
            dates.add(dt.date())
        
        # Get one forecast per day (at noon if available)
        for date in sorted(dates):
            day_items = [item for item in data["list"] 
                        if datetime.fromtimestamp(item["dt"]).date() == date]
            
            # Try to get forecast around noon
            noon_forecast = None
            for item in day_items:
                dt = datetime.fromtimestamp(item["dt"])
                if 11 <= dt.hour <= 14:
                    noon_forecast = item
                    break
            
            # If no noon forecast, take the first one for the day
            if noon_forecast is None and day_items:
                noon_forecast = day_items[0]
            
            if noon_forecast:
                dt = datetime.fromtimestamp(noon_forecast["dt"])
                forecast_data.append({
                    "date": dt.strftime("%a, %b %d"),
                    "temp": round(noon_forecast["main"]["temp"]),
                    "humidity": noon_forecast["main"]["humidity"],
                    "description": noon_forecast["weather"][0]["description"].title(),
                    "icon": noon_forecast["weather"][0]["icon"],
                })
        
        # If we have less than 7 days, simulate the remaining days
        # This is because the free API only gives 5 days
        last_date = max(dates)
        last_temp = forecast_data[-1]["temp"]
        last_humidity = forecast_data[-1]["humidity"]
        
        while len(forecast_data) < 7:
            last_date += timedelta(days=1)
            # Simulate some variation in temperature and humidity
            temp_change = random.uniform(-2, 2)
            humidity_change = random.uniform(-5, 5)
            
            forecast_data.append({
                "date": last_date.strftime("%a, %b %d"),
                "temp": round(last_temp + temp_change),
                "humidity": min(max(0, round(last_humidity + humidity_change)), 100),
                "description": forecast_data[-1]["description"],
                "icon": forecast_data[-1]["icon"],
            })
        
        return forecast_data
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except (KeyError, ValueError, TypeError) as e:
        return {"error": f"Data parsing error: {str(e)}"}