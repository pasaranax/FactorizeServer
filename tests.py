'''
Created on 01 июня 2016 г.

@author: Михаил Булыгин <pasaranax@gmail.com>
'''


import unittest
from lib import factorize
from web_app import web_app
from SessionHandler import SessionHandler
import json


class Test(unittest.TestCase):


    def test_factorize(self):
        '''
        Тестирует функцию факторизации
        '''
        input_values = [None, "string", False, 0.1, 9e-20, -3e-90, -0.1, 2.5, 
                        -100500, -10**100, -1, 0, 1, [], {}, [1, 2], {"a": self},
                        2, 3, 4, 5, 7, 13, 100, 1001, 13**10, 1234567890123456, 10*100+1]
        for value in input_values:
            result = factorize(value)
            result = list(result)
            first = result[0]
            self.assertIsInstance(result, list, value)
            self.assertIsInstance(first, int, value)
            
    def test_web_app(self):
        '''
        Тестирует web_app и get_static (внутри web_app)
        '''
        start_response = lambda a, b: None
        
        # тест на правильный вариант
        environ = {"PATH_INFO": "/client/",
                   "QUERY_STRING": "number=12345678", 
                   "HTTP_COOKIE": "sid=123"}
        res = web_app(environ, start_response)
        self.assertIsInstance(res[0], bytes, res)
        self.assertGreater(len(res[0]), 20, res)
        
        # множественный тест
        environ_variants = [{"PATH_INFO": "/factorize"},
                            {"PATH_INFO": "/factorize?ololo"},
                            {"PATH_INFO": "/factorize?number"},
                            {"PATH_INFO": "/factorize?smth=*&number=10"},
                            {"PATH_INFO": "/factorize?smth=&&&ololo"},
                            {"PATH_INFO": "/factorise"},
                            {"PATH_INFO": "qqqqqqq"},
                            {"PATH_INFO": "/client"},
                            {"PATH_INFO": "/client/"},
                            {"PATH_INFO": "/client/index.html?11"},
                            {"PATH_INFO": "/client/functions.js"},
                            {"PATH_INFO": "/client/../sessions.db"},
                            {"PATH_INFO": "/client/hex-loader2.gif"},
                            {"PATH_INFO": "/client/hex-loader.gif"},
                            {"PATH_INFO": "/client/lostfile"},
                            {"PATH_INFO": "/client/lostfile.py"},
                            {"PATH_INFO": "/client/lostfile.php"},
                            {"PATH_INFO": "/client/lostfile.html"},
                            {"PATH_INFO": "/client/."},
                            {"PATH_INFO": "/client/.."}]
        for environ in environ_variants:
            query = {"QUERY_STRING": ""}
            environ.update(query)
            
            res = web_app(environ, start_response)
            first = res[0]
            self.assertIsInstance(res, list, environ)
            self.assertIsInstance(first, bytes, environ)
            
    def test_SessionHandler(self):
        '''
        Тестирует класс, отвечающий за сессии
        '''
        # тест на правильный вариант
        environ = {"QUERY_STRING": "number=12345678", "HTTP_COOKIE": "sid=123"}
        session = SessionHandler(environ)
        out = session.result()
        first = json.loads(json.loads(out)[0][2])
        second = [2, 3, 3, 47, 14593]
        self.assertEqual(first, second, environ)
        
        # множественный тест
        environ_variants = [{"QUERY_STRING": "number=1234567890", "HTTP_COOKIE": ""},
                            {"QUERY_STRING": "number=-1", "HTTP_COOKIE": "sid=123"},
                            {"QUERY_STRING": "1", "HTTP_COOKIE": "q=423432543215"},
                            {"HTTP_COOKIE": ""},
                            {"SOMETHING": "poo"},]
        for environ in environ_variants:
            session = SessionHandler(environ)
            out = session.result()
            self.assertIsInstance(out, str, environ)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()