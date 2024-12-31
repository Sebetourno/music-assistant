import os
import openai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from dotenv import load_dotenv
from flask import Flask

# Charger les variables d'environnement
load_dotenv()

# Clés API depuis les variables d'environnement
openai.api_key = os.getenv("OPENAI_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Initialiser Flask
app = Flask(__name__)

# Initialiser Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

@app.route('/')
def home():
    return "🎵 Music Assistant API is Running!"

@app.route('/recommendations')
def recommendations():
    prompt = "Give me music recommendations for Imagine Dragons"
    
    # Appel à OpenAI GPT
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )

    openai_response = response.choices[0].text.strip()
    
    # Exemple d'utilisation de Spotify pour rechercher un morceau
    results = sp.search(q=openai_response, limit=5, type="track")
    tracks = [track['name'] for track in results['tracks']['items']]
    
    return f"Recommended songs: {', '.join(tracks)}"

if __name__ == '__main__':
    app.run(debug=True)
