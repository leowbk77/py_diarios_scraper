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
    Logs.log(f"Subindo db ./data/{args.cidade}.db")
    db = database.init(f"data/{args.cidade}.db")
    Logs.log('Criando tabelas')
    database.create_tbl_docs(db)
    database.create_tbl_docs_fts(db)
    db.close()
elif args.download:
    #faltando implementação
    if args.ano and args.mes:
        link = Udia.fluxo_download(args.ano[0], args.mes[0])
        
        #links = ['https://docs.uberlandia.mg.gov.br/wp-content/uploads/2025/12/7264.pdf', 'https://docs.uberlandia.mg.gov.br/wp-content/uploads/2026/01/7265.pdf']
        #Logs.log(f"Teste de download de 2 docs: {links}")
        #Udia.download_and_index_pdfs(links)
    else:
        Logs.log('Erro: faltando argumento em tentativa de download')