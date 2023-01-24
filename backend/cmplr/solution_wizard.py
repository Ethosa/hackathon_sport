# -*- coding: utf-8 -*-
from re import findall
from os import path, getcwd, mkdir
from typing import Type
from time import time

from models import Solution
from . import ABCCompiler


class SolutionWizard:
    def __init__(
            self,
            filename: str,
            solution: Solution
    ):
        self.filename = filename
        self.solution = solution

    async def check_solution(
            self,
            compiler_type: Type[ABCCompiler],
            max_time: int,
            weight: int,
            input_data: bytes | None = None,
            file_ext: str = 'py',
            need_class_name: bool = False,
    ):
        class_name = findall(r'class\s+(\S+)\s*{', self.solution.code)
        if class_name:
            class_name = class_name[0]
        # Normalize path and creates user directory
        script_name = class_name if need_class_name and class_name else 'script'
        p = path.normpath(getcwd() + f'/{self.filename}/{script_name}.{file_ext}').replace('\\', '/')
        if not path.exists(self.filename):
            mkdir(self.filename)
        # Initialize compiler
        compiler = compiler_type(p)
        # Check forbidden things
        if forbidden := compiler.forbidden(self.solution.code):
            return forbidden
        # Save code into file
        with open(p, 'w', encoding='utf-8') as f:
            f.write(self.solution.code)
        compile_result = await compiler.compile()
        now = time()
        run_result = await compiler.run(input_data)
        now = time() - now
        return {'response': {
            'compile': {'stdout': compile_result.stdout, 'stderr': compile_result.stderr},
            'run': {'stdout': run_result.stdout, 'stderr': run_result.stderr},
            'time': now,
            'weight': path.getsize(p)
        }}

