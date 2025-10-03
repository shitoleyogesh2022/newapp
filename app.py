from flask import Flask, render_template
import feedparser
import random
import requests
import json
from datetime import datetime

app = Flask(__name__)

# Local content as fallback
LOCAL_CONTENT = {
    'songs': [
        ("Sai by Satinder Sartaj", "https://www.youtube.com/embed/7S0Z_JcVZ5Q"),
        ("Udaarian by Satinder Sartaj", "https://www.youtube.com/embed/H24t0xTN1ss"),
        ("Laadli by Satinder", "https://www.youtube.com/embed/quPz6p1Qj58")
    ],
    'images': {
        'tortoise': [
            "https://upload.wikimedia.org/wikipedia/commons/3/3d/Tortoise_in_grass.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/8/85/Desert_tortoise.jpg"
        ],
        'plant': [
            "https://upload.wikimedia.org/wikipedia/commons/2/2f/Indoor_plant.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/a/a5/Garden_plant.jpg"
        ]
    },
    'messages': [
        "You make my day brighter ☀️",
        "Keep smiling, keep shining ✨",
        "You're amazing! 💖"
    ]
}

def get_quote():
    try:
        response = requests.get("https://api.quotable.io/random")
        if response.status_code == 200:
            return response.json()['content']
    except:
        return random.choice(LOCAL_CONTENT['messages'])

def get_joke():
    try:
        headers = {'Accept': 'application/json'}
        response = requests.get("https://icanhazdadjoke.com/", headers=headers)
        if response.status_code == 200:
            return response.json()['joke']
    except:
        return "Why did the cookie go to the doctor? Because it was feeling crumbly! 😄"

@app.route("/")
def home():
    content = {
        'quote': get_quote(),
        'joke': get_joke(),
        'song': random.choice(LOCAL_CONTENT['songs']),
        'tortoise_image': random.choice(LOCAL_CONTENT['images']['tortoise']),
        'plant_image': random.choice(LOCAL_CONTENT['images']['plant']),
        'message': random.choice(LOCAL_CONTENT['messages']),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return render_template("index.html", content=content)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
