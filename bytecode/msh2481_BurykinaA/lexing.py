import re
from dataclasses import dataclass
from enum import auto, Enum
from typing import Callable, List, Optional, Pattern, Tuple


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
    value: Optional[str | int] = None

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
        self.rules: List[Tuple[Pattern, Callable[[str], Token]]] = [
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
            f"Invalid character: {self.current_char} at position {self.pos}"
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
