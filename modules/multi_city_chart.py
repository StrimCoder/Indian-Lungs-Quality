import plotly.graph_objects as go
import numpy as np
import random
from datetime import datetime, timedelta

def create_multi_city_chart(cities=None):
    """
    Create an animated line chart comparing AQI trends for multiple cities
    
    Args:
        cities (list): List of city names to compare (default: Mumbai, Delhi, Bangalore)
        
    Returns:
        plotly.graph_objects.Figure: Animated line chart
    """
    if cities is None:
        cities = ["Mumbai", "Delhi", "Bangalore"]
    
    # Generate 24 hours of data points (one per hour)
    hours = 24
    timestamps = [(datetime.now() - timedelta(hours=i)).strftime("%H:%M") for i in range(hours)]
    timestamps.reverse()  # Oldest first
    
    # City colors
    colors = {
        "Mumbai": "#1E88E5",   # Blue
        "Delhi": "#D81B60",    # Red
        "Bangalore": "#8E24AA", # Purple
        "Kolkata": "#FFC107",  # Amber
        "Chennai": "#43A047",  # Green
        "Hyderabad": "#FB8C00" # Orange
    }
    
    # Generate realistic AQI data for each city
    city_data = {}
    for city in cities:
        if city == "Delhi":
            # Delhi typically has higher pollution
            base = 180
            amplitude = 60
        elif city == "Mumbai":
            # Mumbai moderate
            base = 100
            amplitude = 40
        elif city == "Bangalore":
            # Bangalore typically cleaner
            base = 70
            amplitude = 30
        else:
            # Other cities
            base = 120
            amplitude = 50
        
        # Generate data with a realistic pattern (higher in morning/evening, lower midday)
        aqi_values = []
        for i in range(hours):
            hour = (datetime.now() - timedelta(hours=hours-i-1)).hour
            
            # Time-based variation (rush hours have higher pollution)
            time_factor = 0.8
            if 7 <= hour <= 10:  # Morning rush
                time_factor = 1.2
            elif 16 <= hour <= 19:  # Evening rush
                time_factor = 1.3
            
            # Add some randomness
            random_factor = random.uniform(0.85, 1.15)
            
            aqi = base * time_factor * random_factor
            aqi_values.append(min(500, max(0, int(aqi))))
        
        city_data[city] = aqi_values
    
    # Create figure
    fig = go.Figure()
    
    # Add traces for each city
    for city in cities:
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=city_data[city],
                mode="lines+markers",
                name=city,
                line=dict(width=3, color=colors.get(city, "#000000")),
                marker=dict(size=8, color=colors.get(city, "#000000"))
            )
        )
    
    # Add animation frames
    frames = []
    for i in range(1, len(timestamps) + 1):
        frame_data = []
        for city in cities:
            frame_data.append(
                go.Scatter(
                    x=timestamps[:i],
                    y=city_data[city][:i],
                )
            )
        frames.append(go.Frame(data=frame_data, name=str(i)))
    
    fig.frames = frames
    
    # Add slider and buttons
    fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 300, "redraw": True}, "fromcurrent": True}],
                        "label": "Play",
                        "method": "animate",
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                        "label": "Pause",
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 10},
                "type": "buttons",
                "x": 0.1,
                "y": 0,
            }
        ],
        sliders=[
            {
                "steps": [
                    {
                        "args": [[str(i)], {"frame": {"duration": 300, "redraw": True}, "mode": "immediate"}],
                        "label": timestamps[i-1],
                        "method": "animate",
                    }
                    for i in range(1, len(timestamps) + 1)
                ],
                "x": 0.1,
                "y": 0,
            }
        ],
        xaxis=dict(
            title="Time (Last 24 Hours)",
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.1)",
        ),
        yaxis=dict(
            title="Air Quality Index (AQI)",
            range=[0, max([max(vals) for vals in city_data.values()]) + 20],
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.1)",
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e0e0e0"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=14)
        ),
        margin=dict(l=60, r=30, t=50, b=50),
        height=500,
        title={
            'text': "24-Hour AQI Comparison",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24, 'color': '#e0e0e0'}
        },
    )
    
    # Add AQI threshold lines
    aqi_thresholds = [
        (50, "Good", "green"),
        (100, "Moderate", "#B7950B"),
        (200, "Unhealthy", "orange"),
        (300, "Very Unhealthy", "red"),
        (500, "Hazardous", "purple")
    ]
    
    for threshold, label, color in aqi_thresholds:
        fig.add_shape(
            type="line",
            x0=timestamps[0],
            y0=threshold,
            x1=timestamps[-1],
            y1=threshold,
            line=dict(color=color, width=1, dash="dash"),
        )
        fig.add_annotation(
            x=timestamps[0],
            y=threshold,
            text=label,
            showarrow=False,
            xshift=-40,
            font=dict(color=color, size=10),
        )
    
    return fig