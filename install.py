from pathlib import Path
import sys

PYTHON = Path(sys.executable)
AUTH_ABS = Path('./auth.py').resolve()
MAIN_ABS = Path('./main.py').resolve()

with open('encounterMarker.bat', 'w') as file:
    file.write(f'{PYTHON} {AUTH_ABS}\n')
    file.write(f'{PYTHON} {MAIN_ABS}\n')
    file.write('pause')