from dataclasses import dataclass
from enum import auto, Enum
from typing import Union

from lexing import Lexer, Token, TokenType


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


def test_parsing_1():
    """Test parsing a simple arithmetic program"""
    program = """
    CP 42, r1      # Load constant 42 into r1
    CP r1, r2      # Copy r1 to r2
    ADD r1, r2, r3 # Add r1 and r2, store in r3
    MUL 2, r3, r4  # Multiply r3 by 2, store in r4
    WRITE r4       # Output result
    """

    lexer = Lexer(program)
    instructions = parse(lexer)
    print("\nTest 1 - Arithmetic:")
    print("Input program:")
    print(program)
    print("Parsed instructions:")
    for inst in instructions:
        print(inst)


def test_parsing_2():
    """Test parsing a program with jumps and I/O"""
    program = """
    READ r1        # Read input into r1
    JUMP zero, r1, 42  # If r1 is zero, jump to address 42
    STORE r1, 100  # Store r1 at memory address 100
    LOAD 100, r2   # Load from address 100 into r2
    SUB r2, r1, r3 # Subtract r1 from r2, store in r3
    WRITE r3       # Output result
    """

    lexer = Lexer(program)
    instructions = parse(lexer)
    print("\nTest 2 - Control Flow and I/O:")
    print("Input program:")
    print(program)
    print("Parsed instructions:")
    for inst in instructions:
        print(inst)


if __name__ == "__main__":
    test_parsing_1()
    test_parsing_2()
