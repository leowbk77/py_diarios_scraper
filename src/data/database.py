'''
lmf

database.py

Gerenciamento do armazenamento dos dados dos documentos
para controle de download e Full Text Search
'''

import sqlite3

def init(db: str) -> sqlite3.Connection:
    return sqlite3.connect(db)

def create_tbl_docs(dbCon: sqlite3.Connection):
    sql = """
            CREATE TABLE IF NOT EXISTS docs
                (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nm_edicao TEXT UNIQUE NOT NULL,
                caminho TEXT NOT NULL,
                ano INTEGER NOT NULL,
                mes INTERGER NOT NULL,
                indexado BOOLEAN NOT NULL
                )
            """
    cursor = dbCon.cursor()
    cursor.execute(sql)
    dbCon.commit()

def insert_into_tbl_docs(nmEdicao: str, caminho: str, ano: int, mes: int, indexado: bool, dbCon: sqlite3.Connection) -> int | None:
    # falta tratamento de erro para arquivos de mesmo nome
    # colocar um try catch para sqlite3.IntegrityError: UNIQUE constraint failed: docs.nm_edicao
    sql = """
            INSERT INTO docs (nm_edicao, caminho, ano, mes, indexado)
            VALUES (?,?,?,?,?)
            """
    cursor = dbCon.cursor()
    cursor.execute(sql, (nmEdicao, caminho, ano, mes, indexado))
    docId = cursor.lastrowid
    dbCon.commit()
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

def update_doc_indexado(docId: int, dbCon: sqlite3.Connection):
    sql = """
            UPDATE docs
            SET indexado = TRUE
            WHERE id = ?
            """
    cursor = dbCon.cursor()
    cursor.execute(sql, [docId])
    dbCon.commit()
    return True
    
def text_search(text: str, dbCon: sqlite3.Connection):
    sql = """
            SELECT * FROM docs_fts WHERE conteudo MATCH '?'
            """
    cursor = dbCon.cursor()
    return cursor.execute(sql, (text))