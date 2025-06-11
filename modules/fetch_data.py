import requests
import logging
from typing import Dict, Any, Optional, Union
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init(autoreset=True)

# --- API KEYS (keep them secret in production)
OPENWEATHER_API_KEY = "760fb4c157f74ffc6b0576219d9ad110"
AQI_API_TOKEN = "c0c1175080f63bb06d273a381a0d61a86efebe85"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=f"{Fore.CYAN}%(asctime)s{Style.RESET_ALL} - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def fetch_api_data(url: str, timeout: int = 10) -> Dict[str, Any]:
    """Generic function to fetch data from APIs with error handling."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.RequestException as e:
        logger.error(f"{Fore.RED}Request failed: {e}{Style.RESET_ALL}")
        return {"success": False, "error": f"Request failed: {str(e)}"}
    except (ValueError, TypeError) as e:
        logger.error(f"{Fore.RED}JSON parsing error: {e}{Style.RESET_ALL}")
        return {"success": False, "error": f"Data parsing error: {str(e)}"}

def get_weather(city: str) -> Dict[str, Any]:
    """Fetch real-time weather data for a city with beautiful output."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    result = fetch_api_data(url)
    
    if not result["success"]:
        return {"error": result["error"]}
        
    data = result["data"]
    if data.get("cod") != 200:
        error_msg = data.get("message", "Unknown error")
        logger.warning(f"{Fore.YELLOW}Weather API error: {error_msg}{Style.RESET_ALL}")
        return {"error": f"API Error: {error_msg}"}
        
    try:
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"].title(),
            "city_name": data["name"],
            "country": data["sys"]["country"]
        }
    except KeyError as e:
        logger.error(f"{Fore.RED}Missing data in weather response: {e}{Style.RESET_ALL}")
        return {"error": f"Data structure error: {str(e)}"}

def get_aqi(city: str) -> Union[int, Dict[str, str]]:
    """Fetch real-time AQI data for a city with beautiful output."""
    url = f"https://api.waqi.info/feed/{city}/?token={AQI_API_TOKEN}"
    result = fetch_api_data(url)
    
    if not result["success"]:
        return {"error": result["error"]}
        
    data = result["data"]
    if data.get("status") != "ok":
        error_msg = data.get("data", "Unknown error")
        logger.warning(f"{Fore.YELLOW}AQI API error: {error_msg}{Style.RESET_ALL}")
        return {"error": f"API Error: {error_msg}"}
        
    try:
        aqi_value = data["data"]["aqi"]
        logger.info(f"{Fore.GREEN}Successfully retrieved AQI for {city}: {aqi_value}{Style.RESET_ALL}")
        return aqi_value
    except KeyError as e:
        logger.error(f"{Fore.RED}Missing data in AQI response: {e}{Style.RESET_ALL}")
        return {"error": f"Data structure error: {str(e)}"}

def display_weather_info(weather_data: Dict[str, Any]) -> None:
    """Display weather information in a beautiful format."""
    if "error" in weather_data:
        print(f"{Fore.RED}Error: {weather_data['error']}{Style.RESET_ALL}")
        return
        
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ Weather for {Fore.YELLOW}{weather_data['city_name']}, {weather_data['country']}{Fore.CYAN} ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠══════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.WHITE}Temperature: {Fore.YELLOW}{weather_data['temperature']}°C{Fore.CYAN}           ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.WHITE}Humidity: {Fore.YELLOW}{weather_data['humidity']}%{Fore.CYAN}               ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.WHITE}Wind Speed: {Fore.YELLOW}{weather_data['wind_speed']} m/s{Fore.CYAN}        ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.WHITE}Description: {Fore.YELLOW}{weather_data['description']}{Fore.CYAN}    ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════╝{Style.RESET_ALL}\n")