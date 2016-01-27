from __future__ import unicode_literals

import dis
from unittest import TestCase

from bytecode_magic.decorators import strip_calls
from bytecode_magic.instruction import Instruction


class InstructionTests(TestCase):
    """Tests for bytecode_magic.instruction."""

    def test_argument_parsing_serialization(self):
        """Testing Instruction.from_code argument parsing and serialization"""
        bytecode = b'%c\x01\x02' % dis.opmap['STORE_FAST']
        instructions = Instruction.from_code(bytecode)

        self.assertEqual(len(instructions), 1)

        instruction = instructions[0]
        self.assertEqual(Instruction(dis.opmap['STORE_FAST'], 0x0201),
                         instruction)
        self.assertEqual(instruction.as_bytes, bytecode)

    def test_extended_argument_parsing_serialization(self):
        """Testing Instruction.from_code argument parsing and serialization of
        extended arguments
        """
        bytecode = (b'%c\x03\x04%c\x01\x02'
                    % (dis.EXTENDED_ARG, dis.opmap['STORE_FAST']))

        instructions = Instruction.from_code(bytecode)

        self.assertEqual(len(instructions), 1)

        instruction = instructions[0]
        self.assertEqual(Instruction(dis.opmap['STORE_FAST'], 0x04030201),
                         instruction)
        self.assertEqual(instruction.as_bytes, bytecode)


class DecoratorTests(TestCase):
    """Tests for bytecode_magic.decorators"""

    def test_strip_calls(self):
        """Testing @strip_calls"""
        @strip_calls('a')
        def foo():
            a()
        
        def bar():
            return None

        self.assertEqual(foo.func_code.co_code, bar.func_code.co_code)

    def test_strip_calls_uncalled(self):
        """Testing @strip_calls doesn't modify functions that do not call"""
        def foo():
            return None

        orig_func_code = foo.func_code
        strip_calls('a', foo)

        self.assertIs(orig_func_code, foo.func_code)

    def test_strip_calls_multiple(self):
        """Testing @strip_calls stripping multiple functions"""
        @strip_calls('a')
        @strip_calls('b')
        def foo():
            a()
            b()

        def bar():
            return None

        self.assertEqual(foo.func_code.co_code, bar.func_code.co_code)

    def test_strip_calls_nested(self):
        """Testing @strip_calls stripping nested function calls"""
        @strip_calls('a')
        def foo():
            a(b(), c(), d(), e())

        def bar():
            return None

        self.assertEqual(foo.func_code.co_code, bar.func_code.co_code)


