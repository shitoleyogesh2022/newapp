from flask import Flask, render_template
import feedparser
import random

app = Flask(__name__)

# Example RSS feeds (Shayari + Jokes)
RSS_FEEDS = [
    "https://www.typingbaba.com/blog/feed/",   # Hindi related
    "https://www.typingbaba.com/blog/category/jokes/feed/",
    "https://www.typingbaba.com/blog/category/shayari/feed/"
]

def get_random_quote():
    entries = []
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            entries.extend(feed.entries)
        except:
            pass
    if entries:
        choice = random.choice(entries)
        return choice.title
    return "You are my favorite notification ❤️"

@app.route("/")
def index():
    quote = get_random_quote()
    return render_template("index.html", quote=quote)

if __name__ == "__main__":
    app.run(debug=True)