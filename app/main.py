from fastapi import FastAPI, Depends, HTTPException,Query, Request,APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from urllib.parse import urlencode
import logging
import os
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
import secrets



app = FastAPI()
load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
router = APIRouter()
#Spotify App Credentials-pasted from Spotify Developer Dashboard
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
SPOTIFY_SCOPE = "playlist-modify-private playlist-modify-public"
app.include_router(router)
# Generate a 32-byte long secret key
secret_key = secrets.token_hex(32)

print(secret_key)
app.add_middleware(
    SessionMiddleware, secret_key=secret_key
)

# OAuth2 Details
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

# Initialize Spotify OAuth2 object
sp_oauth = SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri='http://localhost:8000/auth/callback',
    scope=os.getenv('SPOTIFY_SCOPE')
)

async def get_access_token(code: str):
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info['access_token']
    return access_token

async def get_access_token(request: Request):
    access_token = request.session.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="No access token in session")
    return access_token

@app.get("/auth/login")
def login():
    try:
        auth_url = sp_oauth.get_authorize_url()
        print(f"Auth URL: {auth_url}")  # Add this line
        print(f"Redirect URI: {SPOTIFY_REDIRECT_URI}")  # Add this line
        response = RedirectResponse(url=auth_url)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/auth/callback")
async def callback(request: Request, code: str = Query(...)):
    try:
        # Exchange the authorization code for an access token
        token_info = sp_oauth.get_access_token(code, as_dict=True)
        request.session["access_token"] = token_info['access_token']
        return JSONResponse({"access_token": request.session["access_token"]})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.get("/searchSong/{query}")
async def search_song(query: str, request:Request, access_token: str = Depends(get_access_token)):
    try:
        print(f"Redirect URI: {query}")
        sp = spotipy.Spotify(auth=access_token)
        print(f"Redirect URI: {query}")
        results = sp.search(q='track:'+ query, limit = 1, type='track')
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/createPlaylist")
def create_playlist(playlist_name: str, access_token: str = Depends(callback)):
    try:
        sp = spotipy.Spotify(auth=access_token)
        user_id = sp.current_user()["id"]
        playlist = sp.user_playlist_create(user_id, playlist_name)
        return playlist
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/addSongToPlaylist")
def addSongToPlaylist(playlist_id: str, song_uri: str, access_token: str = Depends(callback)):
    try:
        sp = spotipy.Spotify(auth=access_token)
        sp.playlist_add_items(playlist_id, [song_uri])
        return {"message": "Song added to playlist"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

