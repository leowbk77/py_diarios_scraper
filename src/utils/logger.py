'''
lmf

logger.py

Logger para o scraper
'''
from datetime import datetime, date
from utils import config as AppConfig

LOGS_PATH = AppConfig.getLogsPath()
LOGS_DATA = date.today().strftime("%d%m%Y")
LOGS_FILENAME = "log-scrap-" + LOGS_DATA + '.log'

def init_log():
    try:
        with open(LOGS_PATH + LOGS_FILENAME, "x", encoding = "utf-8") as logFile:
            logFile.write(f"LogFile initiated at {datetime.now()}\n")
            print('LogFile initiated.')
    except FileExistsError:
        print(f"LogFile: {LOGS_FILENAME} encontrado")
    
def to_file(line: str) -> None:
    with open(LOGS_PATH + LOGS_FILENAME, "a", encoding = "utf-8") as logFile:
        logFile.write(line + '\n')

def log(info: str) -> None:
    logInfo = str(datetime.now()) + " [INF] " + info
    to_file(logInfo)
    print(logInfo)