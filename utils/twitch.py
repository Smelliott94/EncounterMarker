import requests
import logging
import math
import utils.affixes
import json

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

def request_stream_marker(client_id, user_id, access_token, log_data, dry_run=False):
    # Construct the POST request headers
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Define the data for setting the stream marker
    description = _form_marker_description(log_data)
    data = {
        "user_id": user_id,
        "description": description  # Optional: You can provide a description for the marker
    }
    if not dry_run:
        # Make the POST request to set the stream marker
        marker_url = "https://api.twitch.tv/helix/streams/markers"
        logging.critical(json.dumps(headers))
        logging.critical(json.dumps(data))
        response = requests.post(marker_url, headers=headers, json=data)

        # Check the response
        if response.status_code == 200:
            logger.info("Stream marker set successfully.")
            response_data = response.json()
            logger.info(f"Marker ID: {json.dumps(response_data)}")
            return description
        else:
            logger.info(f"Failed to set stream marker. Status code: {response.status_code}")
            logger.info(response.text)
    else:
        logging.warning('DRY RUN MODE')
        logging.warning(data)

def request_chat_announcement(client_id, user_id, access_token, message):
    # Construct the POST request headers
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    params = {
        'broadcaster_id': user_id,
        'moderator_id': user_id
    }
    data = {
        'message': message
    }
    url = "https://api.twitch.tv/helix/chat/announcements"
    response = requests.post(url, headers=headers, json=data, params=params)

    # Check the response
    if response.status_code == 204:
        logger.info("Announcement sent successfully.")
        logger.info(response.text)
    else:
        logger.info(f"Failed to send Announcement. Status code: {response.status_code}")
        logger.info(response.text)


