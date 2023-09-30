# EncounterMarker
Creates twitch markers when you enter an encounter or Mythic+ dungeon. Currently only Mythic+ dungeons are supported.
Raid encounters TBD.

## Setup
1. Register an application at https://dev.twitch.tv/console/apps (2FA required)
1. Set an oauth Redirect URL to http://localhost:8080/
1. create a `.env` file in the project root folder with the following constants
```bash
TWITCH_CLIENT_ID=your_client_id
TWITCH_CLIENT_SECRET=your_client_secret
TWITCH_CHANNEL_NAME=your_channel_name
WOW_ROOT_DIR='C:\Program Files (x86)\World of Warcraft\_retail_' # < Default value, not required if your WoW install is there
```

1. Run `auth.py`. You'll be directed to allow your app in your web browser. If successful, an access token should now be saved in `.env`
2. Run `main.py` (recommended from a terminal to see logged actions, exit eith CTRL+C)
