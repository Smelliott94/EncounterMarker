import requests
import dotenv
import os

# Your Twitch API client ID
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
# The Twitch username (channel name) for which you want to obtain the user_id
username = "creepin_wow"  # Replace with the channel's username

# Construct the URL for the "Get Users" endpoint
url = f"https://api.twitch.tv/helix/users?login={username}"

# Set up the headers with your client ID and OAuth token if required
headers = {
    "Client-ID": TWITCH_CLIENT_ID,
}

# Make the GET request to obtain the user_id
response = requests.get(url, headers=headers)

# Parse the response JSON to extract the user_id
data = response.json()
if "data" in data and len(data["data"]) > 0:
    user_id = data["data"][0]["id"]
    print(f"User ID for {username}: {user_id}")
else:
    print(f"User not found: {username}")
    print(response.text)