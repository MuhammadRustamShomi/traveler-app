import os
import requests
import streamlit as st
import google.generativeai as genai
import json

# ---------------------------
#  SET YOUR FREE GOOGLE API KEY
# ---------------------------
GEMINI_API_KEY = "AIzaSyCnMXLuHSSWDoFk4B9peXoyWpZqpy9K7MA"
OPENTRIPMAP_API_KEY = "5ae2e3f221c38a28845f05b6"   # Free Demo Key (public)

genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="Free AI Travel Chatbot", layout="wide")
st.title("🌍 Free AI Travel Chatbot (Gemini + Free APIs)")

# ---------------------------
#  GEO + POIs (OPEN TRIP MAP)
# ---------------------------

def geocode(city):
    url = "https://api.opentripmap.com/0.1/en/places/geoname"
    params = {"name": city, "apikey": OPENTRIPMAP_API_KEY}
    r = requests.get(url, params=params).json()
    return r

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

# ---------------------------
#  GEMINI AI TRAVEL PLANNER
# ---------------------------

def generate_itinerary(city, days, budget, poi_list):
    prompt = f"""
You are an expert travel planner. Create a detailed travel plan.

City: {city}
Days: {days}
Budget: {budget}
Places of interest: {poi_list}

Return:
1) Day-by-day itinerary
2) Recommended places to visit
3) Hotels (budget-friendly)
4) Food recommendations
5) Total budget estimate
6) Best season to visit
7) Travel tips
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text


# ---------------------------
#   UI FORM
# ---------------------------

with st.form("travel"):
    city = st.text_input("Destination City", "Dubai")
    days = st.number_input("How many days?", 1, 10, 3)
    budget = st.text_input("Budget (e.g., USD 500)", "USD 400")
    submit = st.form_submit_button("Generate Travel Plan")

if submit:
    st.info("Fetching location...")

    geo = geocode(city)
    if "lat" not in geo:
        st.error("City not found! Try another city.")
        st.stop()

    lat, lon = geo["lat"], geo["lon"]

    st.success(f"Found location: {city} (Lat: {lat}, Lon: {lon})")

    st.info("Finding top attractions...")
    pois = get_pois(lat, lon)

    st.write("Top attractions found:", pois)

    st.info("Generating AI travel plan using FREE Gemini API...")

    result = generate_itinerary(city, days, budget, pois)

    st.subheader("✨ Your AI Travel Plan")
    st.write(result)
