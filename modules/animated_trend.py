import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def animated_aqi_temp_chart():
    """Generate an animated 24-hour AQI & Temperature trend line chart."""

    # Simulate 24 hours of AQI and Temperature data
    times = pd.date_range(end=datetime.now(), periods=24, freq='H')
    aqi_values = [random.randint(60, 250) for _ in range(24)]
    temp_values = [random.uniform(20, 36) for _ in range(24)]

    # Create DataFrame
    df = pd.DataFrame({
        'Time': times,
        'AQI': aqi_values,
        'Temperature': temp_values
    })
    df['Hour'] = df.index  # frame reference

    # Initialize figure
    fig = go.Figure()

    # Add AQI trace
    fig.add_trace(go.Scatter(
        x=df['Time'], y=df['AQI'],
        mode='lines+markers',
        name='AQI',
        line=dict(color='orange', width=3)
    ))

    # Add Temperature trace
    fig.add_trace(go.Scatter(
        x=df['Time'], y=df['Temperature'],
        mode='lines+markers',
        name='Temperature (°C)',
        yaxis="y2",
        line=dict(color='dodgerblue', width=3)
    ))

    # Configure axes and layout
    fig.update_layout(
        title="📊 Animated 24-Hour AQI & Temperature Trend",
        xaxis=dict(title="Time"),
        yaxis=dict(title="AQI", range=[0, 300]),
        yaxis2=dict(title="Temperature (°C)", overlaying='y', side='right', range=[15, 40]),
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.5)'),
        height=500,
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[dict(label="▶️ Play",
                          method="animate",
                          args=[None, {"frame": {"duration": 400, "redraw": True},
                                       "fromcurrent": True}])]
        )]
    )

    # Create frames for animation
    frames = []
    for i in range(len(df)):
        frame = go.Frame(
            data=[
                go.Scatter(x=df['Time'][:i+1], y=df['AQI'][:i+1]),
                go.Scatter(x=df['Time'][:i+1], y=df['Temperature'][:i+1])
            ],
            name=str(i)
        )
        frames.append(frame)

    fig.frames = frames

    return fig
