# -*- coding: utf-8 -*-
import asyncio


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


class PythonCompiler(ABCCompiler):
    async def compile(
            self,
            input_data: bytes = None
    ) -> OutputData:
        proc = await asyncio.create_subprocess_shell(
            f'python {self.filepath}',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        if input_data:
            res = await proc.communicate(input_data)
            return OutputData(*res)
        return OutputData(*(await proc.communicate()))


class JavaCompiler(ABCCompiler):
    async def precompile(self, filepath):
        proc = await asyncio.create_subprocess_shell(
            f'javac {filepath} --release 8',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        return OutputData(*(await proc.communicate()))

    async def compile(
            self,
            input_data: bytes = None
    ) -> OutputData:
        proc = await asyncio.create_subprocess_shell(
            f'cd {self.filepath.rsplit("/", 1)[0]} && java {self.filepath.rsplit("/", 1)[1]}',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        if input_data:
            res = await proc.communicate(input_data)
            return OutputData(*res)
        return OutputData(*(await proc.communicate()))


class CSharpCompiler(ABCCompiler):
    async def precompile(self, filepath):
        proc = await asyncio.create_subprocess_shell(
            f'cd {self.filepath.rsplit("/", 1)[0]} && '
            f'csc /t:exe /out:{filepath.rsplit("/", 1)[1].rsplit(".", 1)[0]}.exe {filepath.rsplit("/", 1)[1]}',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        return OutputData(*(await proc.communicate()))

    async def compile(
            self,
            input_data: bytes = None
    ) -> OutputData:
        proc = await asyncio.create_subprocess_shell(
            f'cd {self.filepath.rsplit("/", 1)[0]} && {self.filepath.rsplit("/", 1)[1]}.exe',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        if input_data:
            res = await proc.communicate(input_data)
            return OutputData(*res)
        return OutputData(*(await proc.communicate()))
