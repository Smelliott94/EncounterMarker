# EncounterMarker
Creates a [Twitch stream marker](https://dev.twitch.tv/docs/api/markers/) when you enter an encounter or Mythic+ dungeon to make your life a bit easier when creating highlights.
Currently only Mythic+ dungeons are supported.
Raid encounters TBD.

Note: You'll have to register your own application since the program polls the log file on your local computer.

## Setup
1. Register an application at https://dev.twitch.tv/console/apps (2FA required)
1. On the Manage Application page. Set an oauth Redirect URL to http://localhost:8080/. Note the Client ID and Client Secret.
1. create a `.env` file in the project root folder with the following constants
```bash
TWITCH_CLIENT_ID=your_client_id
TWITCH_CLIENT_SECRET=your_client_secret
TWITCH_USER_ID=your_user_id # A number corresponding to your twitch channel. Can be found using the twitch API or a website like https://streamscharts.com/tools/convert-username
WOW_ROOT_DIR='C:\Program Files (x86)\World of Warcraft\_retail_' # < Default value, not required if your WoW install is there
```
1. Download dependencies : `python -m pip install -r requirements.txt`
1. Run `auth.py`. You'll be directed to allow your app in your web browser. If successful, an access token should now be saved in `.env`

## Usage
1. Run `python ./main.py` (recommended from a terminal to see logged actions, exit with CTRL+C)
