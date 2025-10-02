import streamlit as st
import requests
import random
import datetime
from functools import lru_cache
import openai # you’ll use this for custom content
from openai import OpenAI
import os
from dotenv import load_dotenv 
load_dotenv()
# --- Configure your OpenAI key ---
try:
    # Try getting the API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # If not in environment, try getting from secrets
        api_key = st.secrets["openai_api_key"]
    
    client = OpenAI(api_key=api_key)
    
except Exception as e:
    st.error(f"Failed to initialize OpenAI client: {str(e)}")
    # Set a flag to use fallback responses
    USE_FALLBACK = True
else:
    USE_FALLBACK = False
    
    
PERENUAL_KEY = os.getenv("PERENUAL_KEY", "sk-Dcg068deda0fd7d7912644")



def test_openai_connection():
    try:
        test_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        st.sidebar.success("✅ OpenAI API connection successful")
        return True
    except Exception as e:
        st.sidebar.error(f"❌ OpenAI API connection failed: {str(e)}")
        return False

# Test connection
is_api_working = test_openai_connection()
    

#TREFLE_KEY = st.secrets.get("TREFLE_KEY", "") # if you also use Trefle
# ------------------ Helper API functions ------------------
@st.cache_data(ttl=3600)
def fetch_hindi_shayari():
    """
    Fetch a Hindi quote / shayari with better error handling
    """
    # Fallback quotes
    local = [
        ("तेरी मुस्कान मेरी सबसे बड़ी कमान है", ""),
        ("हर शब तेरे ख्वाबों में खो जाऊँ", ""),
        ("तेरे बिना दिल को हो गई है तन्हाई", "")
    ]
    
    try:
        url = "https://apislist.com/api/2372/hindi-quotes-and-shayari-free-api"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            try:
                j = res.json()
                quote = j.get("quote") or j.get("shayari")
                author = j.get("author", "")
                if quote:
                    return quote, author
            except ValueError:
                return random.choice(local)
    except Exception as e:
        st.write(f"Using fallback quotes due to API error: {e}")
    
    return random.choice(local)
    
@st.cache_data(ttl=3600)
def fetch_english_quote():
    """
    Fetch a general quote (English) via ZenQuotes API.
    """
    try:
        res = requests.get(" https://zenquotes.io/api/random", timeout=5)
        if res.status_code == 200:
            arr = res.json()
            if isinstance(arr, list) and len(arr) > 0:
                q = arr[0].get("q")
                a = arr[0].get("a")
                return q, a
    except Exception as e:
        st.write("Error fetching zen quote:", e)
    # fallback
    return "Love yourself, always.", "Unknown"
@st.cache_data(ttl=3600)
def fetch_plant_info():
    """
    Fetch a random plant species via Perenual API (if key available).
    """
    if not PERENUAL_KEY:
        return None
    try:
        # fetch species list, random page
        page = random.randint(1, 50)
        url = f"https://perenual.com/api/v2/species-list?key={PERENUAL_KEY}&page={page}"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            j = res.json()
            data = j.get("data", [])
            if data:
                plant = random.choice(data)
                return {
                    "common_name": plant.get("common_name"),
                    "scientific_name": plant.get("scientific_name"),
                    "image_url": plant.get("default_image", {}).get("original_url")
                }
    except Exception as e:
        st.write("Error fetching plant info:", e)
    return None
def openai_generate_shayari(prompt: str):
    """
    Use OpenAI to generate a personalized shayari with improved error handling
    """
    if USE_FALLBACK:
        return get_fallback_response(prompt)
        
    fallback_responses = {
        "romantic": [
            "Love is like a garden, growing more beautiful each day",
            "In your eyes, I see my future bright and clear",
            "Every moment with you is a treasure to keep"
        ],
        "fun": [
            "You're the pastry to my tea",
            "Like a tortoise, my love is slow but forever",
            "Together we bloom like spring flowers"
        ]
    }
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=60,
            temperature=0.8,
            timeout=10  # Add timeout
        )
        return response.choices[0].message.content
    except Exception as e:
        st.write(f"Using fallback due to API error: {str(e)}")
        if "romantic" in prompt.lower():
            return random.choice(fallback_responses["romantic"])
        return random.choice(fallback_responses["fun"])
    
def get_fallback_response(prompt):
    """
    Get appropriate fallback response based on prompt type
    """
    romantic_responses = [
        "Love is like a garden, growing more beautiful each day",
        "In your eyes, I see my future bright and clear",
        "Every moment with you is a treasure to keep",
        "Like stars in the night sky, our love shines eternal",
        "Together we write our story of forever"
    ]
    
    fun_responses = [
        "You're the sweetness in my pastry",
        "Like a patient tortoise, our love is steady and true",
        "Together we bloom like spring flowers",
        "You make my heart dance with joy",
        "Life is sweeter with you by my side"
    ]
    
    if any(word in prompt.lower() for word in ["romantic", "love", "heart", "forever"]):
        return random.choice(romantic_responses)
    return random.choice(fun_responses)    
    
# ------------------ Streamlit UI & logic ------------------
st.set_page_config(page_title="For You💖", page_icon="", layout="centered")
st.title("Just for You")
today = datetime.datetime.now().strftime("%A, %d %B %Y")
st.write(f"**{today}**")
# Shayari / Quote Section
st.header("Shayari / Quote for You")
# Random choice: either fetch from Hindi API, or use OpenAI to generate a custom one
if random.random() < 0.5:
    q, a = fetch_hindi_shayari()
    if q:
        st.write(f"> {q}")
        if a:
            st.write(f"— {a}")
    else:
        # fallback to OpenAI
        prompt = "Write a romantic Hindi shayari about love and moonlight"
        sh = openai_generate_shayari(prompt)
        st.write(sh)
else:
    q, a = fetch_english_quote()
    st.write(f"> {q}")
    st.write(f"— {a}")
# Sweet / Comedy / Fun Section
st.header("A Little Fun")
# Use OpenAI to generate a cute line combining her passions
prompt_fun = ("Write a lighthearted, romantic one-line in Hindi or English that mentions plants, "
              "tortoise or pastry, in a playful way.")
fun_line = openai_generate_shayari(prompt_fun)
if fun_line:
    st.write(fun_line)
else:
    # fallback
    st.write("You + me + pastry = perfect trio")
# Music (same as before)
st.header("🎶A Song You Love")
songs = [
    ("Sai by Satinder Sartaj", " https://www.youtube.com/watch?v=7S0Z_JcVZ5Q"),
    ("Udaarian by Satinder Sartaj", " https://www.youtube.com/watch?v=H24t0xTN1ss"),
    ("Laadli by Satinder", " https://www.youtube.com/watch?v=quPz6p1Qj58")
]
song = random.choice(songs)
st.write(f"**{song[0]}**")
st.video(song[1])
# Pastry / Sweet Corner
st.header("Sweet Thoughts")
prompt_sweet = "Write a romantic line about truffle pastry and sweetness of love"
sweet_line = openai_generate_shayari(prompt_sweet)
if sweet_line:
    st.write(sweet_line)
else:
    st.write("Sweet like chocolate, but sweeter is my love for you")
st.image(" https://upload.wikimedia.org/wikipedia/commons/0/05/Chocolate_truffle_cake.jpg",
         caption="A little treat for you")
# Plant / Nature Section
st.header("🌿Plant of the Day")
plant = fetch_plant_info()
if plant:
    st.write(f"**{plant.get('common_name')}** (aka *{plant.get('scientific_name')}*)")
    if plant.get("image_url"):
        st.image(plant.get("image_url"), width=300)
    st.write("May our love grow like this plant 🌱")
else:
    st.write("Green like your spirit🍃")
# Tortoise Friend
st.header("🐢Your Tortoise Says")
prompt_tort = "Write a small heartfelt message from a tortoise, about love and patience."
tmsg = openai_generate_shayari(prompt_tort)
if tmsg:
    st.write(tmsg)
else:
    st.write("Slow and steady, always by your side 🐢")
st.image(" https://upload.wikimedia.org/wikipedia/commons/5/54/Hermann_tortoise.jpg",
         caption="Your little friend")
# Sparkle / Diamond Section
st.header("💎You Shine")
prompt_dia = "Write a romantic line comparing her to a diamond"
dmsg = openai_generate_shayari(prompt_dia)
if dmsg:
    st.write(dmsg)
else:
    st.write("More precious than any gem ✨")
st.image(" https://upload.wikimedia.org/wikipedia/commons/4/4f/Diamond.jpg",
         caption="Sparkling like you")
# Reveal Your Heart
st.header("💌Open My Heart")
if st.button("Tap to Reveal"):
    # Use OpenAI to generate a heartfelt proposal or letter
    prompt_proposal = ("Write a romantic proposal in Hindi or mixed Hindi-English, "
                       "expressing deep love, sincerity.")
    proposal = openai_generate_shayari(prompt_proposal)
    if proposal:
        st.success(proposal)
    else:
        st.success("I love you deeply. Kuttaa")
