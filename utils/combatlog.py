import re
import math
import utils.affixes
import csv
from pathlib import Path
import utils.setup_logging
import logging
import time

logger = logging.getLogger()

def format_timer(time_in_ms):
    time_in_s = time_in_ms / 1000
    time_in_mins = time_in_s / 60
    return f'{math.floor(time_in_mins)}:{math.floor(time_in_s % 60)}'

def form_marker_description(data):
    zone = data.get('zone_name', '')
    key_level = data.get('key_level', '')
    success = data.get('success', '')
    player_score  = data.get('player_score', '')
    timer = data.get('timer', '')
    affix_ids = data.get('affix_ids', '')
    boss = data.get('encounter_name', '')
    difficulty = data.get('difficulty', '')
    
    # Key finish
    if timer and isinstance(success, int) and player_score:
        formatted_timer = format_timer(timer)
        timed_or_depleted = 'timed' if success == 1 else 'depleted'
        return f'Key end | {timed_or_depleted} {formatted_timer} | {player_score}io'
    
    # Key start
    if zone:
        affixes = utils.affixes.get_affixes(affix_ids)
        return f'{zone} {key_level} | {affixes}'
    
    # Boss end
    if boss and difficulty:
        formatted_timer = format_timer(timer)
        kill_or_wipe = 'kill' if success == 1 else 'wipe'
        desc = f'{time.strftime("%H:%M")} | {difficulty} {boss} | {kill_or_wipe}'
        return desc

def get_encounter_name(encounter_id):

    try:
        csv_path = Path(__file__).resolve().parent.parent / "data" / "DungeonEncounter.csv"
        with open(csv_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                if row and len(row) > 1 and int(row[1]) == encounter_id:
                    match = row[0]
                    break
            return match
    except FileNotFoundError:
        logger.error(f"Encounter data csv missing {csv_path}")
        return "Boss"
    except Exception as e:
        logger.error(f"Error: {e}")
        return "Boss"

def parse_log_line(log_line):
    if 'CHALLENGE_MODE_START' in log_line:
        # zoneName, instanceID, challengeModeID, keystoneLevel, [affixID, ...]
        log_line = log_line.replace('"', '')
        dungeon_details =  log_line.split(',')[1:-3]
        affix_ids_pattern = r'\[([\d,]+)\]'
        match = re.search(affix_ids_pattern, log_line)
        matched_text = match.group(1)
        affix_ids = matched_text = [int(i) for i in matched_text.split(',')]
        return {
            'type': 'CHALLENGE_MODE_START',
            'zone_name': dungeon_details[0],
            'instance_id': int(dungeon_details[1]),
            'affix_ids': affix_ids,
            'key_level': int(dungeon_details[3]),
            'report': True
        }
    if 'CHALLENGE_MODE_END' in log_line:
        # instanceID, success, keystoneLevel, totalTime, keyScore, playerScore
        dungeon_details = log_line.split(',')[1:]
        timer = int(dungeon_details[3])
        if not timer:
            return {
                'type': 'CHALLENGE_MODE_END',
                'report': False
            }

        return {
            'type': 'CHALLENGE_MODE_END',
            'instance_id': int(dungeon_details[0]),
            'success': int(dungeon_details[1]),
            'key_level': int(dungeon_details[2]),
            'timer': timer,
            'key_score': float(dungeon_details[4]),
            'player_score': round(float(dungeon_details[5])),
            'report': True
        }
    
    if 'ENCOUNTER_END' in log_line:
        # ENCOUNTER_END: 0 encounterID, 1 encounterName, 2 difficultyID, 3 groupSize, 4 success, 5 fightTime
        # https://wowpedia.fandom.com/wiki/DifficultyID
        raid_diff_map = {14: 'Normal', 15: 'Heroic', 16: 'Mythic'}
        log_line = log_line.replace('"', '')
        log_line = log_line.replace('\n', '')
        encounter_details = log_line.split(',')
        # Names might have a comma which messes up splitting. Ignore Name and look up by encounter ID from csv instead
        # 1 encounterID, 2 difficultyID, 3 groupSize, 4 success, 5 fightTime
        encounter_details = [encounter_details[1], *encounter_details[-4:]]
        encounter_name = get_encounter_name(int(encounter_details[0]))
        timer = int(encounter_details[-1])

        # Ignore fights shorter than 10s (10k ms)
        if timer < 10000 and not encounter_details[3]:
            return {
                'type': 'ENCOUNTER_END',
                'report': False
            }
        
        return {
            'type': 'ENCOUNTER_END',
            'encounter_id': int(encounter_details[0]),
            'encounter_name': encounter_name,
            'difficulty': raid_diff_map[int(encounter_details[1])],
            'success': int(encounter_details[3]),
            'timer': timer,
            'report': True
        }



