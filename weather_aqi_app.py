import streamlit as st
import requests
from datetime import datetime

API_KEY = "YOUR_API_KEY"

st.set_page_config(page_title="Smart Weather & AQI", page_icon="🌦️")
st.title("🌤️ Weather & Air Quality Monitor")
st.markdown("Check the live weather and air pollution for Indian cities.")

city_coords = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Kolkata": (22.5726, 88.3639),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707)
}

city = st.selectbox("Choose a city", list(city_coords.keys()))
lat, lon = city_coords[city]

if st.button("Get Live Weather & AQI"):
    # --- Weather API (OneCall 3.0) ---
    weather_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,alerts&appid={API_KEY}&units=metric"
    weather_data = requests.get(weather_url).json()
    
    current = weather_data['current']
    daily = weather_data['daily'][0]

    st.subheader(f"🌇 {city} - Current Weather")
    st.metric("🌡️ Temperature", f"{current['temp']} °C")
    st.write(f"📋 Description: {current['weather'][0]['description'].capitalize()}")
    st.write(f"💧 Humidity: {current['humidity']}%")
    st.write(f"🌬️ Wind Speed: {current['wind_speed']} m/s")

    dt = datetime.fromtimestamp(daily['dt']).strftime('%A, %d %b')
    st.subheader(f"🗓️ Forecast for {dt}")
    st.write(f"🌡️ Max: {daily['temp']['max']}°C | Min: {daily['temp']['min']}°C")
    st.write(f"🌅 Sunrise: {datetime.fromtimestamp(current['sunrise']).strftime('%H:%M')}")
    st.write(f"🌇 Sunset: {datetime.fromtimestamp(current['sunset']).strftime('%H:%M')}")

    # --- AQI API ---
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    aqi_data = requests.get(aqi_url).json()
    aqi = aqi_data['list'][0]['main']['aqi']
    comps = aqi_data['list'][0]['components']

    aqi_status = {
        1: "Good 😊",
        2: "Fair 🙂",
        3: "Moderate 😐",
        4: "Poor 😷",
        5: "Very Poor 🤢"
    }

    st.subheader("🌫️ Air Quality Index (AQI)")
    st.metric("AQI", f"{aqi} - {aqi_status[aqi]}")
    st.write(f"PM2.5: {comps['pm2_5']} µg/m³")
    st.write(f"PM10: {comps['pm10']} µg/m³")
    st.write(f"CO: {comps['co']} µg/m³")
    st.write(f"NO₂: {comps['no2']} µg/m³")
