from pathlib import Path 
import argparse 
from openai import OpenAI
import os


model = 'gpt-4'
client = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY")
    
)

parser = argparse.ArgumentParser(description="CLI for getting params for API Call")
parser.add_argument("user_location")
args = parser.parse_args()
print(args.user_location)

def chat_completion_request(messages):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e.status_code}")
        return e

GPT_MODEL = "gpt-4"
# Set your OpenAI API key from the environment variable
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

system_prompt = "Assume the persona of a music curator for a radio station. Your job is to take the location or city that the user provides and source underground songs to add to a playlist. To determine if a song is underground or not, evaluate tracks found through your search based on the following criteria. The artist who made the song should have less than 40,000 followers on social media and popular streaming platforms. The song itself should not be on any major music charts but should be gaining traction in terms of growth in streams. Using this criteria, create a playlist of 15-20 songs, make sure to include multiple genres and ensure that more than 7 unique artists are featured in the playlist.  Also come up with a fun name for the playlist based on the information about the songs inside of it. Integrate user authentication via a fast API to allow interaction with Spotify’s developer API. Authenticate the user, retrieve an access token, and use it to add the generated playlist to the user's Spotify library. Only include songs in the playlist that fit the criteria, and avoid extraneous details or song recommendations outside the requested playlist. Output the playlist in a JSON format"

messages = []
messages.append({"role": "system", "content": system_prompt})
messages.append({"role": "system", "content": "If the location is missing, make sure to prompt the user for their current location and then use that in your search. Thanks! "})
#messages.append({"role": "user", "content": "Make me a playlist of underground songs from several different genres based on my location. Output the list in a JSON readable format "})
messages.append({"role": "user", "content": args.user_location})
messages.append({"role": "assistant", "content": "Sure, I'll get right on that. Please provide your location in the following format: '{city},{state}'"})


chat_response = chat_completion_request(
    messages
)
print(chat_response.choices[0].message.content)
