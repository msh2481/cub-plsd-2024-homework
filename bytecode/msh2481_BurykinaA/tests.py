from utils.lexing import Lexer, Token, TokenType
from utils.parsing import parse, Instruction, Register, Literal, Condition
from utils.vm import VM
import sys
from io import StringIO


def test_lexer():
    """Test the lexer functionality"""
    # Test basic instruction recognition
    lexer = Lexer("CP LOAD STORE ADD MUL SUB READ WRITE JUMP")
    expected_types = [
        TokenType.CP, TokenType.LOAD, TokenType.STORE, TokenType.ADD,
        TokenType.MUL, TokenType.SUB, TokenType.READ, TokenType.WRITE,
        TokenType.JUMP, TokenType.EOF
    ]
    for expected_type in expected_types:
        assert lexer.next().type == expected_type

    # Test register recognition
    lexer = Lexer("r0 r1 r9 r10 r15")
    for i in [0, 1, 9, 10, 15]:
        token = lexer.next()
        assert token.type == TokenType.REGISTER
        assert token.value == i

    # Test numbers and negative numbers
    lexer = Lexer("42 -17 0 999")
    expected_numbers = [42, -17, 0, 999]
    for num in expected_numbers:
        token = lexer.next()
        assert token.type == TokenType.NUMBER
        assert token.value == num

    # Test conditions
    lexer = Lexer("zero pos neg")
    expected_conditions = ["zero", "pos", "neg"]
    for cond in expected_conditions:
        token = lexer.next()
        assert token.type == TokenType.CONDITION
        assert token.value == cond

    # Test complex instruction with comments
    lexer = Lexer("LOAD r1, -42 # This is a comment\nJUMP zero, r15")
    expected_tokens = [
        (TokenType.LOAD, None),
        (TokenType.REGISTER, 1),
        (TokenType.COMMA, None),
        (TokenType.NUMBER, -42),
        (TokenType.JUMP, None),
        (TokenType.CONDITION, "zero"),
        (TokenType.COMMA, None),
        (TokenType.REGISTER, 15),
        (TokenType.EOF, None)
    ]
    for exp_type, exp_value in expected_tokens:
        token = lexer.next()
        assert token.type == exp_type
        if exp_value is not None:
            assert token.value == exp_value


def test_parser():
    """Test the parser functionality"""
    # Test arithmetic instruction parsing
    program = """
    CP 42, r1
    ADD r1, r2, r3
    MUL 2, r3, r4
    SUB r4, r1, r5
    """
    lexer = Lexer(program)
    instructions = parse(lexer)
    
    assert len(instructions) == 4
    assert instructions[0].opcode == TokenType.CP
    assert isinstance(instructions[0].args[0], Literal)
    assert instructions[0].args[0].value == 42
    
    # Test memory operations parsing
    program = """
    STORE r1, 100
    LOAD 100, r2
    """
    lexer = Lexer(program)
    instructions = parse(lexer)
    
    assert len(instructions) == 2
    assert instructions[0].opcode == TokenType.STORE
    assert isinstance(instructions[0].args[1], Literal)
    assert instructions[0].args[1].value == 100

    # Test jump instruction parsing
    program = "JUMP zero, r1, 42"
    lexer = Lexer(program)
    instructions = parse(lexer)
    
    assert len(instructions) == 1
    assert instructions[0].opcode == TokenType.JUMP
    assert isinstance(instructions[0].args[0], Condition)
    assert instructions[0].args[0] == Condition.ZERO


def test_arithmetic():
    """Test basic arithmetic operations in VM"""
    program_text = """
    CP 42, r1      # Load constant 42 into r1
    CP r1, r2      # Copy r1 to r2
    ADD r1, r2, r3 # Add r1 and r2, store in r3 (42 + 42 = 84)
    MUL 2, r3, r4  # Multiply r3 by 2, store in r4 (84 * 2 = 168)
    SUB r4, r1, r5 # Subtract r1 from r4, store in r5 (168 - 42 = 126)
    """
    
    lexer = Lexer(program_text)
    program = parse(lexer)
    vm = VM(program)
    vm.run()
    
    assert vm.registers[1] == 42, "r1 should be 42"
    assert vm.registers[2] == 42, "r2 should be 42"
    assert vm.registers[3] == 84, "r3 should be 84"
    assert vm.registers[4] == 168, "r4 should be 168"
    assert vm.registers[5] == 126, "r5 should be 126"


def test_memory():
    """Test memory operations (LOAD/STORE)"""
    program_text = """
    CP 123, r1     # Load 123 into r1
    STORE r1, 100  # Store r1 at memory address 100
    LOAD 100, r2   # Load from address 100 into r2
    """
    
    lexer = Lexer(program_text)
    program = parse(lexer)
    vm = VM(program)
    vm.run()
    
    assert vm.registers[1] == 123, "r1 should be 123"
    assert vm.registers[2] == 123, "r2 should be 123"
    assert vm.memory[100] == 123, "Memory at 100 should be 123"


def test_jumps():
    """Test conditional jumps"""
    program_text = """
    CP 0, r1       # Load 0 into r1
    CP 42, r2      # Load 42 into r2
    JUMP zero, r1, 5  # Should jump to instruction 5 (r1 is zero)
    CP 99, r3      # This should be skipped
    CP 100, r3     # This should be skipped
    CP 1, r3       # This should execute (instruction 5)
    JUMP pos, r2, 9   # Should jump to instruction 9 (r2 is positive)
    CP 200, r4     # This should be skipped
    CP 201, r4     # This should be skipped
    CP 2, r4       # This should execute (instruction 9)
    """
    
    lexer = Lexer(program_text)
    program = parse(lexer)
    vm = VM(program)
    vm.run()
    
    assert vm.registers[1] == 0, "r1 should be 0"
    assert vm.registers[2] == 42, "r2 should be 42"
    assert vm.registers[3] == 1, "r3 should be 1 (jumped over 99 and 100)"
    assert vm.registers[4] == 2, "r4 should be 2 (jumped over 200 and 201)"


def test_io():
    """Test input/output operations"""
    # Save original stdin/stdout
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    
    # Create string buffer for input and output
    sys.stdin = StringIO("42\n")
    sys.stdout = StringIO()
    
    program_text = """
    READ r1        # Read input into r1 (will be 42)
    MUL r1, 2, r2  # Multiply by 2 (84)
    WRITE r2       # Print result
    """
    
    try:
        lexer = Lexer(program_text)
        program = parse(lexer)
        vm = VM(program)
        vm.run()
        
        assert vm.registers[1] == 42, "r1 should be 42 (input value)"
        assert vm.registers[2] == 84, "r2 should be 84 (42 * 2)"
        
        output = sys.stdout.getvalue()
        assert "84" in output, "Output should contain 84"
    
    finally:
        # Restore original stdin/stdout
        sys.stdin = old_stdin
        sys.stdout = old_stdout


def run_all_tests():
    """Run all tests and report results"""
    tests = [
        ("Lexer", test_lexer),
        ("Parser", test_parser),
        ("VM Arithmetic", test_arithmetic),
        ("VM Memory", test_memory),
        ("VM Jumps", test_jumps),
        ("VM I/O", test_io)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            print(f"Running {test_name} tests...", end=" ")
            test_func()
            print("PASSED")
            passed += 1
        except AssertionError as e:
            print(f"FAILED: {str(e)}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {str(e)}")
            failed += 1
    
    print(f"\nTest Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 