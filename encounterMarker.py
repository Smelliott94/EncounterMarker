import time
from pathlib import Path
import logging
import os
from utils.combatlog import parse_log_line
import utils.api
import utils.setup_logging
import dotenv
import utils.process

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
WOW_ROOT_DIR = os.getenv("WOW_ROOT_DIR_OVERRIDE", "")
APP_CLIENT_CODE = os.getenv("APP_CLIENT_CODE", "")
TWITCH_USER_ID = os.getenv("TWITCH_USER_ID", "")
logger = logging.getLogger()

wow_window = utils.process.getWowWindow()
log_dir = Path(utils.process.getLogFolderLocation(wow_window, WOW_ROOT_DIR))
log_file = os.path.join(log_dir, utils.process.getMostRecentLogFile(log_dir))

target_text = [
    "CHALLENGE_MODE_START",
    "CHALLENGE_MODE_END"
]

# Function to check if specific text is present in the log file
def check_log_for_text(log_file, target_text):
    for line in log_file:
        for word in target_text:
            if word in line:
                return line
    return False

def validate_user():
    valid_user_id = None
    while not valid_user_id:
        if not APP_CLIENT_CODE:
            client_code = input("Input private client code:")
            # Return a valid user_id or None
            valid_user_id, valid_app_code = utils.api.validate_app_user(client_code)
        else:
            # Re-validate client code if in env
            valid_user_id, valid_app_code = utils.api.validate_app_user(APP_CLIENT_CODE)
        
        if not valid_user_id:
            dotenv.unset_key(dotenv_file, "APP_CLIENT_CODE")
            dotenv.unset_key(dotenv_file, "TWITCH_USER_ID")
            if "APP_CLIENT_CODE" in os.environ:
                os.environ.pop("APP_CLIENT_CODE")
            if "TWITCH_USER_ID" in os.environ:
                os.environ.pop("TWITCH_USER_ID")
            
            response = utils.api.request_auth_link()
            response_data = response.json()
            logger.critical("User could not be validated")
            if response.status_code == 200:
                logger.critical(f"Allow app via: {response_data['twitch_auth_link']} and note private client code")
            else:
                logger.critical("API error")
                logger.critical(response_data)

    os.environ["APP_CLIENT_CODE"] = valid_app_code
    os.environ["TWITCH_USER_ID"] = valid_user_id
    
    dotenv.set_key(dotenv_file, "APP_CLIENT_CODE", valid_app_code)
    dotenv.set_key(dotenv_file, "TWITCH_USER_ID", valid_user_id)
    logger.info(f"User {valid_user_id} validated")

validate_user()
# Open the log file in read mode with buffering set to 1
while True:
    # Main loop, checks for newest file
    log_file = os.path.join(log_dir, utils.process.getMostRecentLogFile(log_dir))
    logger.info(f'Polling {log_file}')
    
    # Line-buffer the log file and continue where you left off after sleeping
    try:
        with open(log_file, 'r', buffering=1, encoding="utf-8") as log_file:
            log_file.seek(0, 2) # Start from the end of the file since we don't care about the past
            while True:
                matched_line = check_log_for_text(log_file, target_text)
                if matched_line:
                    log_data = parse_log_line(matched_line)
                    logger.warning(log_data)
                    if log_data['report']:
                        marker_description = utils.api.request_stream_marker(TWITCH_USER_ID, log_data)
                
                time.sleep(1)
                new_log_file = os.path.join(log_dir, utils.process.getMostRecentLogFile(log_dir))
                if log_file.name != str(new_log_file):
                    logger.warning("More recently modified log file detected")
                    break

    except PermissionError as e:
        # Likely tried to open the file as it was being created
        logging.error(e)
        time.sleep(1)