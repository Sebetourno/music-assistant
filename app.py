import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer les clés API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Vérifier si les clés sont chargées correctement
if not all([OPENAI_API_KEY, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, YOUTUBE_API_KEY]):
    raise ValueError("Une ou plusieurs clés API manquent. Vérifiez votre fichier .env.")
