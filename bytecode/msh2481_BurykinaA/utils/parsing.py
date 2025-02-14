from dataclasses import dataclass
from enum import Enum

from utils.lexing import Lexer, TokenType


@dataclass
class Register:
    """Represents a register reference (r0-r15)"""

    number: int  # Register number (0-15)

    def __repr__(self):
        return f"r{self.number}"


@dataclass
class Literal:
    """Represents an immediate integer value"""

    value: int

    def __repr__(self):
        return str(self.value)


class Condition(Enum):
    """Represents a condition flag for jumps"""

    ZERO = "zero"
    POS = "pos"
    NEG = "neg"

    def __repr__(self):
        return self.value


# A value can be either a register reference or a literal
Value = Register | Literal


@dataclass
class Instruction:
    """Represents a single bytecode instruction"""

    opcode: TokenType
    args: list[Value | Literal | Condition]

    def __repr__(self):
        args_str = ", ".join(str(arg) for arg in self.args)
        return f"Instruction({self.opcode.name}, [{args_str}])"


def parse_value(lexer: Lexer) -> Value:
    """Parse a value (register or literal)"""
    token = lexer.next()

    if token.type == TokenType.REGISTER:
        assert isinstance(token.value, int)
        return Register(token.value)
    elif token.type == TokenType.NUMBER:
        assert isinstance(token.value, int)
        return Literal(token.value)
    else:
        raise Exception(f"Expected value, got {token}")


def parse_register(lexer: Lexer) -> Register:
    """Parse a register reference"""
    token = lexer.next()

    if token.type == TokenType.REGISTER:
        assert isinstance(token.value, int)
        return Register(token.value)
    else:
        raise Exception(f"Expected register, got {token}")


def parse_condition(lexer: Lexer) -> Condition:
    """Parse a condition flag"""
    token = lexer.next()

    if token.type == TokenType.CONDITION:
        assert isinstance(token.value, str)
        return Condition(token.value)
    else:
        raise Exception(f"Expected condition, got {token}")


def expect_comma(lexer: Lexer):
    """Consume a comma token or raise an error"""
    token = lexer.next()
    if token.type != TokenType.COMMA:
        raise Exception(f"Expected comma, got {token}")


def parse(lexer: Lexer) -> list[Instruction]:
    """Parse a sequence of instructions"""
    instructions: list[Instruction] = []

    while True:
        token = lexer.next()

        # Check for end of input
        if token.type == TokenType.EOF:
            break

        # Parse based on instruction type
        if token.type == TokenType.CP:
            # CP src, tgt
            src = parse_value(lexer)
            expect_comma(lexer)
            tgt = parse_register(lexer)
            instructions.append(Instruction(TokenType.CP, [src, tgt]))

        elif token.type == TokenType.LOAD:
            # LOAD memref, tgt
            addr = parse_value(lexer)  # memory address
            expect_comma(lexer)
            tgt = parse_register(lexer)
            instructions.append(Instruction(TokenType.LOAD, [addr, tgt]))

        elif token.type == TokenType.STORE:
            # STORE src, memref
            src = parse_value(lexer)
            expect_comma(lexer)
            addr = parse_value(lexer)  # memory address
            instructions.append(Instruction(TokenType.STORE, [src, addr]))

        elif token.type in {TokenType.ADD, TokenType.MUL, TokenType.SUB}:
            # ADD/MUL/SUB src, src, tgt
            src1 = parse_value(lexer)
            expect_comma(lexer)
            src2 = parse_value(lexer)
            expect_comma(lexer)
            tgt = parse_register(lexer)
            instructions.append(Instruction(token.type, [src1, src2, tgt]))

        elif token.type == TokenType.READ:
            # READ tgt
            tgt = parse_register(lexer)
            instructions.append(Instruction(TokenType.READ, [tgt]))

        elif token.type == TokenType.WRITE:
            # WRITE src
            src = parse_value(lexer)
            instructions.append(Instruction(TokenType.WRITE, [src]))

        elif token.type == TokenType.JUMP:
            # JUMP cond, src, addr
            cond = parse_condition(lexer)
            expect_comma(lexer)
            src = parse_value(lexer)
            expect_comma(lexer)
            addr = parse_value(lexer)

            instructions.append(Instruction(TokenType.JUMP, [cond, src, addr]))

        else:
            raise Exception(f"Unexpected token: {token}")

    return instructions
