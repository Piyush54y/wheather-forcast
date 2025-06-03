import streamlit as st
import requests

API_KEY = "f4d95ef455bf4ada8f982321250306"

city_coords = {
    "Delhi": "Delhi",
    "Mumbai": "Mumbai",
    "Kolkata": "Kolkata",
    "Bangalore": "Bangalore",
    "Chennai": "Chennai",
    "Hyderabad": "Hyderabad",
    "Pune": "Pune"
}

st.set_page_config(page_title="🌤️ Weather & AQI", layout="centered", page_icon="☁️")
st.title("🌤️ Weather & Air Quality Monitor")

city = st.selectbox("Choose a city", list(city_coords.keys()))
location = city_coords[city]

if st.button("Get Live Weather & AQI"):
    with st.spinner("Fetching data..."):
        try:
            url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}&aqi=yes"
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200 or "error" in data:
                st.error("❌ Failed to fetch weather. Please check your API key or limits.")
                st.json(data)
                st.stop()

            current = data['current']
            location_data = data['location']

            # Display location and local time
            st.subheader(f"📍 Current Weather in {location_data['name']}, {location_data['region']}, {location_data['country']}")
            st.write(f"🕒 Local Time: {location_data['localtime']}")

            # Real-time temperature and condition
            st.metric("🌡️ Temperature", f"{current['temp_c']} °C")
            st.write("📋 Condition:", current['condition']['text'])
            st.write("💧 Humidity:", f"{current['humidity']}%")
            st.write("🌬️ Wind Speed:", f"{current['wind_kph']} kph")

            # Note: Sunrise is not in current endpoint, you need forecast API for that
            st.info("🌅 Sunrise/Sunset data is available in forecast API, not current API.")

            # Air Quality Index data
            st.subheader("🌫️ Air Quality Index (AQI)")
            if 'air_quality' in current:
                aqi = current['air_quality']
                st.write("🧪 PM2.5:", round(aqi['pm2_5'], 2), "μg/m³")
                st.write("🧪 PM10:", round(aqi['pm10'], 2), "μg/m³")
                st.write("🧪 CO:", round(aqi['co'], 2), "μg/m³")
                st.write("🧪 NO₂:", round(aqi['no2'], 2), "μg/m³")
                st.write("🧪 O₃:", round(aqi['o3'], 2), "μg/m³")
                st.write("🧪 SO₂:", round(aqi['so2'], 2), "μg/m³")
            else:
                st.warning("⚠️ AQI data not available for this location.")

        except Exception as e:
            st.error("⚠️ Something went wrong.")
            st.exception(e)
