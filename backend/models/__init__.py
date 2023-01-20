# -*- coding: utf-8 -*-
from enum import IntEnum

from pydantic import BaseModel


class Solution(BaseModel):
    code: str
    access_token: str
    task_id: int
    lang: int


class Task(BaseModel):
    title: str
    description: str


class User(BaseModel):
    name: str
    group: str
    login: str
    password: str


class Mark(BaseModel):
    task_id: int
    user_id: int
    score: int
    used_lang: str


class Language(IntEnum):
    Python = 1
    CSharp = 2
    Java = 3
