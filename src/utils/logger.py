'''
lmf
simple_logger.py
Logger para o scraper
'''
from datetime import datetime, date

LOGS_PATH = './logs/'
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

'''
class Logger:

    def __init__(self, path: str):
        self.PATH = path
        self.DATA = date.today().strftime("%d%m%Y")
        self.LOGS_FILENAME = "log-scrap-" + self.LOGS_DATA + '.txt'
        try:
            self.logFile = open()
        except :
'''