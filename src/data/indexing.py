'''
lmf

indexing.py

Módulo que cuida da indexação dos arquivos pdf no banco para a busca textual
'''
import sqlite3
from data import database
from pypdf import PdfReader
from utils.helpers import is_pdf_ext, get_docname_from_uri, format_url_base
from utils import logger as Logs

'''
indexaçao do conteúdo do documento
'''
def index(filePath: str, db: sqlite3.Connection, docId: int):
    pdf = PdfReader(filePath)
    
    for idx, page in enumerate(pdf.pages, start=1):
        # trycatch para pular paginas com erro
        # caso arquivos tenham paginas muito grandes para extração
        # como ocorre em pdfs com imagens scaneadas que podem gerar extração muito grande
        # e não tem utilidade para extração textual
        try:
            text = page.extract_text()
            database.insert_into_tbl_docs_fts(docId, idx, text, db)
        except Exception as e:
            Logs.log(f"Página {idx}: {e}")
    return True

    ''' bloco antigo que gerava erro e impedia a extração total
    pageIndx = 1
    for page in pdf.pages:
        database.insert_into_tbl_docs_fts(docId, pageIndx, page.extract_text(), db)
        pageIndx += 1
    return True
    '''
    

'''
Indexação do documento local
'''
def index_local(filePath: str, dbName: str, urlBase: str, ano: int, mes: int, dia: int):
    db = database.init(f"./data/{dbName}.db")
    if is_pdf_ext(filePath):
        docName = get_docname_from_uri(filePath)
        Logs.log(f"Arquivo com extencao pdf - docName obtido: {docName} - Inserindo na base e indexando paginas...")
        docId = database.insert_into_tbl_docs(docName, f"{format_url_base(urlBase)}/{docName}", ano, mes, dia, db)
        if docId != (-1):
            index(filePath, db, docId)
        else:
            Logs.log(f"{docName} já possui uma entrada indexada ou erro de indexacao ocorreu.")
    else:
        Logs.log("Arquivo não é pdf. Indexacao não realizada.")