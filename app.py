import streamlit as st
import requests
from datetime import datetime

API_KEY = "9db50c7b28266e83432aa025a772b16b"  # Your OpenWeatherMap API Key

# Predefined city coordinates
city_coords = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Kolkata": (22.5726, 88.3639),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707)
}

st.set_page_config(page_title="Weather Forecast App", page_icon="🌤️")
st.title("🌤️ Weather Forecast - OpenWeatherMap API")
st.markdown("Get live weather updates and 7-day forecast for top Indian cities.")

# City selection
city = st.selectbox("Choose a City", list(city_coords.keys()))
lat, lon = city_coords[city]

if st.button("Get Weather Forecast"):
    exclude = "minutely,hourly,alerts"
    units = "metric"

    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude}&units={units}&appid={API_KEY}"
    res = requests.get(url)
    data = res.json()

    current = data['current']
    daily = data['daily']

    # 🌡️ Current Weather
    st.subheader(f"🌆 Current Weather in {city}")
    st.metric("🌡️ Temperature", f"{current['temp']} °C")
    st.write("📋 Description:", current['weather'][0]['description'].capitalize())
    st.write("💧 Humidity:", f"{current['humidity']}%")
    st.write("🌬️ Wind Speed:", f"{current['wind_speed']} m/s")
    st.write("🌅 Sunrise:", datetime.fromtimestamp(current['sunrise']).strftime("%I:%M %p"))
    st.write("🌇 Sunset:", datetime.fromtimestamp(current['sunset']).strftime("%I:%M %p"))

    # 📆 7-Day Forecast
    st.subheader("📆 7-Day Forecast")
    for day in daily[:7]:
        date = datetime.fromtimestamp(day['dt']).strftime("%A, %d %b")
        temp_day = day['temp']['day']
        temp_night = day['temp']['night']
        weather = day['weather'][0]['main']
        desc = day['weather'][0]['description'].capitalize()
        st.markdown(f"**{date}**")
        st.write(f"🌞 Day: {temp_day} °C | 🌙 Night: {temp_night} °C | {weather} ({desc})")
        st.write("---")
