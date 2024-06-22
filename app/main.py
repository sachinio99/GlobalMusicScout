from fastapi import FastAPI, Depends, HTTPException,Query, Request,APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
import os
from dotenv import load_dotenv


app = FastAPI()
load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
router = APIRouter()
#Spotify App Credentials-pasted from Spotify Developer Dashboard
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
SPOTIFY_SCOPE ='playlist-modify-private playlist-modify-public user-library-modify'
app.include_router(router)


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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
async def get_access_token(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="No access token provided")
    token_info = sp_oauth.get_cached_token()  # Get the token info from the cache
    if not token_info:
        raise HTTPException(status_code=401, detail="No token info found")
    if sp_oauth.is_token_expired(token_info):  # Use sp_oauth instead of sp
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        token = token_info['access_token']
    return token


@app.get("/auth/login")
def login():
    try:
        
        auth_url = sp_oauth.get_authorize_url()
        print(f"Auth URL: {auth_url}")  # Add this line
        print(f"Redirect URI: {SPOTIFY_REDIRECT_URI}")  # Add this line
        response = RedirectResponse(url=auth_url)
        return response
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to initiate authentication")
        
    

@app.get("/auth/callback")
async def callback(request: Request, code: str = Query(...)):
    try:
        
        # Exchange the authorization code for an access token
        token_info = sp_oauth.get_access_token(code, as_dict=True)
        #request.session["access_token"] = token_info['access_token']
        sp_oauth.auth = token_info['access_token']
        #return JSONResponse({"access_token": request.session["access_token"]})
        return JSONResponse(token_info["access_token"])
    except Exception as e:
        print(e)
    

@app.get("/searchSong/{query}")
async def search_song(query: str = Query(...)):
    try:
        sp = spotipy.Spotify(auth_manager=sp_oauth)
        results = sp.search(q='track:'+ query, limit = 1, type='track')
        return results.get('tracks').get('items')[0].get('uri')
    except Exception as e:
        raise HTTPException(e.status_code, detail=str(e))


@app.get("/createPlaylist/{playlist_name}")
async def create_playlist(playlist_name: str = Query(...)):
    try:
        sp = spotipy.Spotify(auth_manager=sp_oauth)
        user_id = sp.current_user()["id"]
        print(f"User ID: {user_id}")
        playlist = sp.user_playlist_create(user_id, playlist_name, public=False)
        return playlist
    except Exception as e:
        raise HTTPException(print("Status code:", e.status_code), detail=str(e))
    

@app.get("/addSongToPlaylist/{playlist_id}/{song_uri}")
def addSongToPlaylist(playlist_id: str = Query(...), song_uri: str = Query(...)):
    try:
        sp = spotipy.Spotify(auth_manager = sp_oauth)
        sp.playlist_add_items(playlist_id,  [song_uri])
        return {"message": "Song added to playlist"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

