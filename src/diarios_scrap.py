'''
lmf

diarios_scrap.py

Módulo principal do scraper
'''
import scrapers.udia as Udia
from data import database
from utils import logger as Logs, scraper_parser as Args

arg = Args.parser.parse_args()
Logs.init_log()

def obter_cidade(argCidade: str | list[str]):
    if argCidade == Args.UDI:
        return argCidade
    else: 
        return argCidade[0]

def init():
    cidade = obter_cidade(arg.cidade)
    Logs.log(f"Tentando Iniciar database: {cidade}")
    if database.db_exists(f"{cidade}"):
        Logs.log("Database Encontrado - pulando etapa de criacao")
    else:
        Logs.log("Database nao encontrado.")
        Logs.log(f"Subindo db ./data/{cidade}.db")
        db = database.init(f"data/{cidade}.db")
        Logs.log('Criando tabelas')
        database.create_tbl_docs(db)
        database.create_tbl_docs_fts(db)
        db.close()
        Logs.log("Database criado e populado.")

def download():
    if arg.ano and arg.mes:
        if Args.ano_mes_valid(arg.ano[0], arg.mes[0]):
            cidade = obter_cidade(arg.cidade)
            if cidade == Args.UDI :
                Udia.fluxo_download(arg.ano[0], arg.mes[0])
            else:
                #faltando implementacao de outras cidades
                Logs.log(f"Erro: Cidade não implementada - {arg.cidade}")
        else:
            Logs.log("Erro - ano/mes invalido")
    else:
        Logs.log("Erro no download: Faltando argumentos ano/mes")

'''
    Fluxo de execução principal
'''
if arg.listc:
    Args.list_cidades()
else:
    if arg.init:
        init()
    if arg.download:
        download()