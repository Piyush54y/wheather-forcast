import streamlit as st
import requests
from datetime import datetime
import pytz

API_KEY = "bcbb60c7dbd12fcf01754ed47775153e"

city_coords = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Kolkata": (22.5726, 88.3639),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567)
}

st.set_page_config(page_title="🌤️ Weather & AQI", layout="centered", page_icon="☁️")
st.title("🌤️ Live Weather & Air Quality")

city = st.selectbox("Choose a city", list(city_coords.keys()))
lat, lon = city_coords[city]

if st.button("Get Live Weather & AQI"):
    with st.spinner("Fetching live data..."):
        try:
            # ✅ Real-time Weather
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
            weather_res = requests.get(weather_url)
            weather = weather_res.json()

            if weather_res.status_code != 200:
                st.error("❌ Failed to fetch weather data.")
                st.json(weather)
                st.stop()

            ist = pytz.timezone("Asia/Kolkata")
            sunrise_time = datetime.fromtimestamp(weather['sys']['sunrise'], tz=pytz.utc).astimezone(ist).strftime("%I:%M %p")
            sunset_time = datetime.fromtimestamp(weather['sys']['sunset'], tz=pytz.utc).astimezone(ist).strftime("%I:%M %p")

            st.subheader(f"📍 Current Weather in {city}")
            st.metric("🌡️ Temperature", f"{weather['main']['temp']} °C")
            st.write("📋 Description:", weather['weather'][0]['description'].capitalize())
            st.write("💧 Humidity:", f"{weather['main']['humidity']}%")
            st.write("🌬️ Wind Speed:", f"{weather['wind']['speed']} m/s")
            st.write("🌅 Sunrise:", sunrise_time)
            st.write("🌇 Sunset:", sunset_time)

            # ✅ Air Quality
            st.subheader("🌫️ Air Quality Index (AQI)")
            aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
            aqi_res = requests.get(aqi_url)
            aqi_data = aqi_res.json()

            if "list" not in aqi_data:
                st.warning("⚠️ AQI data not available.")
                st.json(aqi_data)
            else:
                air = aqi_data['list'][0]
                aqi = air['main']['aqi']
                pollutants = air['components']
                aqi_levels = {
                    1: "Good 🟢",
                    2: "Fair 🟡",
                    3: "Moderate 🟠",
                    4: "Poor 🔴",
                    5: "Very Poor 🔴"
                }

                st.write("AQI Level:", aqi_levels.get(aqi, "Unknown"))
                st.write("🧪 PM2.5:", pollutants['pm2_5'], "μg/m³")
                st.write("🧪 PM10:", pollutants['pm10'], "μg/m³")
                st.write("🧪 CO:", pollutants['co'], "μg/m³")
                st.write("🧪 NO₂:", pollutants['no2'], "μg/m³")
                st.write("🧪 O₃:", pollutants['o3'], "μg/m³")
                st.write("🧪 SO₂:", pollutants['so2'], "μg/m³")

        except Exception as e:
            st.error("⚠️ Something went wrong while fetching data.")
            st.exception(e)
