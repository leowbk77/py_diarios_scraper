'''
lmf
downloader.py
Módulo de download dos arquivos pdf
'''
import requests
import headers
import scrapers.udia as udia
import utils.logger as Logs

CHUNK_SIZE = 512

'''
    Função principal de download dos documentos
    Retorna o docName do ultimo arquivo salvo
'''
def download_docs(documentos: list[str]):
    session = requests.Session()
    session.headers.update(headers.HEADERS)
    lastDownloadDocName = ''
    try:
        for documento in documentos:
            pdf = udia.obter_link_pdf(documento)
            docName = udia.obter_edicao_documento(documento) + '.pdf'
            with session.get(pdf, stream=True, timeout=30) as req:
                Logs.log(f'GET: {docName}')
                if req.status_code != 200:
                    Logs.log(f"Falha no GET: status {req.status_code}")
                else:
                    with open('downloads/' + docName, 'wb') as file:
                        for chunk in req.iter_content(chunk_size=CHUNK_SIZE):
                            file.write(chunk)
                        Logs.log(f'{docName} salvo.')
                        lastDownloadDocName = docName
    except Exception:
        Logs.log("Erro no download")
    finally:
        Logs.log("Download concluído")
    return lastDownloadDocName