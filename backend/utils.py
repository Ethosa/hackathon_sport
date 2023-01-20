# -*- coding: utf-8 -*-
from random import choice
from string import digits, ascii_letters

arr = digits + ascii_letters + '_'

def gen_token(length: int) -> str:
    return ''.join([choice(arr) for i in range(length)])
