from pathlib import Path 
import argparse 
from openai import OpenAI
import os


model = 'gpt-4'
client = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY")
    
)
def main():
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

messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what song to search for or what functions to use. Make sure to use the songs in the list returned based on the user's location"})
messages.append({"role": "system", "content": "If the location is missing, make sure to prompt the user for their current location and then use that in your search. Thanks! "})
messages.append({"role": "user", "content": "Make me a playlist of underground songs from several different genres based on my location. "})
messages.append({"role": "assistant", "content": "Sure, I'll get right on that. Please provide your location in the following format: '{city},{state}'"})


chat_response = chat_completion_request(
    messages
)
print(chat_response)

if __name__ == "__main__":
    main()