'''
lmf

diarios_scrap.py

Módulo principal do scraper
'''
import scrapers.udia as Udia
from data import database, indexing as Indx
from utils import logger as Logs, scraper_parser as Args

args = Args.parser.parse_args()
Logs.init_log()

if args.listc:
    Args.list_cidades()
    #Indx.index_file('./downloads/7265.pdf', database.init_database(f'./data/{args.cidade}.db'))
elif args.init:
    if args.ano and args.mes:
        Logs.log(f"Subindo db ./data/{args.cidade}.db")
        db = database.init_database(f"data/{args.cidade}.db")
        Logs.log('Criando tabelas')
        database.create_tbl_docs(db)
        database.create_tbl_docs_fts(db)
        database.create_tbl_last_ano_mes_download(db)
        database.update_last_ano_mes(args.ano[0], args.mes[0], db)
        db.close()
    else:
        Logs.log('Erro: faltando argumento em tentativa de init')
elif args.download:
    #faltando implementação
    if args.ano and args.mes:
        link = Udia.fluxo_download(args.ano[0], args.mes[0])
    else:
        Logs.log('Erro: faltando argumento em tentativa de download')