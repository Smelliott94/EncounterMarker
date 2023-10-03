import time
import requests
from pathlib import Path
import logging
import os
from utils.combatlog import parse_log_line
from utils.twitch import request_stream_marker, request_chat_announcement
import utils.setup_logging
import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_USER_ID = os.getenv("TWITCH_USER_ID")
TWITCH_ACCESS_TOKEN = os.getenv("TWITCH_ACCESS_TOKEN")
WOW_ROOT_DIR = os.getenv("WOW_ROOT_DIR", "C:\Program Files (x86)\World of Warcraft\_retail_")

logger = logging.getLogger()

# Function to check if specific text is present in the log file
def check_log_for_text(log_file, target_text):
    
    for line in log_file:
        for word in target_text:
            if word in line:
                return line
    return False

# Function to get the most recent file
def get_most_recent_file(directory, file_prefix):
    try:
        # List all files in the directory
        files = [file for file in directory.iterdir() if file.name.startswith(file_prefix)]
        
        # Sort the matching files by modification time (most recent first)
        files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        if files:
            most_recent_file = files[0]
            return most_recent_file
        else:
            return None
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
        return None
wow_root_dir = Path(WOW_ROOT_DIR)
log_dir = wow_root_dir / "Logs"
log_file_prefix = "WoWCombatLog"

target_text = [
    "CHALLENGE_MODE_START",
    "CHALLENGE_MODE_END"
] 

# Open the log file in read mode with buffering set to 1
while True:
    # Main loop, checks for newest file
    log_file = get_most_recent_file(log_dir, log_file_prefix)
    logger.info(f'Polling {log_file}')

    # Line-buffer the log file and continue where you left off after sleeping
    try:
        with open(log_file, 'r', buffering=1, encoding="utf-8") as log_file:
            log_file.seek(0, 2) # Start from the end of the file
            while True:
                matched_line = check_log_for_text(log_file, target_text)
                if matched_line:
                    log_data = parse_log_line(matched_line)
                    logger.warning(log_data)
                    if log_data['report']:
                        marker_description = request_stream_marker(
                            TWITCH_CLIENT_ID,
                            TWITCH_USER_ID,
                            TWITCH_ACCESS_TOKEN,
                            log_data
                        )
                
                time.sleep(1)
                new_log_file = get_most_recent_file(log_dir, log_file_prefix)
                if log_file.name != str(new_log_file):
                    logger.warning("More recently modified log file detected")
                    break
    except PermissionError as e:
        # Likely tried to open the file as it was being created
        logging.error(e)
        time.sleep(1)
