'''
udia.py

Léo MF.

Scraper para o site dos diários oficiais da prefeitura de Uberlândia
'''
import requests
import mimetypes
from bs4 import BeautifulSoup
from data import indexing as Indx, database as dbUdi
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
FILESDIR = './downloads/'
DATABASE = './data/udi.db'
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
    Retorna o ano e o mes (ano, mes) da url do link de acesso 
    do pdf.

    Sem tratamento de erros.
'''
def ano_mes_from_pdf_link(link: str):
    anoIndex = 5
    mesIndex = 6
    dados = link.split('/')
    return (int(dados[anoIndex]), int(dados[mesIndex]))

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

'''
    Retorna o nome do arquivo a partir do link de pdf gerado
    na lista do pdf_links_from_doc_list()
'''
def doc_name_from_link(link: str):
    return link.split('/')[7]

'''
    Verifica se o download foi de um pdf
'''
def is_pdf(content_type: str | None):
    if mimetypes.guess_extension(content_type) == '.pdf':
        return True
    return False

'''
    faz o index no db
    falta logs
'''
def index_file(filePath: str, link: str, ano: int, mes: int, docName: str):
    db = dbUdi.init(DATABASE)
    docId = dbUdi.insert_into_tbl_docs(docName, link, ano, mes, False, db)
    Indx.index_file(filePath, db, docId)
    dbUdi.update_doc_indexado(docId, db)
    db.close()

'''
    Salva o arquivo obtido no request
'''
def save_file(path: str, request: requests.Response):
    with open(path, 'wb') as file:
        for chunk in request.iter_content(chunk_size=net.CHUNK_SIZE):
            file.write(chunk)

'''
    Tenta obter o link de uma resposta que veio quebrada.
'''
def find_link_on_html(htmlPath: str):
    stringFound = ''
    with open(htmlPath, 'rt', encoding='utf-8') as file:
        html = file.read()
        startPos = html.find("window.location=\"https://docs.uberlandia.mg.gov.br/wp-content/uploads/")
        endPos = html.find(';', startPos)
        stringFound = html[startPos:endPos]
    return stringFound[17:-1]

'''
    Funcao que refaz o link de acesso para os arquivos que vem quebrados
'''
def rebuild_pdf_link(docName: str, ano: int):
    baseUrl = "https://www.uberlandia.mg.gov.br/"
    if ano >= 2018:
        baseUrl = baseUrl + 'diariooficial/edicao-'
    else:
        baseUrl = baseUrl + 'diario_oficial/edicao-'
    return f"{baseUrl}{docName.lower()[:-4]}"

'''
    Funcao que tenta reobter o arquivo que está com link quebrado
'''
def retry_get_pdf(link: str, docLocalPath: str):
    pdfFileName = docLocalPath[:-5]
    with session.get(link, stream=True, timeout=27) as get:
        save_file(docLocalPath, get)
    link = find_link_on_html(docLocalPath)
    with session.get(link, stream=True, timeout=27) as req:
        if req.status_code != 200:
            Logs.log(f"Falha no GET: status {req.status_code}")
        else:
            save_file(pdfFileName, req)
    return pdfFileName


'''
    Realiza o download dos arquivos a partir da lista de links
    gerada pela pdf_links_from_doc_list()
    e indexa.
'''
def download_and_index_pdfs(links: list[str]):
    try:
        for link in links:
            docName = doc_name_from_link(link)
            docAno, docMes = ano_mes_from_pdf_link(link)
            docLocalPath = f"{FILESDIR}/{docName}"
            Logs.log(f'GET: {docName}')
            with session.get(link, stream=True, timeout=27) as req:
                if req.status_code != 200:
                    Logs.log(f"Falha no GET: status {req.status_code}")
                else:
                    if is_pdf(req.headers.get('content-type')):
                        #criar uma funcao
                        Logs.log('PDF obtido - salvando e indexando.')
                        save_file(docLocalPath, req)
                        Logs.log(f'{docName} salvo. Indexando...')
                        index_file(docLocalPath, link, docAno, docMes, docName)
                    else:
                        # faltando implementacao
                        Logs.log(f"Falha: Arquivo não é um pdf - Possvel link quebrado - tentando reobter link")
                        #save_file(f"{docLocalPath}.html", req)
                        #Logs.log(f"{docName}.html salvo.")
                        #realizar download novamente
                        retry_get_pdf(rebuild_pdf_link(docName, docAno), f"{docLocalPath}.html")
    except Exception as ex:
        Logs.log(f"Erro no download and Index: {ex}")
        raise
    finally:
        Logs.log("Download e Index concluidos")

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
    return download_and_index_pdfs(pdfLinks)