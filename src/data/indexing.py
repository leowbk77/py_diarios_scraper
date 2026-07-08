'''
lmf

indexing.py

Módulo que cuida da indexação dos arquivos pdf no banco para a busca textual
'''
import sqlite3
import datetime
from data import database
from pypdf import PdfReader
from utils.helpers import is_pdf_ext, get_docname_from_uri
from utils import logger as Logs

'''
indexaçao do conteúdo do documento
'''
def index(filePath: str, db: sqlite3.Connection, docId: int):
    pdf = PdfReader(filePath)
    pageIndx = 1
    for page in pdf.pages:
        database.insert_into_tbl_docs_fts(docId, pageIndx, page.extract_text(), db)
        pageIndx += 1
    return True

'''
Indexação do documento local
'''
def index_local(filePath: str, dbName: str, urlBase: str, ano: int, mes: int, dia: int):
    db = database.init(dbName)
    docName = get_docname_from_uri(filePath)
    if is_pdf_ext(filePath):
        #uso futuro com a alteracao do banco
        docDate = datetime.datetime(ano, mes, dia)
        #uso futuro com a alteracao do banco
        docId = database.insert_into_tbl_docs(docName, f"{urlBase}/{docName}", ano, mes, dia, False, db)
        index(filePath, db, docId)
    else: 
        Logs.log("Arquivo não é pdf.")