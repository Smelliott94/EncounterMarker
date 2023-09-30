import requests
import logging
import math
import utils.affixes

logger = logging.getLogger()

def _format_timer(time_in_ms):
    time_in_s = time_in_ms / 1000
    time_in_mins = time_in_s / 60
    return f'{math.floor(time_in_mins)}:{math.floor(time_in_s % 60)}'

def _form_marker_description(data):
    zone = data.get('zone_name', '')
    key_level = data.get('key_level', '')
    success = data.get('success', '')
    player_score  = data.get('player_score', '')
    timer = data.get('timer', '')
    affix_ids = data.get('affix_ids', '')
    
    if timer and isinstance(success, int):
        formatted_timer = _format_timer(timer)
        timed_or_depleted = 'timed' if success == 1 else 'depleted'
        return f'Key end | {timed_or_depleted} {formatted_timer} | {player_score}io'
    
    if zone:
        affixes = utils.affixes.get_affixes(affix_ids)
        return f'{zone} {key_level} | {affixes}'

def request_stream_marker(client_id, channel_id, access_token, log_data, dry_run=False):
    # Construct the POST request headers
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Define the data for setting the stream marker
    data = {
        "user_id": channel_id,
        "description": _form_marker_description(log_data)  # Optional: You can provide a description for the marker
    }
    if not dry_run:
        # Make the POST request to set the stream marker
        marker_url = "https://api.twitch.tv/helix/streams/markers"
        response = requests.post(marker_url, headers=headers, json=data)

        # Check the response
        if response.status_code == 200:
            logger.info("Stream marker set successfully.")
            response_data = response.json()
            logger.info(f"Marker ID: {response_data['data']['id']}")
        else:
            logger.info(f"Failed to set stream marker. Status code: {response.status_code}")
            logger.info(response.text)
    else:
        logging.warning('DRY RUN MODE')
        logging.warning(data)
