'''
lmf

config.py

Módulo que fornece as configurações do scraper
'''

import configparser
from pathlib import Path

settings = configparser.ConfigParser()
configPath = Path.cwd()

if configPath.name == 'utils':
    configPath = './../config.ini'
else:
    configPath = configPath / "config.ini"

settings.read(configPath)

'''
função que retorna as cidades disponíveis.
'''
def getParserCidades():
    cidades = settings['parser.cidades']
    retorno = []
    for key in cidades:
        retorno.append(cidades.get(key))
    return retorno

'''
função que lista (print) as cidades disponíveis.
'''
def listParserCidades():
    cidades = settings['parser.cidades']
    for key in cidades:
        print(f"{key}\t{cidades[key]}")

'''
função que retorna o menor ano possível para a realização da busca de documentos
para a indexação.
'''
def getParserAnoMinimo():
    parser = settings['parser']
    menorAno = parser.getint('MenorAno')
    return menorAno

'''
função que retorna o caminho configurado para o diretório de logs.
'''
def getLogsPath():
    logsSettings = settings['logs']
    return logsSettings.get('Path')

'''
função que retorna o caminho configurado para o diretório de downloads dos doumentos
baixados para a indexação.
'''
def getDownloadPath():
    dataSettings = settings['data']
    return dataSettings.get('DownloadsDir')

'''
função que retorna o caminho configurado para o diretório dos arquivos sqlite de base de
dados indexados
'''
def getDataBasePath():
    dataSettings = settings['data']
    return dataSettings.get('DataBaseDir')
