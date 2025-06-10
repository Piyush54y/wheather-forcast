import streamlit as st
import requests
from datetime import datetime

API_KEY = "9db50c7b28266e83432aa025a772b16b"

city_coords = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Kolkata": (22.5726, 88.3639),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567)
}

st.set_page_config(page_title="🌤️ Weather & AQI Monitor", layout="centered", page_icon="☁️")
st.title("🌤️ Weather & Air Quality Monitor")
st.markdown("Get real-time weather + air quality (PM, CO, NO₂, etc.) for Indian cities.")

city = st.selectbox("Choose a city", list(city_coords.keys()))
lat, lon = city_coords[city]

if st.button("Get Live Weather & AQI"):
    try:
        with st.spinner("Fetching data..."):
            # 🌤️ Weather Forecast
            weather_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units=metric&appid={API_KEY}"
            weather_res = requests.get(weather_url)
            weather_data = weather_res.json()

            if 'current' not in weather_data:
                st.error("❌ Weather API error. Check key/limit.")
                st.json(weather_data)
                st.stop()

            current = weather_data['current']
            daily = weather_data['daily']

            st.subheader(f"📍 Current Weather in {city}")
            st.metric("🌡️ Temperature", f"{current['temp']} °C")
            st.write("📋 Description:", current['weather'][0]['description'].capitalize())
            st.write("💧 Humidity:", f"{current['humidity']}%")
            st.write("🌬️ Wind Speed:", f"{current['wind_speed']} m/s")
            st.write("🌅 Sunrise:", datetime.fromtimestamp(current['sunrise']).strftime("%I:%M %p"))
            st.write("🌇 Sunset:", datetime.fromtimestamp(current['sunset']).strftime("%I:%M %p"))

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

            # 🌫️ Air Quality Index
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
        st.error("An error occurred while fetching data.")
        st.exception(e)
