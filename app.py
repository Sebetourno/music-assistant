import os
from flask import Flask, request, render_template
import openai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

app = Flask(__name__)

# Chargement des clés API depuis les variables d'environnement
openai.api_key = os.getenv('OPENAI_API_KEY')
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
youtube_api_key = os.getenv('YOUTUBE_API_KEY')

# Configuration de Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret))

@app.route('/')
def home():
    return "Music Assistant is running!"

@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        user_query = request.form['query']
        # Appel à OpenAI pour obtenir une réponse
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=user_query,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    return render_template('index.html')

@app.route('/spotify')
def spotify():
    # Exemple de recherche sur Spotify
    results = sp.search(q='Daft Punk', limit=1)
    return results['tracks']['items'][0]['name']

@app.route('/youtube')
def youtube():
    # Exemple d'utilisation de l'API YouTube
    query = 'Daft Punk'
    youtube_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={youtube_api_key}"
    response = requests.get(youtube_url)
    video_data = response.json()
    return video_data['items'][0]['snippet']['title']

if __name__ == "__main__":
    app.run(debug=True)
