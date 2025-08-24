import streamlit as st
import requests
import google.generativeai as genai
from rule_based import forward_chaining

# --- Page Configuration ---
st.set_page_config(
    page_title="Intelligent Weather Predictor",
    page_icon="🌦️",
    layout="wide"
)

# --- API Configuration ---
try:
    WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except KeyError:
    st.error("API keys not found. Please add them to your .streamlit/secrets.toml file.")
    st.stop()

# --- Weather Pictorials ---
WEATHER_ICONS = {
    "Clear Skies": "☀️",
    "Pleasant and Sunny": "😊",
    "Overcast Skies": "☁️",
    "Light Rain or Drizzle": "🌦️",
    "Heavy Rain Expected": "🌧️",
    "High Chance of Thunderstorms": "⛈️",
    "Snowfall Likely": "❄️",
    "Stormy Weather": "🌪️",
    "Windy Conditions": "💨",
    "Strong Wind Warning": "🚩",
    "Fog or Mist Likely": "🌫️",
    "Extremely Hot": "🥵",
    "Very Hot": "🔥",
    "Freezing Cold": "🥶",
    "High UV Index: Use Sun Protection": "😎",
    "Low Visibility": "👀",
    "Default": "🌍"
}

# --- Functions ---
def get_weather_data(city):
    """Fetches weather data from OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def get_gemini_response(facts, conclusions):
    """Generates a descriptive weather narrative using Gemini API."""
    prompt = f"""
    Based on the following weather data and rule-based conclusions, generate a friendly and descriptive weather forecast.

    **Weather Data:**
    - Temperature: {facts.get('temp', 'N/A')}°C
    - Feels Like: {facts.get('feels_like', 'N/A')}°C
    - Humidity: {facts.get('humidity', 'N/A')}%
    - Wind Speed: {facts.get('wind_speed', 'N/A')} m/s
    - Cloudiness: {facts.get('clouds', 'N/A')}%
    - Pressure: {facts.get('pressure', 'N/A')} hPa
    - Main Condition: {facts.get('main_condition', 'N/A')}

    **Expert System Conclusions:**
    {', '.join(conclusions) if conclusions else 'No specific conclusions.'}

    **Your Task:**
    Write a short, engaging weather report. Be conversational and helpful. For example, if there's a high UV index, advise wearing sunscreen. If it's stormy, suggest staying indoors.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Could not generate AI forecast: {e}"

# --- Streamlit UI ---
st.title("🌦️ Intelligent Weather Prediction System")
st.markdown("Enter a city name to get a smart weather forecast.")

city = st.text_input("Enter City Name:", "")

if st.button("Get Forecast"):
    if not city:
        st.warning("Please enter a city name.")
    else:
        with st.spinner(f"Fetching weather data for {city}..."):
            data = get_weather_data(city)

        if data:
            st.success("Data fetched successfully!")

            # Prepare facts for the rule-based system
            facts = {
                'temp': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'clouds': data['clouds']['all'],
                'pressure': data['main']['pressure'],
                'visibility': data.get('visibility', 10000), # Default to 10km
                'main_condition': data['weather'][0]['main'],
                # Mock data for rules not covered by free API
                'precipitation_prob': data.get('pop', 0) * 100, # Probability of precipitation if available
                'uv_index': 7 # Placeholder UV index
            }

            # Run the Rule-Based System
            conclusions = forward_chaining(facts)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 Raw Weather Data")
                st.write(f"**Temperature:** {facts['temp']}°C")
                st.write(f"**Humidity:** {facts['humidity']}%")
                st.write(f"**Wind Speed:** {facts['wind_speed']} m/s")
                st.write(f"**Cloudiness:** {facts['clouds']}%")
                st.write(f"**Condition:** {facts['main_condition']}")

            with col2:
                st.subheader("🧠 Expert System Analysis")
                if conclusions:
                    for conclusion in conclusions:
                        icon = WEATHER_ICONS.get(conclusion, WEATHER_ICONS['Default'])
                        st.markdown(f"- {icon} {conclusion}")
                else:
                    st.write("No specific conditions triggered the expert rules.")
            
            st.divider()

            st.subheader("🤖 Weather Forecast")
            with st.spinner("Generating AI-powered narrative..."):
                ai_forecast = get_gemini_response(facts, conclusions)
                st.markdown(ai_forecast)