import requests
import json
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored  
import os

GPT_MODEL = "gpt-4"
# Set your OpenAI API key from the environment variable
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)
#This is the file that will define the flow for the agent that can return a list of songs and then return the URIs of the song that can be added to the playlist
ngrok_url = "https://807a-207-38-131-18.ngrok-free.app/"

#Define helper function to call api to search for a song
def search_song(song_name: str):
    url = ngrok_url + "/searchSong/" + song_name
    response = requests.get(url)
    return response.json().get('uri')





#utility function to make a call to chat completions api, keeps track of conversation state 
#For this specific case - When the api returns a list of songs, keep track of that and then return the URIs of each song in a JSON format
@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=custom_functions,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e.status_code}")
        return e
    
def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }
    
    #This is just a utility function ignore in the future
    for message in messages:
        if message["role"] == "system":
            print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "user":
            print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "function":
            print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))

messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what song to search for or what functions to use. Make sure to use the songs in the list returned based on the user's location"})
messages.append({"role": "system", "content": "If the location is missing, make sure to prompt the user for their current location and then use that in your search. Thanks! "})
messages.append({"role": "user", "content": "Make me a playlist of underground songs from several different genres based on my location. "})
chat_response = chat_completion_request(
    messages, tools = custom_functions,tool_choice={"type": "function", "function": {"name": "parseOutputForSongList"}} #We are setting the tools list in the completion request function call 
)

assistant_message = chat_response.choices[0].message
messages.append(assistant_message)
pretty_print_conversation(messages)



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
        'description': 'Create a new playlist on the user\'s Spotify account',
        'parameters': {
            'type': 'object',
            'properties': {
                'playlist_name': {
                    'type': 'string',
                    'description': 'The name of the new playlist'
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