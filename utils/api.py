import requests
import logging
import utils.combatlog
import json
import os

logger = logging.getLogger()
API_ROOT = os.getenv("API_ROOT", "https://encountermarkerserver.onrender.com")

def request_stream_marker(user_id, log_data):
    
    # Define the data for setting the stream marker
    description = utils.combatlog.form_marker_description(log_data)
    headers = {"X-Client-Code": os.getenv('APP_CLIENT_CODE')}

    data = {
        "user_id": user_id,
        "description": description  # Optional: You can provide a description for the marker
    }
    
    # Make the POST request to set the stream marker
    marker_url = f"{API_ROOT}/marker"
    logging.critical(json.dumps(data))
    response = requests.post(marker_url, json=data, headers=headers)

    # Check the response
    if response.status_code == 200:
        logger.info("Request success")
        response_data = response.json()
        logger.info(f"Response: {json.dumps(response_data)}")
    else:
        logger.error(f"Failed to set stream marker. Status code: {response.status_code}")
        logger.error(response.text)

def request_auth_link():
    url = f"{API_ROOT}/auth_link"
    response = requests.get(url)
    return response

def validate_app_user(code):
    headers = {'X-Client-Code': code}
    url = F"{API_ROOT}/validate_user"
    valid_user_id = None
    valid_app_code = None
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        logger.critical(e)
        raise e

    if response.status_code == 200:
        response_data = response.json()
        valid_user_id = response_data['valid_user_id']
        valid_app_code = code

    return valid_user_id, valid_app_code