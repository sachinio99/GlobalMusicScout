
# Global Music Scout

**Global Music Scout** is an AI Agent that helps curate playlists based on your current location.

## Installation

After cloning the repository, follow the steps below to:

1. Start the Fast API locally
2. Install and launch ngrok to expose the API to the AI Agent
3. Run the agent file that will connect to your Spotify and create a customized playlist of new, underground music

### Prerequisites

Make sure you have **uvicorn** installed locally:

```sh
pip install "uvicorn[standard]"
```

### Step-by-Step Instructions

#### 1. Install Repository Dependencies

```sh
pip install -r requirements.txt
```

#### 2. Install FastAPI

```sh
pip install fastapi
```

#### 3. Start the FastAPI Server

The default URL it will run on is `http://localhost:8000`.

```sh
cd app
uvicorn main:app --reload
```

#### 4. Install ngrok

After creating an account [here](https://ngrok.com/docs/getting-started/), install ngrok:

```sh
brew install --cask ngrok
```

#### 5. Configure ngrok Auth Token

You can find your auth token on the ngrok dashboard:

```sh
ngrok config add-authtoken <<your_auth_token_here>>
```

#### 6. Run ngrok on the Correct Port

```sh
ngrok http http://localhost:8000
```

### Agent Code

**Coming Soon**
