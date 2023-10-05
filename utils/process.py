import win32process
import win32api
import win32con
import win32gui
import ctypes
import os

def getWowProcessPath(wowWindow):
    _, pid = win32process.GetWindowThreadProcessId(wowWindow)
    handle = ctypes.windll.kernel32.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)
    if handle == 0:
        raise Exception("Failed to query wow process (is it open?)")
    
    path = ctypes.create_unicode_buffer(win32con.MAX_PATH)
    if ctypes.windll.psapi.GetModuleFileNameExW(handle, 0, path, win32con.MAX_PATH) == 0:
        raise Exception("Failed to get World of Warcraft process path!")
    
    win32api.CloseHandle(handle)
    return os.path.dirname(path.value)

# Using the wow base path, get the log folder location
def getLogFolderLocation(wowWindow, wow_base = ""):
    if wow_base == "":
        wowProcessPath = getWowProcessPath(wowWindow)
        logFolderLocation = os.path.join(wowProcessPath, "Logs")
    else:
        logFolderLocation = wow_base + "\\Logs"
        logFolderLocation = logFolderLocation.replace('/', '\\')
        if not logFolderLocation.endswith('\\'):
            logFolderLocation += '\\'
    return logFolderLocation

# Ported this function even though one already exists in entry point
def getMostRecentLogFile(logFolderLocation):
    files = os.listdir(logFolderLocation)
    files = [f for f in files if f.startswith("WoWCombatLog") and f.endswith(".txt")]
    if len(files) == 0:
        raise Exception("Failed to find WoWCombatLog*.txt file!")
    mostRecentLogFile = max(files, key=lambda f: os.path.getmtime(os.path.join(logFolderLocation, f)))
    return mostRecentLogFile

# Get the log folder location and the most recent log file in one go
def getLogFileLocation(wowWindow):
    logFolderLocation = getLogFolderLocation(wowWindow)
    logFileName = getMostRecentLogFile(logFolderLocation)
    return os.path.join(logFolderLocation, logFileName)

def getWowWindow():
    wowWindow = win32gui.FindWindow(None, "World of Warcraft")
    if wowWindow == 0:
        raise Exception("Failed to find World of Warcraft window!")
    return wowWindow