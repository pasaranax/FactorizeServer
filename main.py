'''
Created on 31 мая 2016 г.

@author: Михаил Булыгин <pasaranax@gmail.com>
'''

from wsgiref.simple_server import make_server
from web_app import web_app

    
if __name__ == '__main__':
    httpd = make_server("localhost", 8000, web_app)
    httpd.serve_forever()
    

    