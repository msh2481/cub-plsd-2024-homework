import sys
from utils.lexing import Lexer
from utils.parsing import parse
from utils.vm import VM


def load_program(filename: str) -> str:
    """Load program text from a file"""
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m bytecode.msh2481_BurykinaA.main <program_file>")
        sys.exit(1)

    program_text = load_program(sys.argv[1])

    try:
        lexer = Lexer(program_text)
        program = parse(lexer)

        vm = VM(program)
        vm.run()

    except Exception as e:
        print(f"Error executing program: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 