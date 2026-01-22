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
import headers
from bs4 import BeautifulSoup
'''
uso de sessão para evitar reenvio de parametros
ja que será feito grande número de conexões ao mesmo host
'''
session = requests.Session()
session.headers.update(headers.HEADERS)
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
    baseUrl = 'https://docs.uberlandia.mg.gov.br/wp-content/uploads/' + ano + '/' + mes + '/'
    links = []
    for documento in documentos:
        urlPdf = baseUrl + documento[7:] + '.pdf'
        links.append(urlPdf)
    return links


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

