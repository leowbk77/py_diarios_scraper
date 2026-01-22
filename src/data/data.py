'''
lmf

data.py

Gerenciamento do armazenamento dos dados dos documentos
para controle de download e Full Text Search
'''

import sqlite3

def init_database(db: str) -> sqlite3.Connection:
    return sqlite3.connect(db)

def create_tbl_docs(dbCon: sqlite3.Connection):
    sql = """
            CREATE TABLE IF NOT EXISTS docs
                (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nm_edicao TEXT UNIQUE
                )
            """
    cursor = dbCon.cursor()
    cursor.execute(sql)
    dbCon.commit()

def insert_into_tbl_docs(nmEdicao: str, dbCon: sqlite3.Connection):
    sql = """
            INSERT INTO docs (nm_edicao)
            VALUES (?)
            """
    cursor = dbCon.cursor()
    cursor.execute(sql, (nmEdicao))
    dbCon.commit()

def create_tbl_docs_fts(dbCon: sqlite3.Connection):
    sql = """
            CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts
            USING fts5(doc_id, pagina, conteudo)
            """
    # SELECT * FROM docs WHERE conteudo MATCH 'uvwxyz';
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
    
def create_tbl_last_ano_mes_download(dbCon: sqlite3.Connection):
    sqlLastAnoMesDownload = """
                                CREATE TABLE IF NOT EXISTS last_ano_mes_download
                                    (
                                    id INTEGER PRIMARY KEY,
                                    ano INTEGER NOT NULL CHECK(ano > 0),
                                    mes INTEGER NOT NULL CHECK(mes > 0 AND mes <= 12)
                                    last_doc TEXT
                                    )
                                """
    sqlInitAnoMesDownload = """
                                INSERT INTO last_ano_mes_download (id, ano, mes)
                                VALUES (1, 2015, 1, 'x.pdf')
                                """
    cursor = dbCon.cursor()
    cursor.execute(sqlLastAnoMesDownload)
    cursor.execute(sqlInitAnoMesDownload)
    dbCon.commit()

def update_last_ano_mes(ano: int, mes: int, dbCon: sqlite3.Connection):
    sql = "UPDATE last_ano_mes_download SET ano = ?, mes = ? WHERE id = 1"
    cursor = dbCon.cursor()
    cursor.execute(sql, (ano, mes))
    dbCon.commit()

def update_last_ano_mes_docName(lastDoc: str, dbCon: sqlite3.Connection):
    sql = "UPDATE last_ano_mes_download SET last_doc = ? WHERE id = 1"
    cursor = dbCon.cursor()
    cursor.execute(sql, (lastDoc))
    dbCon.commit()

def get_last_ano(dbCon: sqlite3.Connection):
    sql = "SELECT ano FROM last_ano_mes_download WHERE id = 1"
    cursor = dbCon.cursor()
    res = cursor.execute(sql)
    return res.fetchone()

def get_last_mes(dbCon: sqlite3.Connection):
    sql = "SELECT mes FROM last_ano_mes_download WHERE id = 1"
    cursor = dbCon.cursor()
    res = cursor.execute(sql)
    return res.fetchone()