# -*- coding: utf-8 -*-
import asyncio
import os

from asyncio.subprocess import Process
from re import search


class OutputData:
    def __init__(self, stdout: bytes, stderr: bytes, encoding: str = 'utf-8'):
        self.stdout: str = stdout.decode(encoding)
        self.stderr: str = stderr.decode(encoding)

    def __str__(self) -> str:
        return f'OutputData({self.stdout}, {self.stderr})'


class ABCCompiler:
    def __init__(
            self,
            filepath: str = ''
    ):
        self.filepath = filepath

    async def compile(
            self
    ) -> OutputData:
        raise NotImplementedError('You can not call compile method')

    async def run(
            self,
            input_data: bytes = None
    ) -> OutputData:
        raise NotImplementedError('You can not call run method')

    @staticmethod
    def forbidden(code: str) -> dict[str, any] | None:
        return None

    @staticmethod
    async def generate_proc(command: str) -> Process:
        return await asyncio.create_subprocess_shell(
            command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )


class PythonCompiler(ABCCompiler):
    async def compile(self) -> OutputData:
        return OutputData(b'', b'')

    async def run(
            self,
            input_data: bytes = None
    ) -> OutputData:
        command = 'python' if os.name in ['win32', 'nt'] else 'python3'

        proc = await self.generate_proc(f'{command} {self.filepath}')
        if input_data:
            res = await proc.communicate(input_data)
            return OutputData(*res)
        return OutputData(*(await proc.communicate()))

    @staticmethod
    def forbidden(code: str) -> dict[str, any] | None:
        if search(r'(\nimport\s+(?!(math|random))|__import__)', code):
            return {'response': {
                'error': 'import is forbidden',
                'available_list': [
                    'math',
                    'random'
                ],
                'code': 200
            }}
        elif search(r'from\s+(?!(math|random)\s+import)', code):
            return {'response': {
                'error': 'import is forbidden',
                'available_list': [
                    'math',
                    'random'
                ],
                'code': 200
            }}
        elif search(r'open\s*\([\S\s]*\)', code):
            return {'response': {
                'error': 'Working with files is forbidden',
                'code': 401
            }}


class JavaCompiler(ABCCompiler):
    async def compile(self) -> OutputData:
        flags = '--release 8' if os.name in ['nt', 'win32'] else ''
        proc = await self.generate_proc(
            f'javac {self.filepath} {flags}'
        )
        return OutputData(*(await proc.communicate()))

    async def run(
            self,
            input_data: bytes = None
    ) -> OutputData:
        print(
            f'cd {self.filepath.rsplit("/", 1)[0]} && java {self.filepath.rsplit("/", 1)[1].rsplit(".", 1)[0]}')
        proc = await self.generate_proc(
            f'cd {self.filepath.rsplit("/", 1)[0]} && java {self.filepath.rsplit("/", 1)[1].rsplit(".", 1)[0]}'
        )
        if input_data:
            res = await proc.communicate(input_data)
            return OutputData(*res)
        return OutputData(*(await proc.communicate()))

    @staticmethod
    def forbidden(code: str) -> dict[str, any] | None:
        if search(
                r'(import\s+(?!java\.util\.(Scanner|List|Random|LinkedList|Map|HashMap|ArrayList|Set)))',
                code
        ):
            return {'response': {
                'error': 'import is forbidden.',
                'available_list': [
                    'java.util.Scanner', 'java.util.List', 'java.util.Random',
                    'java.util.Map', 'java.util.Set', 'java.util.ArrayList',
                    'java.util.HashMap', 'java.util.LinkedList'
                ],
                'code': 500
            }}
        elif searched := search(r'(File|FileOutputStream|FileInputStream|InputStream|OutputStream)', code):
            return {'response': {
                'error': f'{searched.group(1)} class is forbidden',
                'code': 401
            }}


class CSharpCompiler(ABCCompiler):
    async def compile(self) -> OutputData:
        cmd = (
            f'csc /t:exe /out:{self.filepath.rsplit("/", 1)[1].rsplit(".", 1)[0]}.exe {self.filepath.rsplit("/", 1)[1]}'
            if os.name in ['nt', 'win32'] else
            f'mcs -out:{self.filepath.rsplit("/", 1)[1].rsplit(".", 1)[0]}.exe {self.filepath.rsplit("/", 1)[1]}'
        )
        proc = await self.generate_proc(
            f'cd {self.filepath.rsplit("/", 1)[0]} && {cmd}'
        )
        return OutputData(*(await proc.communicate()), 'cp866')

    async def run(
            self,
            input_data: bytes = None
    ) -> OutputData:
        cmd = (
            f'{self.filepath.rsplit("/", 1)[1].rsplit(".", 1)[0]}.exe'
            if os.name in ['nt', 'win32'] else
            f'mono {self.filepath.rsplit("/", 1)[1].rsplit(".", 1)[0]}.exe'
        )
        proc = await self.generate_proc(
            f'cd {self.filepath.rsplit("/", 1)[0]} && {cmd}'
        )
        if input_data:
            res = await proc.communicate(input_data)
            return OutputData(*res)
        return OutputData(*(await proc.communicate()), 'cp866')

    @staticmethod
    def forbidden(code: str) -> dict[str, any] | None:
        if search(r'(\[[\S ()]+])', code):
            return {'response': {
                'error': 'Attributes is forbidden.',
                'available_list': [],
                'code': 300
            }}
        elif searched := search(
                r'\b(FileInfo|File|Directory|DirectoryInfo|DriveInfo|FileStream|StreamReader|StreamWriter'
                r'|BinaryReader|BinaryWriter|ZipFile|DeflateStream|GZipStream)\b',
                code
        ):
            return {'response': {
                'error': f'{searched.group(1)} class is forbidden',
                'available_list': [],
                'code': 300
            }}
        elif search(r'(using\s+(?!System))', code):
            return {'response': {
                'error': 'using is forbidden (except of System).',
                'available_list': [
                    'System'
                ],
                'code': 400
            }}
