'''
lmf

diarios_scrap.py

Módulo principal do scraper
'''
import utils.parser_conf as parser_conf
import data.data as data
import scrapers.udia as Udia
import utils.logger as Logs

args = parser_conf.parser.parse_args()
Logs.init_log()

def fluxo_download_from_db():
    print('missing implementation')

def fluxo_download_from_args(ano: int, mes: int):
    # IMPLEMENTACAO INICIAL PARA TESTES
    # transformar os crawlers em uma classe para que
    # possa ser herdada e passada por Parâmertro
    Logs.log('Iniciando fluxo de obtencao dos links dos pdfs')
    try:
        paginaURL = Udia.mount_pagina_url(ano, mes)
        Logs.log(f"Link inicial de pagina obtido: {paginaURL}")
        docsLinks = []
        while(paginaURL is not None):
            pagina = Udia.obter_pagina(paginaURL)
            Logs.log('Pagina obtida, obtendo documentos')
            for documento in Udia.obter_links_dos_documentos(pagina):
                docsLinks.append(documento)
            Logs.log('Documentos obtidos')
            paginaURL = Udia.proxima_pagina(pagina)
            Logs.log(f"Proxima pagina: {str(paginaURL)}")
        # corrigir para não precisar passar manual
        # \/\/\/\/\/\/
        Udia.anoAtual = str(ano)
        Udia.mesAtual = str(mes)
        Logs.log('Documentos obtidos, gerando links de pdf')
        pdfLinks = Udia.obter_link_pdfs_from_list(docsLinks)
    except Exception as ex:
        Logs.log(f"Erro no fluxo: {ex}")
    # download seria feito aqui
    #downloader.download_docs([])
    # retorno temporario
    return docsLinks

if args.listc:
    parser_conf.list_cidades()
elif args.init:
    if args.ano and args.mes:
        db = data.init_database(f"data/{args.cidade}.db")
        data.create_tbl_docs(db)
        data.create_tbl_docs_fts(db)
        data.create_tbl_last_ano_mes_download(db)
        data.update_last_ano_mes(args.ano, args.mes, db)
        db.close()
    else:
        Logs.log('Erro: faltando argumento em tentativa de init')
elif args.download:
    #faltando implementação
    if args.ano and args.mes:
        links = fluxo_download_from_args(args.ano[0], args.mes[0])
        print(links)