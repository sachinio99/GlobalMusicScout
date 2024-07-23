import requests
import json
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored  
import os
from main import sp_oauth
import click

@click.group()
def main():
    pass    


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

user_location = ""

@main.command()
@click.option("--location", prompt="Enter your location- be as specific as possible", type=(str))
@click.option("--genre", prompt="Enter your preferred genre", type=(str))
def get_user_location_genre(location, genre):
    #print(f"Your location is {location}")
    #session.post("localhost:8000" + "/userLocation", json={"location":location})
    print("Location saved successfully...generating your playlist...")
    user_location = location
    print(run_conversation(location,genre))
    return location

prompt = "Generate a playlist of songs of underground artists that are popular in your location An underground artist is defined as having under 40k monthly listeners on Spotify Make sure to include a variety of genres, limit it to 15 songs and output the list in a JSON format that includes the song name and artist name in each entry. The location  of the user is "

def search_song(song_name: str):
    url = ngrok_url + "/searchSong/" + song_name
    response = requests.get(url)
    return response.json().get('uri')

def login():
    url = ngrok_url + "/auth/login"
    response = requests.get(url)
    session.post(url,response.json().access_token)
    return response.json().access_token


def create_playlist(playlist_name: str):
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
    },
    {
        'name': 'get_user_location',
        'description': 'Get the location of the user',
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

functions = [
    {
        "type": "function",
        "function": {
            'name': 'login',
            'description': 'Redirect the user to the Spotify authorization URL for authentication',
            'parameters': {}
        }
    }
]
def run_conversation(location: str, genre_pref: str):
    messages = [{"role":"user", 
                "content": prompt + " " + location + "." + "My preferred genre that this playlist should focus on is " + genre_pref + "."
                }]
    

    response = client.chat.completions.create(model = GPT_MODEL, messages = messages, tools = functions, tool_choice="auto")

    first_response = response.choices[0].message
    print(first_response)
    needs_function = first_response.message.tool_calls
    if needs_function:
        print("needs to use a function we passed in")

if __name__ == "__main__":
    main()


print(run_conversation(user_location))