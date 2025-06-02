import streamlit as st
import requests
from datetime import datetime

# 🌐 OpenWeatherMap API Key
API_KEY = "9db50c7b28266e83432aa025a772b16b"

# 📍 Coordinates for Indian cities
city_coords = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Kolkata": (22.5726, 88.3639),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567)
}

# 🎨 Streamlit UI Config
st.set_page_config(page_title="🌤️ Weather & AQI Monitor", layout="centered", page_icon="☁️")
st.title("🌤️ Weather & Air Quality Monitor")
st.markdown("Check the live weather and air pollution for Indian cities.")

# 🔽 Select city
city = st.selectbox("Choose a city", list(city_coords.keys()))
lat, lon = city_coords[city]

if st.button("Get Live Weather & AQI"):
    with st.spinner("Fetching weather data..."):
        try:
            exclude = "minutely,hourly,alerts"
            units = "metric"
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude}&units={units}&appid={API_KEY}"
            
            res = requests.get(url)
            data = res.json()

            # ❌ If error in response
            if 'current' not in data:
                st.error("❌ Failed to fetch weather. Please check your API key or usage limits.")
                st.json(data)
                st.stop()

            current = data['current']
            daily = data['daily']

            # 📍 Current Weather
            st.subheader(f"📍 Current Weather in {city}")
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

        except Exception as e:
            st.error("Something went wrong!")
            st.exception(e)
