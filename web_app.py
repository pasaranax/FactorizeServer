'''
Created on 01 июня 2016 г.

@author: Михаил Булыгин <pararanax@gmail.com>
'''

from SessionHandler import SessionHandler
from mimetypes import guess_type
from os.path import exists


def web_app(environ, start_response):
    '''
    WSGI-приложение с простым обработчиком запросов
    '''
    if environ["PATH_INFO"] == "/factorize":  # запрос к основному скрипту
        session = SessionHandler(environ)
        out = session.result()
        out = out.encode("utf-8")
        status = '200 OK'
        headers = [('Content-type', 'Content-type: application/json; charset=utf-8')]
    elif environ["PATH_INFO"].startswith("/client/"):  # статические объекты (веб-клиент)
        filename = environ["PATH_INFO"][8:].split("?")[0]
        if not filename:
            filename = "index.html"
        out, status, headers = get_static(filename)
    else:  # все остальное не интересует
        out = "404".encode("utf-8")
        status = '404 NOT FOUND'
        headers = [('Content-type', 'Content-type: text/html; charset=utf-8')]
    
    start_response(status, headers)
    
    return [out]

def get_static(filename):
    '''
    Проверяет статический файл в папке client/, отдает нужные заголовки, статус и содержимое
    :param filename: имя файла
    '''
    
    # по умолчанию выдаем ошибку
    status = "404 NOT FOUND"
    headers = [('Content-type', 'Content-type: text/html; charset=utf-8')]
    out = "404".encode("utf-8")

    if exists("client/" + filename):
        # отдает только картинки и html/javascript
        mime = guess_type(filename)[0]
        if not mime:
            pass
        elif "image/" in mime:
            f = open("client/" + filename, mode="rb")
            out = f.read()
            f.close()
            status = '200 OK'
            headers = [('Content-type', 'Content-type: {}'.format(mime))]
        elif "html" in mime or "javascript" in mime:
            f = open("client/" + filename)
            out = f.read()
            f.close()
            out = out.encode("utf-8")
            status = '200 OK'
            headers = [('Content-type', 'Content-type: {}; charset=utf-8'.format(mime))]
    
    return out, status, headers
    