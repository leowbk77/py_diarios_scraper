'''
lmf

database.py

Gerenciamento do armazenamento dos dados dos documentos
para controle de download e Full Text Search
'''

import sqlite3
import os.path as Dir
import utils.logger as Logs
from utils.helpers import format_sqlite_date_str

def init(db: str) -> sqlite3.Connection:
    return sqlite3.connect(db)

def create_tbl_docs(dbCon: sqlite3.Connection):
    sql = """
            CREATE TABLE IF NOT EXISTS docs
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                nm_edicao TEXT UNIQUE NOT NULL,
                caminho TEXT NOT NULL,
                ano INTEGER NOT NULL,
                mes INTEGER NOT NULL,
                dia INTEGER NOT NULL,
                dt_edicao TEXT NOT NULL)
            """
    sqlNovo = """
            CREATE TABLE IF NOT EXISTS docs
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                nm_edicao TEXT UNIQUE NOT NULL,
                caminho TEXT NOT NULL,
                dt_edicao TEXT NOT NULL)
            """
    cursor = dbCon.cursor()
    cursor.execute(sql)
    dbCon.commit()

def insert_into_tbl_docs(nmEdicao: str, caminho: str, ano: int, mes: int, dia: int, dbCon: sqlite3.Connection) -> int | None:
    dt_edicao = format_sqlite_date_str(ano, mes, dia)
    
    sql = """
            INSERT INTO docs (nm_edicao, caminho, ano, mes, dia, dt_edicao)
            VALUES (?,?,?,?,?,?)
            """
    try:
        cursor = dbCon.cursor()
        cursor.execute(sql, (nmEdicao, caminho, ano, mes, dia, dt_edicao))
        docId = cursor.lastrowid
        dbCon.commit()
    except sqlite3.IntegrityError as err:
        Logs.log(f"ERRO: {err}")
        docId = -1
    return docId

def create_tbl_docs_fts(dbCon: sqlite3.Connection):
    sql = """
            CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts
            USING fts5(doc_id, pagina, conteudo)
            """
    cursor = dbCon.cursor()
    cursor.execute(sql)
    dbCon.commit()

def insert_into_tbl_docs_fts(docId: int, page: int, content: str, dbCon: sqlite3.Connection):
    sql = """
            INSERT INTO docs_fts (doc_id, pagina, conteudo)
            VALUES(?,?,?)
            """
    cursor = dbCon.cursor()
    cursor.execute(sql, (docId, page, content))
    dbCon.commit()
    
def text_search(text: str, dbCon: sqlite3.Connection):
    sql = """
            SELECT * FROM docs_fts WHERE conteudo MATCH '?'
            """
    cursor = dbCon.cursor()
    return cursor.execute(sql, (text))

def db_exists(dbName: str):
    return Dir.isfile(f"./data/{dbName}.db")