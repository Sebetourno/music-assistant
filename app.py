import os
from dotenv import load_dotenv
import openai
import requests
from flask import Flask, request, jsonify

# Charger les variables d'environnement
load_dotenv()

# Récupérer les clés API depuis le fichier .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Vérifier si les clés sont correctement chargées
if not all([OPENAI_API_KEY, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, YOUTUBE_API_KEY]):
    raise ValueError("❌ Une ou plusieurs clés API manquent. Vérifiez votre fichier .env.")

# Configuration de l'API OpenAI
openai.api_key = OPENAI_API_KEY

# Initialisation de l'application Flask
app = Flask(__name__)

### 🎵 ROUTE POUR SPOTIFY ###
@app.route('/spotify', methods=['GET'])
def spotify_search():
    query = request.args.get('query', 'Imagine Dragons')
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET
    }

    # Obtenir un token Spotify
    response = requests.post(token_url, headers=headers, data=data)
    access_token = response.json().get('access_token')

    if not access_token:
        return jsonify({"error": "❌ Impossible d'obtenir le token Spotify"}), 500

    search_url = f'https://api.spotify.com/v1/search?q={query}&type=track'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(search_url, headers=headers)
    tracks = response.json().get('tracks', {}).get('items', [])

    return jsonify(tracks)

### 📺 ROUTE POUR YOUTUBE ###
@app.route('/youtube', methods=['GET'])
def youtube_search():
    query = request.args.get('query', 'Imagine Dragons')
    search_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={YOUTUBE_API_KEY}'

    response = requests.get(search_url)
    videos = response.json().get('items', [])

    return jsonify(videos)

### 🤖 ROUTE POUR OPENAI ###
@app.route('/chat', methods=['POST'])
def openai_chat():
    data = request.get_json()
    user_input = data.get('message', '')

    if not user_input:
        return jsonify({"error": "❌ Aucun message fourni"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a music assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message['content']
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

### 🏠 ROUTE D'ACCUEIL ###
@app.route('/')
def home():
    return "<h1>🎵 Music Assistant API is Running!</h1>"

### 🚀 LANCEMENT DE L'APPLICATION ###
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
