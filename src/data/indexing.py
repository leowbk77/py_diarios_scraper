'''
lmf

indexing.py

Módulo que cuida da indexação dos arquivos pdf no banco para a busca textual
'''
import sqlite3
from data import database
from pypdf import PdfReader

'''
    Faltando implementacao
'''
def index_file(file: str, db: sqlite3.Connection):
    pdf = PdfReader(file)
    database.insert_into_tbl_docs_fts(1, 3, pdf.pages[3].extract_text(), db)
    db.close()
    return True