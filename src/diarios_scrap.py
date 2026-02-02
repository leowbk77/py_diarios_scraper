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

def init():
    Logs.log(f"Tentando Iniciar database: {arg.cidade}")
    if database.db_exists(f"{arg.cidade}"):
        Logs.log("Database Encontrado - pulando etapa de criacao")
    else:
        Logs.log("Database nao iniciado.")
        Logs.log(f"Subindo db ./data/{arg.cidade}.db")
        db = database.init(f"data/{arg.cidade}.db")
        Logs.log('Criando tabelas')
        database.create_tbl_docs(db)
        database.create_tbl_docs_fts(db)
        db.close()
        Logs.log("Database criado e populado.")

def download():
    if arg.ano and arg.mes:
        if Args.ano_mes_valid(arg.ano[0], arg.mes[0]):
            if arg.cidade == Args.UDI:
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