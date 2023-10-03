# EncounterMarker
Creates a [Twitch stream marker](https://dev.twitch.tv/docs/api/markers/) when you enter an encounter or Mythic+ dungeon to make your life a bit easier when creating highlights.
Currently only Mythic+ dungeons are supported.
Raid encounters TBD.

**Note:** You'll have to register your own application with Twitch since the program polls the log file on your local computer.

* [Combat log docs](https://wowpedia.fandom.com/wiki/COMBAT_LOG_EVENT)

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
1. `git clone https://github.com/Smelliott94/EncounterMarker.git`
1. Go to the project root directory (`EncounterMarker`) in your terminal
1. Download dependencies : `python -m pip install -r requirements.txt`
2. (Windows) Run `install.py` which should create `encounterMarker.bat`, a batch script that simply executes `auth.py` and `main.py` in sequence and leaves the terminal open so you can see when logs/encounters are found.

## Usage
1. Run `encounterMarker.bat`, making sure to authorize your app on the first run.

> `encounterMarker.bat` Should find the absolute paths to the scripts, so you can move it anywhere you'd like. Note you'll have to re-generate the script if you move the project folder.
