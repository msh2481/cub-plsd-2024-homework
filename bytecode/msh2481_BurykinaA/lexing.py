import re
from dataclasses import dataclass
from enum import auto, Enum
from typing import Callable, Pattern


class TokenType(Enum):
    # Instructions
    CP = auto()
    LOAD = auto()
    STORE = auto()
    ADD = auto()
    MUL = auto()
    SUB = auto()
    READ = auto()
    WRITE = auto()
    JUMP = auto()
    # Registers
    REGISTER = auto()
    # Values
    NUMBER = auto()
    # Conditions
    CONDITION = auto()
    # Separators
    COMMA = auto()
    # End of input
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str | int | None = None

    def __repr__(self):
        if self.value is not None:
            return f"Token({self.type}, {self.value})"
        return f"Token({self.type})"


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None

        # Define regex patterns for different token types
        self.rules: list[tuple[Pattern, Callable[[str], Token]]] = [
            # Comments - skip
            (re.compile(r"#[^\n]*"), lambda _: None),
            # Whitespace - skip
            (re.compile(r"[ \t\n]+"), lambda _: None),
            # Instructions
            (re.compile(r"CP\b"), lambda _: Token(TokenType.CP)),
            (re.compile(r"LOAD\b"), lambda _: Token(TokenType.LOAD)),
            (re.compile(r"STORE\b"), lambda _: Token(TokenType.STORE)),
            (re.compile(r"ADD\b"), lambda _: Token(TokenType.ADD)),
            (re.compile(r"MUL\b"), lambda _: Token(TokenType.MUL)),
            (re.compile(r"SUB\b"), lambda _: Token(TokenType.SUB)),
            (re.compile(r"READ\b"), lambda _: Token(TokenType.READ)),
            (re.compile(r"WRITE\b"), lambda _: Token(TokenType.WRITE)),
            (re.compile(r"JUMP\b"), lambda _: Token(TokenType.JUMP)),
            # Registers (r0 through r15)
            (
                re.compile(r"r(1[0-5]|[0-9])\b"),
                lambda m: Token(TokenType.REGISTER, int(m.group(1))),
            ),
            # Numbers
            (re.compile(r"-?\d+"), lambda m: Token(TokenType.NUMBER, int(m.group()))),
            # Conditions
            (
                re.compile(r"(zero|pos|neg)\b"),
                lambda m: Token(TokenType.CONDITION, m.group()),
            ),
            # Comma separator
            (re.compile(r","), lambda _: Token(TokenType.COMMA)),
        ]

    def error(self):
        raise Exception(
            f"Invalid character: {self.current_char} ({ord(self.current_char)}) at position {self.pos}"
        )

    def next(self) -> Token:
        """Return the next token in the input."""
        # Return EOF if we've reached the end
        if self.pos >= len(self.text):
            return Token(TokenType.EOF)

        # Try each rule
        for pattern, token_func in self.rules:
            match = pattern.match(self.text, self.pos)
            if match:
                # Update position
                self.pos = match.end()
                # Generate token
                token = token_func(match)
                # Skip None tokens (like whitespace)
                if token is None:
                    return self.next()
                return token

        self.error()

    def peek(self) -> Token:
        """Look at the next token without consuming it."""
        # Save current position
        saved_pos = self.pos
        # Get next token
        token = self.next()
        # Restore position
        self.pos = saved_pos
        return token


def test_lexing_1():
    """Test basic instruction recognition"""
    print("\n=== Test 1: Basic Instructions ===")
    text = "CP LOAD STORE ADD MUL SUB READ WRITE JUMP"
    lexer = Lexer(text)

    while True:
        token = lexer.next()
        print(token)
        if token.type == TokenType.EOF:
            break


def test_lexing_2():
    """Test register recognition"""
    print("\n=== Test 2: Registers ===")
    text = "r0 r1 r9 r10 r15"
    lexer = Lexer(text)

    while True:
        token = lexer.next()
        print(token)
        if token.type == TokenType.EOF:
            break


def test_lexing_3():
    """Test numbers and negative numbers"""
    print("\n=== Test 3: Numbers ===")
    text = "42 -17 0 -0 999"
    lexer = Lexer(text)

    while True:
        token = lexer.next()
        print(token)
        if token.type == TokenType.EOF:
            break


def test_lexing_4():
    """Test conditions"""
    print("\n=== Test 4: Conditions ===")
    text = "zero pos neg"
    lexer = Lexer(text)

    while True:
        token = lexer.next()
        print(token)
        if token.type == TokenType.EOF:
            break


def test_lexing_5():
    """Test whitespace handling including newlines"""
    print("\n=== Test 5: Whitespace Handling ===")
    text = """LOAD r1,
    STORE r2,
    ADD r3"""  # Note the newlines and spaces
    lexer = Lexer(text)

    while True:
        token = lexer.next()
        print(token)
        if token.type == TokenType.EOF:
            break


def test_lexing_6():
    """Test complex instruction with multiple components"""
    print("\n=== Test 6: Complex Instruction ===")
    text = "LOAD r1, -42\nJUMP zero, r15"
    lexer = Lexer(text)

    while True:
        token = lexer.next()
        print(token)
        if token.type == TokenType.EOF:
            break


def test_lexing_7():
    """Test peek functionality"""
    print("\n=== Test 7: Peek Testing ===")
    text = "ADD r1, r2"
    lexer = Lexer(text)

    print("Peeked token:", lexer.peek())
    print("Next token:", lexer.next())
    print("Peeked token:", lexer.peek())
    print("Next token:", lexer.next())


def test_lexing_8():
    """Test comment handling"""
    print("\n=== Test 8: Comments ===")
    text = """LOAD r1, 42  # Load value into r1
    STORE r2, r1 # Store it in memory
    # This is a full-line comment
    ADD r1, r2, r3#No space before comment
    """
    lexer = Lexer(text)

    while True:
        token = lexer.next()
        print(token)
        if token.type == TokenType.EOF:
            break


if __name__ == "__main__":
    test_lexing_1()
    test_lexing_2()
    test_lexing_3()
    test_lexing_4()
    test_lexing_5()
    test_lexing_6()
    test_lexing_7()
    test_lexing_8()
