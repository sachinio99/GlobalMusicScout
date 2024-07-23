import requests
import json
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored  
import os
from main import sp_oauth



GPT_MODEL = "gpt-4"
# Set your OpenAI API key from the environment variable
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)
print(os.getenv("OPENAI_API_KEY"))
#This is the file that will define the flow for the agent that can return a list of songs and then return the URIs of the song that can be added to the playlist
ngrok_url = "https://807a-207-38-131-18.ngrok-free.app/"
#Set up the session storage for the auth token
session = requests.Session()


def search_song(song_name: str):
    url = ngrok_url + "/searchSong/" + song_name
    response = requests.get(url)
    return response.json().get('uri')

def login():
    url = ngrok_url + "/auth/login"
    response = requests.get(url)

    session.post(url,response.json().access_token)
    return response.json().access_token


def create_playlist(playlist_name: str, access_token: str):
    url = ngrok_url + "/createPlaylist/" + playlist_name
    response = requests.get(url, headers={"Authorization": f"Bearer {session.get(ngrok_url + '/auth/login').access_token}"})
    return response.json().get('id')


custom_functions = [
    {
        'name': 'login',
        'description': 'Redirect the user to the Spotify authorization URL for authentication',
        'parameters': {}
    },
    {
        'name': 'callback',
        'description': 'Handle the callback from Spotify after successful authentication',
        'parameters': {
            'type': 'object',
            'properties': {
                'code': {
                    'type': 'string',
                    'description': 'The authorization code provided by Spotify'
                }
            }
        }
    },
    {
        'name': 'search_song',
        'description': 'Search for a song on Spotify',
        'parameters': {
            'type': 'object',
            'properties': {
                'query': {
                    'type': 'string',
                    'description': 'The search query for the song'
                },
                format:{
                    "type":"string",
                    "enum":["song_uri"],
                    "description":"The song uri for the given song name"

                }
            }
        }
    },
    {
        'name': 'create_playlist',
        'description': 'Create a new playlist on the users Spotify account',
        'parameters': {
            'type': 'object',
            'properties': {
                'playlist_name': {
                    'type': 'string',
                    'description': 'The name of the new playlist'
                },
                'access_token':{
                    'type':'string',
                    'description':'The access token for the user'
                }
            }
        }
    },
    {
        'name': 'addSongToPlaylist',
        'description': 'Add a song to a playlist on the user\'s Spotify account',
        'parameters': {
            'type': 'object',
            'properties': {
                'playlist_id': {
                    'type': 'string',
                    'description': 'The ID of the playlist to add the song to'
                },
                'song_uri': {
                    'type': 'string',
                    'description': 'The Spotify URI of the song to add'
                }
            }
        }
    },
    {
        'name': 'parseOutputForSongList',
        'description': 'parse the json output from the model for names of songs',
        'parameters': {
            'type': 'object',
            'properties': {
                'location': {
                    'type': 'string',
                    'description': 'location of user'
                
            }
        }
    }
    }
]