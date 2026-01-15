import headers
import scrapers.udia as Udia
import utils.logger as Logs
import downloader
from pypdf import PdfReader

def readF(file: str):
    reader = PdfReader('./data/' + file + '.pdf')
    pageOne = reader.pages[0]
    return pageOne.extract_text()


Logs.init_log()
Udia.urlPaginaAtual = 'https://www.uberlandia.mg.gov.br/2025/12/?post_type=diariooficial'

anoMes = Udia.obter_ano_mes_atual(Udia.urlPaginaAtual)
Udia.anoAtual = anoMes[0]
Udia.mesAtual = anoMes[1]

Logs.log(f"pag: {Udia.urlPaginaAtual}")
Logs.log(f"ano:{Udia.anoAtual} mes:{Udia.mesAtual}")

pagina = Udia.obter_pagina(Udia.urlPaginaAtual)
Logs.log("Pagina obtida, obtendo proxima")

proximaPagina = Udia.obter_proxima_pagina(pagina)
Logs.log(f"proxima obtida: {str(proximaPagina)}, obtendo docs")

docs = Udia.obter_links_dos_documentos(pagina)
Logs.log(f"documentos da pagina atual obtidos, iniciando download dos 3 primeiros")

print()
print(docs)
print()

tresDocs = []
tresDocs.append(docs[0])
tresDocs.append(docs[1])
tresDocs.append(docs[2])

downloader.download_docs(tresDocs)
