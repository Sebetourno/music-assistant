import openai
import os
from flask import Flask, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build

# Charger les variables d'environnement
from dotenv import load_dotenv
load_dotenv()

# Clés API
openai.api_key = os.getenv("OPENAI_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Initialisation de Flask
app = Flask(__name__)

# Initialisation de Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

# Initialisation de YouTube API
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Route principale
@app.route("/")
def home():
    return "🎵 Music Assistant API is Running!"

# Route pour interagir avec OpenAI GPT
@app.route("/ask", methods=["POST"])
def ask_openai():
    question = request.json.get("question")

    # Interroger OpenAI GPT
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        max_tokens=100
    )
    
    return jsonify({"answer": response.choices[0].text.strip()})

# Route pour obtenir des playlists Spotify
@app.route("/spotify", methods=["GET"])
def get_spotify_playlists():
    track = request.args.get("track")
    results = sp.search(q=track, limit=5, type="track")
    tracks = [{"name": track["name"], "artist": track["artists"][0]["name"]} for track in results["tracks"]["items"]]
    return jsonify({"tracks": tracks})

# Route pour obtenir des vidéos YouTube
@app.route("/youtube", methods=["GET"])
def get_youtube_videos():
    query = request.args.get("query")
    request = youtube.search().list(q=query, part="snippet", type="video", maxResults=5)
    response = request.execute()
    videos = [{"title": item["snippet"]["title"], "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"} for item in response["items"]]
    return jsonify({"videos": videos})

if __name__ == "__main__":
    app.run(debug=True)
