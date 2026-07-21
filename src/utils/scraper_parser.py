'''
lmf

parser_conf.py

Script de configuração do parser de argumentos do scraper
'''
import argparse
from datetime import date

ANOMIN = 2015
ANOMAX = date.today().year

UDI = 'udi'
MONTE = 'monte'
TESTE = 'teste'
CIDADES = [UDI, MONTE, TESTE]

parser = argparse.ArgumentParser(
                    prog='Diarios Scraper',
                    description='Scraper para os documentos dos diários oficiais')

parser.add_argument('--listc', '-lc', 
                    action='store_true', 
                    help='Lista as cidades disponíveis, default: Uberlândia')

parser.add_argument('--cidade', '-c',  
                    nargs=1,
                    type=str,
                    default=UDI, 
                    choices=CIDADES, 
                    help='Seleciona a cidade')

parser.add_argument('--init', '-i', 
                    action='store_true', 
                    help='Inicia a base de dados com os parametros das flags --ano & --mes & --cidade')

parser.add_argument('--ano', '-a', 
                    nargs=1, 
                    type=int, 
                    help='Flag que identifica o ano de inicialização, precisa ser usada com a --init')

parser.add_argument('--mes', '-m', 
                    nargs=1, 
                    type=int, 
                    help='Flag que identifica o mes de inicialização, precisa ser usada com a --init')

parser.add_argument('--dia', '-d',
                    nargs=1,
                    type=int,
                    help='Flag que identifica o dia do documento a ser indexado, usado com a --local')

parser.add_argument('--download', '-dl', 
                    action='store_true', 
                    help='Flag que indica que deve-se realizar o download dos docs')

parser.add_argument('--local', '-l',
                    action='store_true',
                    help='Flag que indica que deve-se realizar indexação de arquivos locais')

parser.add_argument('--arquivo', '-p',
                    nargs=1,
                    type=str,
                    help='Caminho local do arquivo a ser indexado')

parser.add_argument('--acesso', '-url', 
                    nargs=1, 
                    type=str, 
                    help='Caminho de rede onde o arquivo vai ser acessado pelos leitores')

def list_cidades():
    print("CIDADE\t\tIDENTIFICADOR")
    print("Uberlândia\tudi")

def ano_mes_valid(ano: int, mes: int):
    if ano >= ANOMIN and ano <= ANOMAX:
        if mes > 0  and mes <= 12:
            return True
    return False

def dia_valid(dia: int):
    if dia >= 1 and dia <= 31:
        return True
    return False