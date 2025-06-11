import plotly.graph_objects as go
import numpy as np
import math

def get_wind_direction_text(degrees):
    """Convert wind direction in degrees to cardinal direction text"""
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
                 "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    
    # Convert degrees to 0-15 index
    index = round(degrees / 22.5) % 16
    return directions[index]

def create_wind_compass(wind_speed, wind_degrees):
    """
    Create a Plotly compass/dial visualization showing wind direction and speed
    
    Args:
        wind_speed (float): Wind speed in m/s
        wind_degrees (float): Wind direction in degrees (0-360, 0 = North)
        
    Returns:
        plotly.graph_objects.Figure: Wind compass visualization
    """
    # Convert degrees to radians for calculations
    wind_radians = math.radians(wind_degrees)
    
    # Create a circle for the compass
    theta = np.linspace(0, 2*np.pi, 100)
    radius = np.ones(100)
    
    # Create the figure
    fig = go.Figure()
    
    # Add compass circle
    fig.add_trace(go.Scatterpolar(
        r=radius,
        theta=np.degrees(theta),
        mode='lines',
        line=dict(color='rgba(255, 255, 255, 0.2)', width=1),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add cardinal directions
    cardinal_dirs = [
        {"dir": "N", "angle": 90, "r": 1.1},
        {"dir": "E", "angle": 0, "r": 1.1},
        {"dir": "S", "angle": 270, "r": 1.1},
        {"dir": "W", "angle": 180, "r": 1.1},
        {"dir": "NE", "angle": 45, "r": 1.05},
        {"dir": "SE", "angle": 315, "r": 1.05},
        {"dir": "SW", "angle": 225, "r": 1.05},
        {"dir": "NW", "angle": 135, "r": 1.05}
    ]
    
    for cd in cardinal_dirs:
        fig.add_annotation(
            x=cd["r"] * np.cos(np.radians(cd["angle"])),
            y=cd["r"] * np.sin(np.radians(cd["angle"])),
            text=cd["dir"],
            showarrow=False,
            font=dict(size=14, color="#e0e0e0")
        )
    
    # Calculate arrow endpoint
    # Convert meteorological wind direction to mathematical angle
    # In meteorology, 0° = North, 90° = East, etc.
    # In mathematics, 0° = East, 90° = North, etc.
    math_angle = 90 - wind_degrees
    if math_angle < 0:
        math_angle += 360
    
    # Arrow length proportional to wind speed (but capped for visual appeal)
    arrow_length = min(0.8, 0.3 + (wind_speed / 20) * 0.5)
    
    # Arrow endpoint
    x_end = arrow_length * np.cos(np.radians(math_angle))
    y_end = arrow_length * np.sin(np.radians(math_angle))
    
    # Add wind direction arrow
    fig.add_trace(go.Scatter(
        x=[0, x_end],
        y=[0, y_end],
        mode='lines+markers',
        line=dict(color='#4776E6', width=3),
        marker=dict(
            size=[10, 15],
            color=['#4776E6', '#4776E6'],
            symbol=['circle', 'arrow'],
            angle=math_angle
        ),
        showlegend=False
    ))
    
    # Get cardinal direction text
    direction_text = get_wind_direction_text(wind_degrees)
    
    # Add wind speed and direction text in the center
    fig.add_annotation(
        x=0,
        y=-0.15,
        text=f"{wind_speed} m/s",
        showarrow=False,
        font=dict(size=20, color="#4776E6"),
        xanchor="center"
    )
    
    fig.add_annotation(
        x=0,
        y=-0.3,
        text=f"{direction_text} ({wind_degrees}°)",
        showarrow=False,
        font=dict(size=16, color="#e0e0e0"),
        xanchor="center"
    )
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0, 1.2]
            ),
            angularaxis=dict(
                visible=False
            )
        ),
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=20),
        height=350,
        width=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title={
            'text': "Wind Direction",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': '#e0e0e0'}
        }
    )
    
    return fig