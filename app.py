import os
import openai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build

# Charger les clés API à partir des variables d'environnement
openai.api_key = os.getenv("OPENAI_API_KEY")
spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
youtube_api_key = os.getenv("YOUTUBE_API_KEY")

# Fonction pour interroger l'API OpenAI
def query_openai(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Fonction pour rechercher des vidéos YouTube
def search_youtube(query):
    youtube = build("youtube", "v3", developerKey=youtube_api_key)
    request = youtube.search().list(q=query, part="snippet", maxResults=5)
    response = request.execute()
    return [item['snippet']['title'] for item in response['items']]

# Fonction pour rechercher des morceaux sur Spotify
def search_spotify(query):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret))
    results = sp.search(q=query, limit=5)
    return [track['name'] for track in results['tracks']['items']]

# Exemple de prompt pour OpenAI
prompt = "Recommande-moi des morceaux de musique à la manière d'Imagine Dragons."
gpt_response = query_openai(prompt)

# Recherche sur YouTube et Spotify
youtube_results = search_youtube("Imagine Dragons music")
spotify_results = search_spotify("Imagine Dragons")

# Afficher les résultats
print(f"OpenAI: {gpt_response}")
print(f"YouTube: {youtube_results}")
print(f"Spotify: {spotify_results}")
