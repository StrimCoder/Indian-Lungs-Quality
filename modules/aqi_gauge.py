import plotly.graph_objects as go

def create_aqi_gauge(aqi):
    """Generate a Plotly AQI gauge chart."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=aqi,
        title={'text': "AQI Level"},
        gauge={
            'axis': {'range': [0, 500]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "green"},
                {'range': [51, 100], 'color': "yellow"},
                {'range': [101, 200], 'color': "orange"},
                {'range': [201, 300], 'color': "red"},
                {'range': [301, 500], 'color': "purple"}
            ],
        }
    ))
    return fig
