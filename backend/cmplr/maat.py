# -*- coding: utf-8 -*-
from typing import Type

from . import ABCCompiler, OutputData
from .solution_wizard import SolutionWizard


class Maat:
    @staticmethod
    async def watch(
            sw: SolutionWizard,
            compiler: Type[ABCCompiler],
            max_time: int,
            weight: int,
            input_data: list[str] | None = None,
            output: list[str] | None = None,
            hidden_layers: list[bool] | None = None,
            file_ext: str = 'py',
            class_name: bool = False
    ) -> OutputData:
        """Checks user's solution

        :param sw: SolutionWizard
        :param compiler: Compiler class
        :param input_data: list of input data
        :param output: list of output data
        :param hidden_layers: list of hidden
        :param file_ext: solution file extension
        :param class_name: need to name file as solution code class
        """
        success = 0
        errors = 0
        max_success = len(output) if output else 0
        res = []
        print(input_data)
        print(output)
        print(hidden_layers)

        time = 2e9
        weight = 0

        if input_data:
            for i in range(len(input_data)):
                inp = input_data[i]
                out = output[i] if output else None
                is_hidden = hidden_layers[i] if hidden_layers else None
                result = await sw.check_solution(
                    compiler, max_time, weight, inp.encode(), file_ext, class_name
                )
                print(result)
                result = result['response']
                weight = result['weight']
                del result['weight']
                time = min(time, result['time'])
                del result['time']
                if 'error' in result:
                    return result
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
            'compile_result': res,
            'time': round(time * 1000),
            'weight': weight,
            'score': 0
        }}
