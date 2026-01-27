'''
lmf

indexing.py

Módulo que cuida da indexação dos arquivos pdf no banco para a busca textual
'''
import sqlite3
from data import database
from pypdf import PdfReader
'''

'''
def index_file(filePath: str, db: sqlite3.Connection, docId: int):
    pdf = PdfReader(filePath)
    pageIndx = 1
    for page in pdf.pages:
        database.insert_into_tbl_docs_fts(docId, pageIndx, page.extract_text(), db)
        pageIndx += 1
    return True