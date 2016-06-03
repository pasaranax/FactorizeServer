'''
Created on 01 июня 2016 г.

@author: Михаил Булыгин <pasaranax@gmail.com>
'''

from multiprocessing import Process  # @UnresolvedImport
import json
import sqlite3 as sql
from datetime import datetime
from random import randint
from time import perf_counter as pc
from lib import factorize


class SessionHandler():
    '''
    Обработчик сессии клиента. Выполняет запрос и сохраняет данные.
    '''
    
    def __init__(self, environ):
        '''
        В конструкторе создается соединение с БД и загружается или создается новая сессия
        :param environ: окружение, приходит с веб-сервера
        '''
        self.connect_db()
        
        self.query = {}
        if "QUERY_STRING" in environ:
            self.query = self.parse_query(environ["QUERY_STRING"])
            
        cookie = {}
        if "HTTP_COOKIE" in environ:
            cookie = self.parse_cookie(environ["HTTP_COOKIE"])
            if "sid" in cookie:
                sid_exists = self.conn.execute("SELECT * FROM sessions WHERE sid = ?", (cookie["sid"],))
                if sid_exists:
                    self.sid = cookie["sid"]
                else:
                    self.new()
            else:
                self.new()
        else:
            self.new()
            
    def parse_cookie(self, string):
        '''
        Разбирает строку с куками и возвращает словарь
        :param string: строка из окружения
        '''
        cookie = {}
        if "; " in string:
            for fragment in string.split("; "):
                frags = fragment.split("=")
                if len(frags) > 1:
                    cookie[frags[0]] = frags[1]
        else:
            frags = string.split("=")
            if len(frags) > 1:
                cookie[frags[0]] = frags[1]
        return cookie
    
    def parse_query(self, string):
        '''
        Разбирает строку с данными запроса и возвращает параметры в виде словаря
        :param string: строка из окружения
        '''
        query = {}
        if "&" in string:
            for fragment in string.split("&"):
                frags = fragment.split("=")
                if len(frags) > 1:
                    query[frags[0]] = frags[1]
        else:
            frags = string.split("=")
            if len(frags) > 1:
                query[frags[0]] = frags[1]
        return query
        
    def result(self):
        '''
        Формирует ответ на основе данных запроса
        '''
        if "number" in self.query:
            try:
                number = int(self.query["number"])
            except(ValueError, KeyError):
                number = 0
            if 1 < number <= 10**9:  # при неболших значениях выполняем в текущем потоке 
                self.operate(number, self.sid)
            elif number > 10**9:  # при больших начениях запускаем отдельный процесс
                operation = Process(target=self.operate, args=(number, self.sid), daemon=True)
                operation.start()
                
        history = self.load()
        dump = json.dumps(history)
        return dump
    
    def operate(self, number, sid):
        '''
        Подсчет результата и запись его в БД. Для запуска в отдельном потоке
        :param number: введенное число
        :param sid: id сессии
        '''
        timer = pc()
        answer = json.dumps(list(factorize(number)))
        timer = round(pc() - timer, 3)
        conn = sql.connect("sessions.db")
        conn.execute("INSERT INTO sessions VALUES(?, ?, ?, ?, ?)", (sid, str(number), answer, timer, datetime.now()))
        conn.commit()

    def connect_db(self):
        '''
        Соединение с БД sqlite3, где хранятся данные клиентов.
        Это соединение используется только для чтения и вывода истории клиента
        '''
        self.conn = sql.connect("sessions.db")
        
    def new(self):
        '''
        Генерирует новую сессию
        '''
        self.sid = str(randint(100000000000, 999999999999))
        
    def load(self):
        '''
        Выгружает из базы 10 последних результатов для данного клиента
        '''
        rows = self.conn.execute("SELECT * FROM sessions WHERE sid = ? ORDER BY time DESC LIMIT 10", (self.sid,))
        history = list(rows)
        return history
    
    
    
    