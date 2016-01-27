from __future__ import unicode_literals

import dis
from types import CodeType

from bytecode_magic.instruction import Instruction


def strip_calls(fn_name, func=None):
    """Filter all calls to the specified function name.

    The given function will be modified in place.

    This can be used as a decorator. For example, the following usages are
    identical:

    .. code:: python

       @strip_calls('f')
       def foo():
           f()

       def bar():
           f()

       strip_calls('f', bar)

    Args:
        fn_name (unicode):
            The function name for which calls are to be stripped.

        func (callable):
            An optional function. If this argument is not provided, a decorator
            is returned.

    Returns:
        callable:
        If ``func`` is provided, then the function will be returned with calls
        to ``func_name`` stripped. Otherwise, a decorator will be returned that
        filters calls to ``func_name`` on the decorated function.
    """
    def decorator(func):
        func_code = func.func_code

        try:
            fn_index = func_code.co_names.index(fn_name)
        except ValueError:
            # fn_name is not called in func.
            return func

        fn_load_instruction = Instruction(dis.opmap['LOAD_GLOBAL'], fn_index)
        pop_top_instruction = Instruction(dis.opmap['POP_TOP'])
        instructions = []
        include = True

        for instruction in Instruction.from_code(func_code.co_code):
            if instruction == fn_load_instruction:
                include = False
            elif not include and instruction == pop_top_instruction:
                include = True
            elif include:
                instructions.append(instruction)

        func.func_code = CodeType(func_code.co_argcount,
                                  func_code.co_nlocals,
                                  func_code.co_stacksize,
                                  func_code.co_flags,
                                  Instruction.to_code(instructions),
                                  func_code.co_consts,
                                  func_code.co_names,
                                  func_code.co_varnames,
                                  func_code.co_filename,
                                  func_code.co_name,
                                  func_code.co_firstlineno,
                                  func_code.co_lnotab,
                                  func_code.co_freevars,
                                  func_code.co_cellvars)

        return func

    if func:
        return decorator(func)

    return decorator
