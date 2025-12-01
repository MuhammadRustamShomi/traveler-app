import os
import requests
import streamlit as st

# ============= API KEY =====================
GEMINI_API_KEY = os.environ.get("AIzaSyCnMXLuHSSWDoFk4B9peXoyWpZqpy9K7MA")

if not GEMINI_API_KEY:
    st.error("❌ ERROR: GEMINI_API_KEY not found in Streamlit Secrets!")
    st.stop()

# ============= Gemini REST API ==============
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY

# ============= OpenTripMap API (Free) ========
OPENTRIPMAP_API_KEY = "5ae2e3f221c38a28845f05b6"


def geocode(city):
    url = "https://api.opentripmap.com/0.1/en/places/geoname"
    params = {"name": city, "apikey": OPENTRIPMAP_API_KEY}
    return requests.get(url, params=params).json()


def get_pois(lat, lon, limit=5):
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


def generate_ai_response(prompt):
    body = { "contents": [{ "parts": [{ "text": prompt }] }] }
    response = requests.post(GEMINI_URL, json=body)

    try:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "AI Error: Could not generate response."


# -------------------- UI --------------------
st.title("🌍 Simple Free AI Travel Chatbot")

with st.form("form"):
    city = st.text_input("Destination", "Dubai")
    days = st.number_input("Days", 1, 10, 3)
    budget = st.text_input("Budget", "300 USD")
    btn = st.form_submit_button("Generate Travel Plan")

if btn:
    st.info("📍 Finding city...")

    geo = geocode(city)
    if "lat" not in geo:
        st.error("City not found!")
        st.stop()

    lat, lon = geo["lat"], geo["lon"]

    st.success(f"City found: {city}")

    st.info("🏙 Getting attractions...")
    pois = get_pois(lat, lon)
    st.write("Attractions:", pois)

    poi_text = ", ".join(pois)

    prompt = f"""
Create a detailed travel plan for {city}.

Days: {days}
Budget: {budget}
Popular places: {poi_text}

Include:
- Day-wise itinerary
- Budget-friendly hotels
- Best season
- Food places
- Tips & warnings
"""

    st.info("🤖 Generating travel plan...")
    result = generate_ai_response(prompt)

    st.subheader("✨ Travel Plan")
    st.write(result)
