import requests
import dotenv
import os
import webbrowser
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import utils.setup_logging

logger = logging.getLogger()
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CHANNEL_NAME = os.getenv("TWITCH_CHANNEL_NAME")

# Your Twitch application credentials and redirect URI
redirect_uri = "http://localhost:8080/"

# Construct the authorization URL
auth_url = f"https://id.twitch.tv/oauth2/authorize?client_id={TWITCH_CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code&scope=user:edit:broadcast"

# Open the authorization URL in the default web browser
webbrowser.open(auth_url)

# Capture the authorization code
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        query_dict = urllib.parse.parse_qs(query)

        if "code" in query_dict:
            authorization_code = query_dict["code"][0]
            logger.info(f"Authorization Code: {authorization_code}")
            
            # Construct the POST request data
            data = {
                "client_id": TWITCH_CLIENT_ID,
                "client_secret": TWITCH_CLIENT_SECRET,
                "code": authorization_code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            }
            
            # Make the POST request to exchange the code for an access token
            token_url = "https://id.twitch.tv/oauth2/token"
            response = requests.post(token_url, data=data)
            
            # Parse the response JSON to obtain the access token
            response_data = response.json()
            if "access_token" in response_data:
                access_token = response_data["access_token"]
                os.environ['TWITCH_ACCESS_TOKEN'] = access_token
                
                dotenv.set_key(dotenv_file, "TWITCH_ACCESS_TOKEN", os.environ['TWITCH_ACCESS_TOKEN'])
                logger.info(f"Access Token: {access_token}")
            else:
                logger.info("Failed to obtain an access token.")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Authorization successful. You can close this window.")

# Start the HTTP server to capture the code
server_address = ('', 8080)
httpd = HTTPServer(server_address, MyHandler)
logger.info("Listening on http://localhost:8080...")
httpd.handle_request()
