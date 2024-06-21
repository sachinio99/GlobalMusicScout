Welcome to Global Music Scout, an AI Agent that helps curate playlists based on where you are in the world

Installation: 

After cloning the repo, follow the steps below to 
1) Start the Fast API Locally
2) Install and launch ngrok to expose the api to the AI Agent
3) run the agent file that will connect to your spotify and create a customized playlist of new, undergound music

Make sure you have uvicorn installed locally

```pip install "uvicorn[standard]"```

Install repo dependencies
```uv pip install -r requirements.txt```

Then install fast api
```pip install fastapi```

Start the Fast API Server: The default url it will run on is localhost:8000

```cd app```
```uvicorn main:app --reload```

Install ngrok after creating an account here: https://ngrok.com/docs/getting-started/
```brew install --cask ngrok```

Make sure to configure your auth token, you can find this on the ngrok dashboard
```ngrok config add-authtoken <<your_auth_token_here>>```

Run ngrok on the correct port
```ngrok http http://localhost:8000```

Agent code coming soon
