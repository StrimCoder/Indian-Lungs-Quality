import requests
import json
import os
from datetime import datetime

# Twitter API credentials - replace with your own
TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN", "YOUR_BEARER_TOKEN_HERE")

def get_twitter_feed(city, count=5):
    """
    Fetch tweets about air quality for a specific city
    
    Args:
        city (str): City name to search for
        count (int): Number of tweets to return
        
    Returns:
        list: List of tweet dictionaries with text, username, created_at, and profile_image
    """
    # If no bearer token, return mock data
    if TWITTER_BEARER_TOKEN == "YOUR_BEARER_TOKEN_HERE":
        return get_mock_tweets(city, count)
    
    try:
        # Twitter API v2 search endpoint
        url = "https://api.twitter.com/2/tweets/search/recent"
        
        # Query parameters
        params = {
            'query': f'air quality {city} OR pollution {city} -is:retweet',
            'max_results': count,
            'tweet.fields': 'created_at',
            'expansions': 'author_id',
            'user.fields': 'profile_image_url,username'
        }
        
        # Headers with bearer token
        headers = {
            'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'
        }
        
        # Make the request
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code != 200:
            return get_mock_tweets(city, count)
        
        # Parse the response
        data = response.json()
        
        # Process tweets
        tweets = []
        if 'data' in data and 'includes' in data and 'users' in data['includes']:
            users = {user['id']: user for user in data['includes']['users']}
            
            for tweet in data['data']:
                author_id = tweet.get('author_id')
                user = users.get(author_id, {})
                
                tweets.append({
                    'text': tweet.get('text', ''),
                    'username': user.get('username', 'Unknown'),
                    'created_at': tweet.get('created_at', ''),
                    'profile_image': user.get('profile_image_url', '')
                })
        
        return tweets
    
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return get_mock_tweets(city, count)

def get_mock_tweets(city, count=5):
    """Generate mock tweets for demo purposes"""
    mock_tweets = [
        {
            'text': f"Air quality in {city} has improved today! AQI levels are down by 15 points. #AirQuality #CleanAir",
            'username': "CleanAirWatch",
            'created_at': (datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ"),
            'profile_image': "https://pbs.twimg.com/profile_images/1234567890/avatar_400x400.jpg"
        },
        {
            'text': f"Concerned about the rising pollution levels in {city}. Authorities need to take immediate action! #Pollution #PublicHealth",
            'username': "EnvActivist",
            'created_at': (datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ"),
            'profile_image': "https://pbs.twimg.com/profile_images/0987654321/avatar_400x400.jpg"
        },
        {
            'text': f"Just checked the AQI for {city} - it's at unhealthy levels today. Wear masks if you're going outside! #AirQualityAlert",
            'username': "HealthAdvisor",
            'created_at': (datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ"),
            'profile_image': "https://pbs.twimg.com/profile_images/1122334455/avatar_400x400.jpg"
        },
        {
            'text': f"New study shows correlation between air pollution in {city} and respiratory issues. #Research #AirPollution",
            'username': "ScienceDaily",
            'created_at': (datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ"),
            'profile_image': "https://pbs.twimg.com/profile_images/5566778899/avatar_400x400.jpg"
        },
        {
            'text': f"Local government announces new measures to combat air pollution in {city}. #GreenInitiatives #CleanAir",
            'username': "CityUpdates",
            'created_at': (datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ"),
            'profile_image': "https://pbs.twimg.com/profile_images/6677889900/avatar_400x400.jpg"
        }
    ]
    
    return mock_tweets[:count]