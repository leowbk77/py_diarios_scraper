'''
udia.py\n
Léo MF.\n
versao inicial do scraper para o site da prefeitura de Uberlândia\n\n

DOCS BS4: https://beautiful-soup-4.readthedocs.io/en/latest/# \n
DOCS REQUESTS: https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request
\n\n
    - tratamento de erros não implementado\n
    - download e acesso ao html ok\n
'''
import requests
from bs4 import BeautifulSoup
from utils import logger as Logs, net
'''
uso de sessão para evitar reenvio de parametros
ja que será feito grande número de conexões ao mesmo host
'''
session = requests.Session()
session.headers.update(net.HEADERS)
'''
Para páginas pós 2018:
https://www.uberlandia.mg.gov.br/2025/12/?post_type=diariooficial
Para páginas pré 2018:
https://www.uberlandia.mg.gov.br/2015/01/?post_type=diario_oficial
'''
urlPaginaAtual = ''
anoAtual = ''
mesAtual = ''

''' 
    Obtém a página e retorna o obj BS que permite navegar 
'''
def obter_pagina(url: str | bytes) -> BeautifulSoup:
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

'''
    Retorna a próxima página a partir do objeto da página atual (retorno de  obter_pagina())
'''
def proxima_pagina(paginaAtual: BeautifulSoup):
    proxima = paginaAtual.find('a', 'page-numbers next') # retorna None se nao achar nada.
    if proxima is None:
        return None
    return proxima.get('href')

'''
    Retorna uma lista com os nomes dos documentos disponíveis na página
'''
def obter_docs(pagina: BeautifulSoup):
    diarios = pagina.find_all("h3", class_="elementor-post__title")
    docs = []
    for documentos in diarios:
        docs.append(str(documentos.a.string.strip()))
    return docs

'''
    Retorna o ano e o mes (ano, mes) da url de página de diários
    Sem tratamento de erros.
'''
def obter_ano_mes_atual(url: str):
    anoIndex = 3
    mesIndex = 4
    dados = url.split('/')
    return (dados[anoIndex], dados[mesIndex])

'''
    Retorna a url da pagina para o scraping montada a partir do ano e mes
'''
def mount_pagina_url(ano: int, mes: int):
    baseUrl = 'https://www.uberlandia.mg.gov.br' + '/' + str(ano) + '/' + str(mes) + '/' + '?post_type='
    if ano >= 2018:
        return baseUrl + 'diariooficial'
    return baseUrl + 'diario_oficial'

'''
    Retorna a lista de links dos pdfs a partir da lista gerada em obter_docs()
'''
def pdf_links_from_doc_list(documentos: list[str], ano: int, mes: int):
    anoUrl = str(ano)
    if mes < 10:
        mesUrl = '0' + str(mes)
    else:
        mesUrl = str(mes)
    baseUrl = 'https://docs.uberlandia.mg.gov.br/wp-content/uploads/' + anoUrl + '/' + mesUrl + '/'
    links = []
    for documento in documentos:
        urlPdf = baseUrl + documento[7:] + '.pdf'
        links.append(urlPdf)
    return links

def doc_name_from_link(link: str):
    return link.split('/')[7]

'''
    Realiza o download dos arquivos a partir da lista de links
    gerada pela pdf_links_from_doc_list()
'''
def download_pdfs(links: list[str]):
    lastDownloadDocName = ''
    try:
        for link in links:
            docName = doc_name_from_link(link)
            with session.get(link, stream=True, timeout=27) as req:
                Logs.log(f'GET: {docName}')
                if req.status_code != 200:
                    Logs.log(f"Falha no GET: status {req.status_code}")
                else:
                    with open('downloads/' + docName, 'wb') as file:
                        for chunk in req.iter_content(chunk_size=net.CHUNK_SIZE):
                            file.write(chunk)
                        Logs.log(f'{docName} salvo.')
                        lastDownloadDocName = docName
    except Exception as ex:
        Logs.log(f"Erro no download: {ex}")
    finally:
        Logs.log("Download concluído")
    return lastDownloadDocName

'''
    Funçao que executa o fluxo de download
'''
def fluxo_download(ano: int, mes: int):
    Logs.log('Iniciando fluxo de obtencao dos links dos pdfs')
    try:
        paginaURL = mount_pagina_url(ano, mes)
        Logs.log(f"Link inicial de pagina obtido: {paginaURL}")
        docsLinks = []
        while(paginaURL is not None):
            pagina = obter_pagina(paginaURL)
            Logs.log('Pagina obtida, obtendo lista de documentos...')
            for documento in obter_docs(pagina):
                docsLinks.append(documento)
            Logs.log('Documentos obtidos, obtendo proxima página...')
            paginaURL = proxima_pagina(pagina)
            Logs.log(f"Proxima pagina: {str(paginaURL)}")
        Logs.log(f'Lista de documentos do mes {str(mes)} obtida, gerando links de pdf...')
        pdfLinks = pdf_links_from_doc_list(docsLinks, ano, mes)
    except Exception as ex:
        Logs.log(f"Erro no fluxo: {ex}")
    Logs.log('Iniciando o download a partir da lista de pdfs obtida...')
    return download_pdfs(pdfLinks)

#=====================================Funções que serão substituidas===================================

''' 
    Retorna o nome do documento a partir da url de acesso
    A url de acesso é obtida na lista retornada pela obter_links_dos_documentos()
    Deprecated ----- Usar somente para testes -------------
'''
def obter_edicao_documento(urlDocumento: str):
    # BASE: 'https://www.uberlandia.mg.gov.br/diariooficial/edicao-7253/'
    # pre-2018 https://www.uberlandia.mg.gov.br/diario-oficial/edicao-5287/
    edicao = urlDocumento.split('/')[4]
    return edicao[7:].upper()
'''
    Retorna uma lista com os documentos disponíveis no objeto da pagina
    Deprecated ----- Usar o obter_docs ------------------
'''
def obter_links_dos_documentos(paginaAtual: BeautifulSoup):
    diarios = paginaAtual.find_all("h3", class_="elementor-post__title")
    documentos = []
    for documento in diarios:
        documentos.append(documento.a.get('href'))
    return documentos
'''
    Retorna a lista com os links para download dos pdfs a partir da lista de documentos 
    (retorno de obter_links_dos_documentos())
    Deprecated ----- Usar somente para testes -------------
'''
def obter_link_pdfs_from_list(documentos: list[str]):
    baseUrl = 'https://docs.uberlandia.mg.gov.br/wp-content/uploads/'
    urlAtual = baseUrl + anoAtual + '/' + mesAtual + '/'
    pdfs = []
    for documento in documentos:
        urlPdf = urlAtual + obter_edicao_documento(documento) + '.pdf'
        pdfs.append(urlPdf)
    return pdfs
'''
    Obtém o link para o arquivo pdf no site da prefeitura a partir
    do link do documento obtido na lista de docs retornada em 
    (obter_links_dos_documentos())
    Deprecated ----- Usar somente para testes -------------
'''
def obter_link_pdf(documento: str):
    baseUrl = 'https://docs.uberlandia.mg.gov.br/wp-content/uploads/'
    urlAtual = baseUrl + anoAtual + '/' + mesAtual + '/'
    return urlAtual + obter_edicao_documento(documento) + '.pdf'

