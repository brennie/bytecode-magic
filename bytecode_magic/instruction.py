from __future__ import unicode_literals

import dis


def has_argument(opcode):
    """Return whether or not the opcode has an argument.

    Args:
        opcode (int):
            The opcode.

    Returns:
        bool:
        Whether or not the opcode has an argument.
    """
    return opcode >= dis.HAVE_ARGUMENT


class Instruction(object):
    """A representation of a Python bytecode instruction.

    The instruction represented by this object may be two instructions, in the
    case of the :py:data:`~dis.EXTENDED_ARG` instruction, which provides an
    extra two bytes for the following opcode's argument.
    """

    EXTENDED_ARG_MIN = 65536

    def __init__(self, opcode, argument=None):
        """Initialize a new Instruction.

        Args
            opcode (int):
                The integer opcode.

            argument (int):
                An optional argument.
        """
        self.opcode = opcode
        self.argument = argument

    @property
    def has_argument(self):
        """Whether or not the instruction has an argument.

        Returns:
            bool:
            Whether or not the instruction has an argument.
        """
        return self.argument is not None

    @property
    def has_extended_argument(self):
        """Whether or not the instruction has an extended argument.

        Returns:
            bool:
            Whether or not the instruction has an argument.
        """
        return self.has_argument and self.argument >= self.EXTENDED_ARG_MIN

    @property
    def as_bytes(self):
        """The instruction encoded to bytes.

        Returns:
            bytes:
            The encoded instruction.
        """
        code = []

        if self.has_argument:
            arg_bytes = (self.argument & 0xFF,
                         (self.argument >> 8) & 0xFF,
                         (self.argument >> 16) & 0xFF,
                         (self.argument >> 24) & 0xFF)

            if self.has_extended_argument:
                code.append(dis.EXTENDED_ARG)
                code.extend(arg_bytes[2:])

        code.append(self.opcode)

        if self.has_argument:
            code.extend(arg_bytes[:2])

        return b''.join(chr(byte) for byte in code)

    @staticmethod
    def to_code(instructions):
        """Encode the instructions to bytes.

        Args:
            instructions (list):
                A list of :py:class:`Instruction`s to encode.

        Returns:
            bytes:
            The instructions encoded as bytes.
        """
        return b''.join(
            instruction.as_bytes
            for instruction in instructions
        )

    @classmethod
    def from_code(cls, code):
        """Parse instructions from the given sequence of bytes.

        Python instructions follow the following format, presented in EBNF::

            <instruction> ::= <simple-opcode> | <opcode-with-arg> <byte> <byte>
            <simple-opcode> ::= 0 | 1 | ... | 89
            <opcode-with-arg> :=
                <extended-arg> <byte> <byte> <extended-opcode> <byte> <byte> |
                <extended-opcode> <byte> <byte>
            <extended-arg> ::= 145
            <extended-opcode> ::= 90 | 91 | ... | 144 | 146 | 147

        The bytes immediately following ``<extended-arg>`` are the most
        significant two bytes of the argument in little endian encoding.
        Likewise, the bytes immediately following ``<extended-opcode>`` are the
        least significant two bytes of the argument (in little endian
        encoding).

        Args:
            code (bytes):
                The instructions.

        Returns:
            list:
            A list of py:class:`Instructions` parsed from the instructions.
        """
        instructions = []
        i = 0

        while i < len(code):
            opcode = ord(code[i])
            i += 1

            if has_argument(opcode):
                arg = (ord(code[i + 1]) << 8) + ord(code[i])
                i += 2

                if opcode == dis.EXTENDED_ARG:
                    opcode = ord(code[i])
                    arg = ((arg << 16) +
                           (ord(code[i + 2]) << 8) +
                           (ord(code[i + 1])))
                    i += 3

                print '%x' % arg
            else:
                arg = None

            instructions.append(Instruction(opcode, arg))

        return instructions

    def __len__(self):
        """Return the length of the instruction in bytes.

        Returns:
            int:
            The length of the instruction in bytes.
        """
        size = 1  # 1 byte per opcode.

        if self.has_argument:
            size += 2  # 2 bytes for an argument.

            if self.has_extended_argument:
                # 1 byte for the EXTENDED_ARG opcode and 2 for its argument.
                size += 3

        return size

    def __repr__(self):
        """Return a representation of the instruction.

        Returns:
            unicode:
            A representation of the instruction.
        """
        if self.argument is not None:
            arg = ', argument=%d' % self.argument
        else:
            arg = ''

        return '<Instruction(opcode=%s%s)>' % (dis.opname[self.opcode], arg)

    def __eq__(self, other):
        """Compare two instructions for equality.

        Two instructions are equal if they have the same opcode and argument.

        Args:
            other (Instruction):
                The instruction to compare this one to.

        Returns:
            bool:
            Whether or not the instructions are equal.
        """
        return (isinstance(other, type(self)) and
                self.opcode == other.opcode and
                self.argument == other.argument)
