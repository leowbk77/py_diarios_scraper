from os import listdir
from os.path import isfile, join
import mimetypes
import ntpath


'''
    Verifica se o arquivo da requisição é um pdf
'''
def is_pdf(content_type: str | None):
    if mimetypes.guess_extension(content_type) == '.pdf':
        return True
    return False

'''
    Retorna a lista de arquivos do diretorio
'''
def file_list_in(directory: str):
    return [file for file in listdir(directory) if isfile(join(directory, file))]

'''
    Retorna True para arquivo pdf e False para outros arquivos
'''
def is_pdf_ext(file: str):
    return file.lower().endswith('.pdf')

'''
    Obtém o nome o nome do documento a partir da uri
'''
def get_docname_from_uri(filePath: str):
    # https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
    head, tail = ntpath.split(filePath)
    return tail or ntpath.basename(head)

'''
    Formata a string para conter o zero a esquerda em caso de dias e meses entre 1 e 9
'''
def format_dia_mes_str(diaMes: int):
    if diaMes < 10:
        strFormatada = f"0{diaMes}"
    else:
        strFormatada = str(diaMes)
    return strFormatada

'''
    Formata a data para o sqlite a partir do input de ano, mes e dia
'''
def format_sqlite_date_str(ano: int, mes: int, dia: int):
    return f'{ano}-{format_dia_mes_str(mes)}-{format_dia_mes_str(dia)}'

'''
    Formata a url de base da indexacao local para remover o / do final caso
    exista
'''
def format_url_base(url: str):
    if url.endswith('/'):
        return url[:-1]
    else: 
        return url