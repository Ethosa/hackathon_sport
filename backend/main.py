# -*- coding: utf-8 -*-
import asyncio
import json

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from re import findall
from os import getcwd, path, mkdir
from database import db, cur

from uvicorn import Server, Config

from cmplr import PythonCompiler, JavaCompiler, CSharpCompiler
from cmplr.solution_wizard import SolutionWizard
from cmplr.maat import Maat
from models import Solution, User, Task, Mark, Language, Role
from utils import gen_token
from config import ADMIN_TOKEN


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
)


async def set_body(request: Request, body: bytes):
    async def receive():
        return {"type": "http.request", "body": body}
    request._receive = receive


@app.middleware('http')
async def check_token(request: Request, call_next):
    if request.method == 'POST':
        body = await request.body()
        secret = json.loads(body)
        if 'access_token' in request.query_params:
            token = request.query_params['access_token']
            u = cur.execute('SELECT * FROM user WHERE access_token = ?', (token,)).fetchone()
            # role 2 is Admin role
            if u is None or u[6] != 2:
                return JSONResponse({
                    "error": "Method not allowed",
                    "code": 100
                }, status_code=status.HTTP_401_UNAUTHORIZED)
        elif 'admin' not in secret and secret['admin'] != ADMIN_TOKEN:
            return JSONResponse({
                "error": "Method not allowed",
                "code": 100
            }, status_code=status.HTTP_401_UNAUTHORIZED)
        await set_body(request, body)
    response = await call_next(request)
    return response


@app.get('/user{user_id}')
async def send_solution(user_id: int):
    user = cur.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
    user_marks = cur.execute('SELECT * FROM mark WHERE user_id = ?', (user_id,)).fetchall()
    if user is None:
        return {'error': 'User is not exists', 'code': 0}
    return {'response': {
        'id': user[0],
        'name': user[1],
        'group': user[2],
        'role': user[6],
        'marks': [{
            'id': mark[0],
            'task_id': [{
                'id': solution[0],
                'title': solution[1]
            } for solution in
                cur.execute('SELECT * FROM task WHERE id = ?', (mark[1],)).fetchall()
            ],
            'user_id': mark[2],
            'score': mark[3]
        } for mark in user_marks]
    }}


@app.post('/user')
async def create_new_user(user: User):
    access_token = gen_token(32)
    cur.execute('''
        INSERT INTO user (name, group_name, login, password, access_token, role)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user.name, user.group, user.login, user.password, access_token, 1))
    db.commit()
    return {'response': {'id': cur.lastrowid, 'access_token': access_token}}


@app.get('/leaders-list')
async def get_leaders():
    users = cur.execute('SELECT * FROM user WHERE role = ?', (Role.USER,)).fetchall()
    scores = []
    for user in users:
        marks = cur.execute('SELECT * FROM mark WHERE user_id = ?', (user[0],)).fetchall()
        scores.append({
            'id': user[0],
            'name': user[1],
            'group': user[2],
            'score': sum([i[3] for i in marks]),
            'login': user[3],
            'decided': len(marks)
        })
    scores = sorted(scores, key=lambda x: x['score'] + x['decided'], reverse=True)
    return scores


@app.post('/boost{user_id}')
async def boost_user(user_id: int):
    u = cur.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
    if u is None:
        return {'error': 'User is not exists', 'code': 0}
    cur.execute('UPDATE user SET role = 2 WHERE id = ?', (user_id,))
    db.commit()
    return {'response': 'success'}


@app.get('/auth')
async def auth(login: str, password: str):
    user = cur.execute(
        'SELECT * FROM user WHERE login = ? and password = ?',
        (login, password)
    ).fetchone()
    if user is None:
        return {'error': 'Incorrect login or password', 'code': 1}
    return {'response': {'id': user[0], 'access_token': user[5]}}


@app.get('/langs')
async def get_lang_by_id():
    langs = cur.execute('SELECT * FROM lang').fetchall()
    return {'response': [{'title': lang[1], 'name': lang[2]} for lang in langs]}


@app.get('/lang{lang_id}')
async def get_lang_by_id(lang_id: int):
    lang = cur.execute('SELECT * FROM lang WHERE id = ?', (lang_id,)).fetchone()
    if lang is None:
        return {'error': 'Language is not exists', 'code': 50}
    return {'response': {'title': lang[1], 'name': lang[2]}}


@app.get('/roles')
async def get_lang_by_id():
    roles = cur.execute('SELECT * FROM role').fetchall()
    return {'response': [{'title': role[1]} for role in roles]}


@app.get('/role{role_id}')
async def get_lang_by_id(role_id: int):
    role = cur.execute('SELECT * FROM role WHERE id = ?', (role_id,)).fetchone()
    if role is None:
        return {'error': 'Role is not exists', 'code': 50}
    return {'response': {'title': role[1]}}


@app.post('/task')
async def create_solution(task: Task):
    cur.execute('''
        INSERT INTO task (title, description, time, weight) VALUES (?, ?)
        ''', (task.title, task.description, task.time, task.weight))
    db.commit()
    return {'response': {
        'id': cur.lastrowid,
        'title': task.title,
        'time': task.time,
        'weight': task.weight
    }}


@app.get('/tasks')
async def get_all_solutions():
    solutions = cur.execute('SELECT * FROM task').fetchall()
    return {'response': [{
        'id': solution[0],
        'title': solution[1],
        'description': solution[2],
        'time': solution[3],
        'weight': solution[4],
    } for solution in solutions]}


@app.get('/task{task_id}')
async def get_solution_by_id(task_id: int):
    solution = cur.execute(
        'SELECT * FROM task WHERE id = ?', (task_id,)
    ).fetchone()
    if solution is None:
        return {'error': 'Task is not exists', 'code': 2}
    return {'response': {
        'id': task_id,
        'title': solution[1],
        'description': solution[2],
        'time': solution[3],
        'weight': solution[4],
    }}


@app.post('/mark')
async def create_mark(mark: Mark):
    cur.execute('''
        INSERT INTO mark (task_id, user_id, score, used_language) VALUES (?, ?, ?, ?)
        ''', (mark.task_id, mark.user_id, mark.score, mark.used_lang))
    db.commit()
    return {'response': {
        'id': cur.lastrowid,
        'task_id': mark.task_id,
        'user_id': mark.user_id,
        'score': mark.score,
        'used_lang': mark.used_lang
    }}


@app.get('/input{task_id}')
async def get_all_inputs(task_id: int):
    inputs = cur.execute('SELECT * FROM default_input WHERE task_id = ?', (task_id,)).fetchall()
    return {'response': [{'input': i[2], 'output': i[3]} for i in inputs if i[4]]}


@app.get('/mark{mark_id}')
async def get_mark_by_id(mark_id: int):
    mark = cur.execute('SELECT * FROM mark WHERE id = ?', (mark_id,)).fetchone()
    if mark is None:
        return {'error': 'Mark is not exists', 'code': 3}
    return {'response': {
        'id': mark[0],
        'task_id': mark[1],
        'user_id': mark[2],
        'score': mark[3],
        'used_lang': mark[4]
    }}


@app.get('/available{lang_id}')
async def get_available(lang_id: int):
    match lang_id:
        case Language.Python:
            return {'response': PythonCompiler.available}
        case Language.Java:
            return {'response': JavaCompiler.available}
        case Language.CSharp:
            return {'response': CSharpCompiler.available}
        case _:
            return {'error': 'Language is not exists', 'code': 50}


@app.put('/solution')
async def send_solution(solution: Solution):
    u = cur.execute('SELECT * FROM user WHERE access_token = ?', (solution.access_token,)).fetchone()
    task = cur.execute('SELECT * FROM task WHERE id = ?', (solution.task_id,)).fetchone()
    default_input = cur.execute('SELECT * FROM default_input WHERE task_id = ?', (solution.task_id,)).fetchall()
    if u is None:
        return {'response': {'error': 'User is not exists', 'code': 1}}
    mark = cur.execute(
        'SELECT * FROM mark WHERE task_id = ? and user_id = ?',
        (solution.task_id, u[0])
    ).fetchone()
    if mark is not None:
        return {'response': {'error': 'Mark is exists', 'code': 100}}
    filename = f'solutions/{solution.access_token}_{solution.task_id}'
    sw = SolutionWizard(filename, solution)

    input_data, output, hidden = (
                [i[2] for i in default_input],
                [i[3] for i in default_input],
                [i[4] for i in default_input]
    )

    match solution.lang:
        case Language.Python:
            result = await Maat.watch(
                sw, PythonCompiler, task[3], task[4], input_data, output, hidden
            )
        case Language.CSharp:
            result = await Maat.watch(
                sw, CSharpCompiler, task[3], task[4], input_data, output, hidden,
                file_ext='cs',
                class_name=True
            )
        case Language.Java:
            result = await Maat.watch(
                sw, JavaCompiler, task[3], task[4], input_data, output, hidden,
                file_ext='java',
                class_name=True
            )
        case _:
            return {
                'error': 'Unknown language',
                'code': 1000
            }
    if 'response' in result and result['response']['success']:
        score = (
            result['response']['success'] +
            (5 if result['response']['time'] <= task[3] else 0) +
            (5 if result['response']['weight'] <= task[4] else 0)
        )
        await create_mark(Mark(
            task_id=solution.task_id,
            user_id=u[0],
            score=score,
            used_lang=solution.lang
        ))
        result['response']['score'] = score
    return result


class ProactorServer(Server):
    def run(self, sockets=None):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
        asyncio.run(self.serve(sockets=sockets))


if __name__ == '__main__':
    config = Config(app="main:app", host="localhost", port=8000, reload=True)
    server = ProactorServer(config=config)
    server.run()
