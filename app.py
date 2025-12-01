import streamlit as st
import requests

st.set_page_config(page_title="AI Travel Chatbot", page_icon="🌍")

st.title("🌍 Simple AI Travel Chatbot (FREE APIs, No AI Key Needed)")

# -------------------------------------------------------------------
# FREE Public APIs (No Auth Required)
# -------------------------------------------------------------------
def get_wikipedia_summary(place):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{place}"
        res = requests.get(url).json()
        return res.get("extract", "No info found.")
    except:
        return "Wikipedia info unavailable."

def get_weather(place):
    try:
        url = f"https://wttr.in/{place}?format=3"
        return requests.get(url).text
    except:
        return "Weather data unavailable."

def get_hotels(place):
    fake_hotels = [
        "Hotel Grand Palace",
        "City View Resort",
        "Blue Orchid Inn",
        "Comfort Stay Hotel",
    ]
    return fake_hotels

def generate_itinerary(place, days):
    return [
        f"Day 1: Explore main city attractions of {place}.",
        f"Day 2: Visit famous landmarks and local food streets.",
        f"Day {days}: Shopping & relaxing before departure."
    ]


# -------------------------------------------------------------------
# MAIN CHATBOT LOGIC
# -------------------------------------------------------------------
place = st.text_input("✈ Enter travel destination:")

days = st.number_input("🗓 Number of days:", min_value=1, max_value=30, value=3)

budget = st.selectbox(
    "💰 Budget range:",
    ["Low", "Medium", "High"]
)

if st.button("Generate Travel Plan"):
    if place.strip() == "":
        st.warning("Please enter a destination.")
    else:
        st.subheader(f"📝 Travel Plan for **{place}**")

        # Wikipedia info
        st.write("### 📘 Destination Overview")
        st.write(get_wikipedia_summary(place))

        # Weather info
        st.write("### 🌤 Current Weather")
        st.write(get_weather(place))

        # Hotels
        st.write("### 🏨 Recommended Hotels")
        hotels = get_hotels(place)
        for h in hotels:
            st.write("- " + h)

        # Itinerary
        st.write("### 🗺 Suggested Itinerary")
        itinerary = generate_itinerary(place, days)
        for item in itinerary:
            st.write("➡ " + item)

        # Travel Tips
        st.write("### 💡 Travel Tips")
        st.write("""
- Keep your documents scanned online  
- Carry a small medical kit  
- Check weather before travel  
- Explore local food & culture  
""")


st.markdown("---")
st.info("Made with ❤️ by Muhammad Rustam")

