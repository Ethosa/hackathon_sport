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
            hidden_layers: list[bool] | None = None,
            file_ext: str = 'py',
            class_name: bool = False
    ) -> OutputData:
        success = 0
        errors = 0
        max_success = len(output) if output else 0
        res = []
        print(input_data)
        print(output)
        print(hidden_layers)

        if input_data:
            for i in range(len(input_data)):
                inp = input_data[i]
                out = output[i] if output else None
                is_hidden = hidden_layers[i] if hidden_layers else None
                result = await sw.check_solution(compiler, inp.encode(), file_ext, class_name)
                print(result)
                if 'error' in result:
                    return result
                result = result['response']
                if result['run']['stderr'] or result['compile']['stderr']:
                    errors += 1
                    if not is_hidden:
                        result['input'] = inp
                        result['output'] = out
                        res.append(result)
                elif result['run']['stdout'] or result['compile']['stdout'] and out:
                    if result['run']['stdout'].replace('\r', '') in [out, out + '\n']:
                        success += 1
                    else:
                        errors += 1
                    if not is_hidden:
                        result['input'] = inp
                        result['output'] = out
                        res.append(result)
        return {'response': {
            'success': success,
            'errors': errors,
            'max_success': max_success,
            'compile_result': [res]
        }}
