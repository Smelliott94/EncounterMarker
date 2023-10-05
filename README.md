# EncounterMarker
Creates a [Twitch stream marker](https://dev.twitch.tv/docs/api/markers/) when you enter an encounter or Mythic+ dungeon to make your life a bit easier when creating highlights.
Currently only Mythic+ dungeons are supported.
Raid encounters TBD.

**Note:** You'll have to register your own application with Twitch since the program polls the log file on your local computer.

* [Combat log docs](https://wowpedia.fandom.com/wiki/COMBAT_LOG_EVENT)

## Setup
1. [Allow the application on Twitch](https://id.twitch.tv/oauth2/authorize?client_id=8188onbz5c834x47p07lfopa4kp0uv&redirect_uri=https://encountermarkerserver.onrender.com/auth&response_type=code&scope=user:edit:broadcast)
1. Note the private client code (this is used to ensure you only make stream markers for yourself)
1. Clone this repository: `git clone https://github.com/Smelliott94/EncounterMarker.git`
1. Go to the project root directory (`EncounterMarker`) in your terminal
   1. If your wow directory isn't `"C:\Program Files (x86)\World of Warcraft\_retail_"`, override `WOW_ROOT_DIR` in the `.env` file
2. Download dependencies : `python -m pip install -r requirements.txt` built and tested on Python 3.8.3

## Usage
1. Run `python .\encounterMarker.py`, and enter the private client code when prompted. This will be saved for future use.
   1. If you want to authenticate another twitch account. clear the contents of `.env`, allow the application for the new account, and use the new code when provided.
