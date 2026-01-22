'''
lmf

downloader.py

Módulo de download dos arquivos pdf
'''
import requests
import headers
import scrapers.udia as Udia
import utils.logger as Logs

CHUNK_SIZE = 512

'''
    Função principal de download dos documentos
    Retorna o docName do ultimo arquivo salvo

    Atualmente espera a lista de uberlandia, corrigir para receber qualquer cidade
'''
def download_pdfs(links: list[str]):
    session = requests.Session()
    session.headers.update(headers.HEADERS)
    lastDownloadDocName = ''
    try:
        for link in links:
            docName = Udia.doc_name_from_link(link)
            with session.get(link, stream=True, timeout=30) as req:
                Logs.log(f'GET: {docName}')
                if req.status_code != 200:
                    Logs.log(f"Falha no GET: status {req.status_code}")
                else:
                    with open('downloads/' + docName, 'wb') as file:
                        for chunk in req.iter_content(chunk_size=CHUNK_SIZE):
                            file.write(chunk)
                        Logs.log(f'{docName} salvo.')
                        lastDownloadDocName = docName
    except Exception as ex:
        Logs.log(f"Erro no download: {ex}")
    finally:
        Logs.log("Download concluído")
    return lastDownloadDocName