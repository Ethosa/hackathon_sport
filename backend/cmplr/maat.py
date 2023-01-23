# -*- coding: utf-8 -*-
from typing import Type

from . import ABCCompiler, OutputData
from .solution_wizard import SolutionWizard


class Maat:
    async def watch(
            self,
            sw: SolutionWizard,
            compiler: Type[ABCCompiler],
            input_data: list[str] | None = None,
            output: list[str] | None = None,
            file_ext: str = 'py',
            class_name: bool = False
    ) -> OutputData:
        success = 0
        errors = 0
        max_success = len(output) if output else 0
        res = {
            'compile': {'stdout': '', 'stderr': ''},
            'run': {'stdout': '', 'stderr': ''},
        }

        if input_data:
            for i in range(len(input_data)):
                inp = input_data[i]
                out = output[i] if output else None
                result = await sw.check_solution(compiler, inp.encode(), file_ext, class_name)
                print(result)
                if 'error' in result:
                    return result
                result = result['response']
                if result['run']['stderr'] or result['compile']['stderr']:
                    errors += 1
                    res['run']['stderr'] += '\n' + result['run']['stderr']
                    res['compile']['stderr'] += '\n' + result['compile']['stderr']
                elif result['run']['stdout'] or result['compile']['stdout']:
                    if out and result['run']['stdout'] == out:
                        success += 1
        return {'response': {
            'success': success,
            'errors': errors,
            'max_success': max_success,
            'compile_result': res
        }}
