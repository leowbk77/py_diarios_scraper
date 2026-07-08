from os import listdir
from os.path import isfile, join
import mimetypes


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

def get_docname_from_uri(filePath: str):
    return 'tmp'