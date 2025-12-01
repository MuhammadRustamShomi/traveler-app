
import os
import requests
import streamlit as st
import google.generativeai as genai

# ---------------------------------------------
#  LOAD GOOGLE GEMINI API KEY (from Streamlit Secrets)
# ---------------------------------------------
GEMINI_API_KEY = os.environ.get("AIzaSyCnMXLuHSSWDoFk4B9peXoyWpZqpy9K7MA")

if not GEMINI_API_KEY:
    st.error("❌ ERROR: GEMINI_API_KEY is not set in Streamlit Secrets!")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# ---------------------------------------------
#   STREAMLIT UI
# ---------------------------------------------
st.set_page_config(page_title="🌍 AI Travel Chatbot", layout="wide")
st.title("🌍 Free AI Travel Chatbot (Gemini + Free APIs)")

# FREE OpenTripMap API (public demo key)
OPENTRIPMAP_API_KEY = "5ae2e3f221c38a28845f05b6"

# ---------------------------------------------
# GEO LOCATION API
# ---------------------------------------------
def geocode(city):
    url = "https://api.opentripmap.com/0.1/en/places/geoname"
    params = {"name": city, "apikey": OPENTRIPMAP_API_KEY}
    r = requests.get(url, params=params).json()
    return r

# ---------------------------------------------
# GET TOP ATTRACTIONS
# ---------------------------------------------
def get_pois(lat, lon, limit=7):
    url = "https://api.opentripmap.com/0.1/en/places/radius"
    params = {
        "radius": 5000,
        "lon": lon,
        "lat": lat,
        "limit": limit,
        "apikey": OPENTRIPMAP_API_KEY
    }
    data = requests.get(url, params=params).json()

    places = []
    for item in data.get("features", []):
        name = item["properties"].get("name")
        if name:
            places.append(name)
    return places

# ---------------------------------------------
#  AI TRAVEL ITINERARY GENERATION (Gemini)
# ---------------------------------------------
def generate_itinerary(city, days, budget, poi_list):
    poi_text = ", ".join(poi_list)

    prompt = f"""
Create a detailed travel plan.

City: {city}
Days: {days}
Budget: {budget}
Popular attractions: {poi_text}

Return:
1. Day-by-day itinerary
2. Best places to visit
3. Budget-friendly hotels
4. Food recommendations
5. Total budget estimate
6. Best travel season
7. Safety + local travel tips
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text


# ---------------------------------------------
#  USER INPUT FORM
# ---------------------------------------------
with st.form("travel_form"):
    city = st.text_input("Enter Destination City", "Dubai")
    days = st.slider("Number of Days", 1, 10, 3)
    budget = st.text_input("Your Budget (e.g., 300 USD)", "400 USD")
    submit = st.form_submit_button("Generate Travel Plan")

# ---------------------------------------------
#  RUNNING THE BOT
# ---------------------------------------------
if submit:
    st.info("📍 Finding city location...")

    geo = geocode(city)
    if "lat" not in geo:
        st.error("❌ City not found! Try another name.")
        st.stop()

    lat, lon = geo["lat"], geo["lon"]
    st.success(f"City found: {city} (Lat: {lat}, Lon: {lon})")

    st.info("🏙 Finding popular attractions near the location...")
    pois = get_pois(lat, lon)

    if len(pois) == 0:
        st.warning("⚠ No attractions found. Still generating AI plan.")
    else:
        st.write("Top attractions:", pois)

    st.info("🤖 Generating travel plan using FREE Google Gemini API...")
    plan = generate_itinerary(city, days, budget, pois)

    st.subheader("✨ Your AI Travel Plan")
    st.write(plan)

