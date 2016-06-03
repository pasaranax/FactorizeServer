'''
Created on 1 июня 2016 г.

@author: Михаил Булыгин <pasaranax@gmail.com>
'''

def factorize(n):
    '''
    Факторизация числа перебором. Генерирует простые множители.
    :param n: число, которое нужно разложить на множители
    '''
    if type(n) is int and n > 1:
        divisor = 2
        while divisor ** 2 <= n:
            if n % divisor == 0:
                n //= divisor
                yield divisor
            else:
                if divisor == 2:
                    divisor += 1
                else:
                    divisor += 2
        yield n
    else:
        yield 0
        
        