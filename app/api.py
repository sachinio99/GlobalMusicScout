from fastapi import FastAPI, Depends, HTTPException, status,Query, Request
from fastapi.responses import JSONResponse, RedirectResponse
import os 
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from urllib.parse import urlencode
import logging


app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#Spotify App Credentials-pasted from Spotify Developer Dashboard
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "http://localhost:8000/auth/callback"
SPOTIFY_SCOPE = "playlist-modify-private playlist-modify-public"
TOKEN_INFO = None

# OAuth2 Details
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

# Initialize Spotify OAuth2 object
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SPOTIFY_SCOPE
)
"""
@app.get("/auth/login")
def login():
    try:
        query_params = {
            "response_type": "code",
            "client_id": SPOTIFY_CLIENT_ID,
            "scope": SPOTIFY_SCOPE,
            "redirect_uri": SPOTIFY_REDIRECT_URI
        }
        url = f"{AUTH_URL}?{urlencode(query_params)}"
        
        return url
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
"""@app.get("/auth/callback")
def callback(code: str = Query(...), state: str = Query(...)):
    try:
        # Exchange code for a token
        data = {
            "grant_type": "authorization_code",
            "code": code,  
            "redirect_uri": SPOTIFY_REDIRECT_URI,
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET
        }
        logger.info(f"Code: {code}")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        logger.info(f"Code: {code}")
        response = requests.post(TOKEN_URL, data=data, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad requests
        TOKEN_INFO = response.json()
        return response.json() # Returns token info as JSON
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

"""

@app.get("/auth/login")
def login():
    try:
        auth_url = sp_oauth.get_authorize_url()
        response = RedirectResponse(url=auth_url)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/auth/callback")
async def callback(request: Request, code: str = Query(...)):
    try:
        # Exchange the authorization code for an access token
        token_info = sp_oauth.get_access_token(code, as_dict=True)
        access_token = token_info["access_token"]
        return JSONResponse({"access_token": access_token})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

#@app.get("search/{query}")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
