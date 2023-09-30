import time
import requests
from pathlib import Path
import logging
from utils.combatlog import parse_log_line

# Define ANSI escape codes for colors
COLORS = {
    'DEBUG': '\033[94m',  # Blue
    'INFO': '\033[92m',   # Green
    'WARNING': '\033[93m',  # Yellow
    'ERROR': '\033[91m',   # Red
    'CRITICAL': '\033[91m\033[1m'  # Red and bold
}

RESET = '\033[0m'  # Reset color

# Create a custom formatter with color for the timestamp
class ColoredTimestampFormatter(logging.Formatter):
    def format(self, record):
        log_level = record.levelname
        color = COLORS.get(log_level, '')
        message = super(ColoredTimestampFormatter, self).format(record)
        timestamp = f"{color}{record.asctime}{RESET}"
        return message.replace(record.asctime, timestamp)

logger = logging.getLogger()
# Create a StreamHandler to display logs in the terminal
console_handler = logging.StreamHandler()

# Set the formatter for the console handler
console_formatter = ColoredTimestampFormatter("%(asctime)s %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(console_formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)

# Set the log level
logger.setLevel(logging.INFO) 

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


# Function to make an HTTP request
def make_http_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("HTTP request successful")
        else:
            print(f"HTTP request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")


wow_root_dir = Path("C:\Program Files (x86)\World of Warcraft\_retail_")
log_dir = wow_root_dir / "Logs"  # Replace with the actual path to your log file
log_file_prefix = "WoWCombatLog"

target_text = [
    "CHALLENGE_MODE_START",
    "CHALLENGE_MODE_END"
] 
url_to_request = "http://example.com"  # Replace with the URL you want to request

# Open the log file in read mode with buffering set to 1
while True:
    # Main loop, checks for newest file
    log_file = get_most_recent_file(log_dir, log_file_prefix)
    logger.info(f'Polling {log_file}')

    # Line-buffer the log file and continue where you left off after sleeping
    try:
        with open(log_file, 'r', buffering=1, encoding="utf-8") as log_file:
            # log_file.seek(0, 2) # Start from the end of the file
            while True:
                matched_line = check_log_for_text(log_file, target_text)
                if matched_line:
                    data = parse_log_line(matched_line)
                    logger.warning(data)
                    make_http_request(url_to_request)
                
                time.sleep(5)
                new_log_file = get_most_recent_file(log_dir, log_file_prefix)
                if log_file.name != str(new_log_file):
                    logger.warning("More recently modified log file detected")
                    break
    except PermissionError as e:
        logging.error(e)
        time.sleep(1)
