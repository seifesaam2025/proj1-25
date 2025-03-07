import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Minimalist Home Monitor",
    page_icon="🏡",
    layout="wide"
)

# Initialize session state variables
if 'temperature' not in st.session_state:
    st.session_state.temperature = 21.5
if 'humidity' not in st.session_state:
    st.session_state.humidity = 42
if 'lights' not in st.session_state:
    st.session_state.lights = {'living': False, 'kitchen': True, 'bedroom': False}
if 'thermostat' not in st.session_state:
    st.session_state.thermostat = 22
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now().strftime("%H:%M:%S")
if 'energy_data' not in st.session_state:
    st.session_state.energy_data = {
        'daily_usage': random.uniform(8, 15),
        'weekly_total': random.uniform(50, 90)
    }

# Apply custom CSS for minimalist design
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
        color: #212529;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 1.2rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .dashboard-title {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #333;
    }
    .sensor-label {
        font-size: 1rem;
        color: #6c757d;
        margin-bottom: 0.3rem;
    }
    .sensor-value {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .card-title {
        font-size: 1.2rem;
        font-weight: 500;
        margin-bottom: 1rem;
        color: #444;
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-on {
        background-color: #20c997;
    }
    .status-off {
        background-color: #ced4da;
    }
</style>
""", unsafe_allow_html=True)

# Function to toggle lights
def toggle_light(room):
    st.session_state.lights[room] = not st.session_state.lights[room]

# Function to update thermostat
def update_thermostat(new_value):
    st.session_state.thermostat = new_value

# Simulate sensor updates
def update_sensors():
    # Update temperature with small random changes
    temp_change = (random.random() - 0.5) * 0.5
    st.session_state.temperature = round(st.session_state.temperature + temp_change, 1)
    
    # Update humidity with small random changes
    humidity_change = (random.random() - 0.5) * 1.5
    st.session_state.humidity = min(max(round(st.session_state.humidity + humidity_change), 30), 70)
    
    # Update energy data with small random changes
    energy_change = (random.random() - 0.5) * 0.3
    st.session_state.energy_data['daily_usage'] = round(st.session_state.energy_data['daily_usage'] + energy_change, 2)
    st.session_state.energy_data['weekly_total'] = round(st.session_state.energy_data['weekly_total'] + energy_change * 7, 2)
    
    # Update timestamp
    st.session_state.last_update = datetime.now().strftime("%H:%M:%S")

# Update data
update_sensors()

# Main layout
st.markdown("<h1 class='dashboard-title'>🏡 Minimalist Home Monitor</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: right; color: #6c757d; font-size: 0.8rem;'>Last updated: {st.session_state.last_update}</p>", unsafe_allow_html=True)

# Create two-column layout for main dashboard
col1, col2 = st.columns([3, 2])

# Left column - Environment sensors
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='card-title'>Environment</h2>", unsafe_allow_html=True)
    
    # Create sensor display grid
    sensor_cols = st.columns(2)
    
    with sensor_cols[0]:
        st.markdown("<p class='sensor-label'>Temperature</p>", unsafe_allow_html=True)
        temp_color = "#dc3545" if st.session_state.temperature > 25 else "#212529"
        st.markdown(f"<p class='sensor-value' style='color: {temp_color};'>{st.session_state.temperature}°C</p>", unsafe_allow_html=True)
        st.progress((st.session_state.temperature - 15) / 20)
    
    with sensor_cols[1]:
        st.markdown("<p class='sensor-label'>Humidity</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='sensor-value'>{st.session_state.humidity}%</p>", unsafe_allow_html=True)
        st.progress(st.session_state.humidity / 100)
    
    # Thermostat control
    st.markdown("<p class='sensor-label'>Thermostat Setting</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='sensor-value' style='font-size: 1.5rem;'>{st.session_state.thermostat}°C</p>", unsafe_allow_html=True)
    new_thermostat = st.slider("", 18, 28, st.session_state.thermostat, key="thermostat_slider", label_visibility="collapsed")
    if new_thermostat != st.session_state.thermostat:
        update_thermostat(new_thermostat)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Energy overview
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='card-title'>Energy Overview</h2>", unsafe_allow_html=True)
    
    energy_cols = st.columns(2)
    with energy_cols[0]:
        st.metric(label="Today's Usage", value=f"{st.session_state.energy_data['daily_usage']:.1f} kWh")
    with energy_cols[1]:
        st.metric(label="This Week", value=f"{st.session_state.energy_data['weekly_total']:.1f} kWh")
    
    # Create sample energy data for chart
    energy_times = [f"{i}:00" for i in range(24)]
    energy_values = []
    for i in range(24):
        if 0 <= i < 6:  # Night (low usage)
            energy_values.append(random.uniform(0.2, 0.5))
        elif 6 <= i < 9:  # Morning peak
            energy_values.append(random.uniform(1.5, 2.3))
        elif 9 <= i < 17:  # Day (medium usage)
            energy_values.append(random.uniform(0.8, 1.3))
        elif 17 <= i < 22:  # Evening peak
            energy_values.append(random.uniform(1.7, 2.5))
        else:  # Late night (low usage)
            energy_values.append(random.uniform(0.3, 0.7))
    
    # Create a chart
    st.line_chart(pd.DataFrame({'Energy (kWh)': energy_values}, index=energy_times))
    
    st.markdown("</div>", unsafe_allow_html=True)

# Right column - Device controls
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='card-title'>Light Controls</h2>", unsafe_allow_html=True)
    
    for room in st.session_state.lights:
        status_class = "status-on" if st.session_state.lights[room] else "status-off"
        status_text = "On" if st.session_state.lights[room] else "Off"
        
        light_cols = st.columns([3, 1])
        with light_cols[0]:
            st.markdown(f"<div><span class='status-indicator {status_class}'></span> {room.capitalize()}: {status_text}</div>", unsafe_allow_html=True)
        with light_cols[1]:
            if st.button("Toggle", key=f"light_{room}", use_container_width=True):
                toggle_light(room)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Simple tips card
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='card-title'>Energy Saving Tips</h2>", unsafe_allow_html=True)
    
    tips = [
        "Turn off lights when leaving a room",
        "Lower thermostat by 1°C to save up to 10% on heating",
        "Unplug devices not in use to eliminate standby power"
    ]
    
    for tip in tips:
        st.markdown(f"• {tip}")
    
    st.markdown("</div>", unsafe_allow_html=True)
