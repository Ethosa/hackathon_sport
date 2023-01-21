# -*- coding: utf-8 -*-
import asyncio
from platform import system
from asyncio.subprocess import Process
from re import search

class OutputData:
    def __init__(self, stdout: str, stderr: str):
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self) -> str:
        return f'OutputData({self.stdout}, {self.stderr})'


class ABCCompiler:
    def __init__(
            self,
            filepath: str = ''
    ):
        self.filepath = filepath

    async def compile(
            self,
            input_data: bytes = None
    ) -> OutputData:
        raise NotImplementedError('You can not call compile method')

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
    async def compile(
            self,
            input_data: bytes = None
    ) -> OutputData:
        command = ""
        
        if (system == "Linux" or "Darwin"):
            command = "python3"
        else:
            command = "python"
        
        proc = await self.generate_proc(f'{command} {self.filepath}')
        if input_data:
            res = await proc.communicate(input_data)
            return OutputData(*res)
        return OutputData(*(await proc.communicate()))

    @staticmethod
    def forbidden(code: str) -> dict[str, any] | None:
        if search(r'(import\s+(?!math)|__import__|from\s+(?!math))', code):
            return {
                'error': 'import is forbidden (except of math)',
                'available_list': [
                    'math'
                ],
                'code': 200
            }
        elif search(r'open\s*\([\S\s]*\)', code):
            return {
                'error': 'Working with files is forbidden',
                'code': 401
            }


class JavaCompiler(ABCCompiler):
    async def precompile(self):
        proc = await self.generate_proc(
            f'javac {self.filepath} --release 8'
        )
        return OutputData(*(await proc.communicate()))

    async def compile(
            self,
            input_data: bytes = None
    ) -> OutputData:
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
            return {
                'error': 'import is forbidden.',
                'available_list': [
                    'java.util.Scanner', 'java.util.List', 'java.util.Random',
                    'java.util.Map', 'java.util.Set', 'java.util.ArrayList',
                    'java.util.HashMap', 'java.util.LinkedList'
                ],
                'code': 500
            }
        elif searched := search(r'(File|FileOutputStream|FileInputStream|InputStream|OutputStream)', code):
            return {
                'error': f'{searched.group(1)} class is forbidden',
                'code': 401
            }


class CSharpCompiler(ABCCompiler):
    async def precompile(self):
        proc = await self.generate_proc(
            f'cd {self.filepath.rsplit("/", 1)[0]} && '
            f'csc /t:exe /out:{self.filepath.rsplit("/", 1)[1].rsplit(".", 1)[0]}.exe '
            f'{self.filepath.rsplit("/", 1)[1]}'
        )
        return OutputData(*(await proc.communicate()))

    async def compile(
            self,
            input_data: bytes = None
    ) -> OutputData:
        proc = await self.generate_proc(
            f'cd {self.filepath.rsplit("/", 1)[0]} && {self.filepath.rsplit("/", 1)[1].rsplit(".", 1)[0]}.exe'
        )
        if input_data:
            res = await proc.communicate(input_data)
            return OutputData(*res)
        return OutputData(*(await proc.communicate()))

    @staticmethod
    def forbidden(code: str) -> dict[str, any] | None:
        if search(r'(\[[\S ()]+])', code):
            return {
                'error': 'Attributes is forbidden.',
                'available_list': [],
                'code': 300
            }
        elif searched := search(
                r'\b(FileInfo|File|Directory|DirectoryInfo|DriveInfo|FileStream|StreamReader|StreamWriter'
                r'|BinaryReader|BinaryWriter|ZipFile|DeflateStream|GZipStream)\b',
                code
        ):
            return {
                'error': f'{searched.group(1)} class is forbidden',
                'available_list': [],
                'code': 300
            }
        elif search(r'(using\s+(?!System))', code):
            return {
                'error': 'using is forbidden (except of System).',
                'available_list': [
                    'System'
                ],
                'code': 400
            }
