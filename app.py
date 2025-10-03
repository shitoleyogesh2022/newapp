from flask import Flask, render_template
import random
import requests
import json
from datetime import datetime
import os

app = Flask(__name__)

# Local content as fallback
LOCAL_CONTENT = {
    'songs': [
        {
            'name': "Peaceful Piano",
            'artist': "Relaxing Music",
            'audio_url': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
            'type': 'audio'
        },
        {
            'name': "Gentle Guitar",
            'artist': "Acoustic Tunes",
            'audio_url': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
            'type': 'audio'
        },
        {
            'name': "Nature Sounds",
            'artist': "Meditation Music",
            'audio_url': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
            'type': 'audio'
        }
    ],
    'shayari': [
        "तेरी मुस्कुराहट से मेरी दुनिया सजती है,\nतेरी खुशी में मेरी खुशी छुपी है।",
        "दिल की दुनिया में तेरा घर है,\nतू नहीं तो ये दिल भी बेघर है।"
    ],
    'jokes': [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? He was outstanding in his field!"
    ],
    'quotes': [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "In the middle of difficulty lies opportunity. - Albert Einstein"
    ]
}
def get_random_song():
    try:
        # You can add API call here to get music from external source
        return random.choice(LOCAL_CONTENT['songs'])
    except Exception as e:
        print(f"Error getting song: {e}")
        # Fallback song
        return {
            'name': "Peaceful Piano",
            'artist': "Relaxing Music",
            'audio_url': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
            'type': 'audio'
        }
    # Your existing get_random_song function here
    # If you don't have this function, use the following:
    return random.choice(LOCAL_CONTENT['songs'])

def get_random_shayari():
    return random.choice(LOCAL_CONTENT['shayari'])

def get_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=5)
        if response.status_code == 200:
            joke_data = response.json()
            return f"{joke_data['setup']} {joke_data['punchline']}"
    except:
        return random.choice(LOCAL_CONTENT['jokes'])

def get_random_image(query):
    try:
        response = requests.get(f"https://source.unsplash.com/featured/?{query}", timeout=5)
        if response.status_code == 200:
            return response.url
    except:
        return f"https://via.placeholder.com/400x300?text={query.capitalize()}+Image"

def get_quote():
    try:
        response = requests.get("https://api.quotable.io/random", timeout=5)
        if response.status_code == 200:
            return response.json()['content']
    except:
        return random.choice(LOCAL_CONTENT['quotes'])

@app.route("/")
def home():
    content = {
        'shayari': get_random_shayari(),
        'joke': get_joke(),
        'song': get_random_song(),
        'tortoise_image': get_random_image('tortoise'),
        'plant_image': get_random_image('plant'),
        'quote': get_quote(),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return render_template("index.html", content=content)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
