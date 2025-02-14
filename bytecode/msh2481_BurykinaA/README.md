# Our GitHub handles

- [@msh2481](https://github.com/msh2481)
- [@BurykinaA](https://github.com/BurykinaA)

# Bytecode Interpreter

A simple bytecode interpreter that executes a custom assembly-like language.

The short description of the design is in the [SPEC.md](SPEC.md) file.
## Requirements

- Python 3.10 or higher

## Usage

### Running a Bytecode Program

Create a text file with your bytecode program (e.g., `program.txt`):
```
READ r1        # Read a number into r1
MUL r1, 2, r2  # Multiply it by 2
WRITE r2       # Print the result
```

Run the program using Python:
```bash
python -m bytecode.msh2481_BurykinaA.main program.txt
```
### Running Tests

Run all tests:
```bash
python bytecode/msh2481_BurykinaA/tests.py
```

## Instruction Set

The interpreter supports the following instructions:

- `CP src, tgt` - Copy value from src to target register
- `LOAD addr, tgt` - Load value from memory address into target register
- `STORE src, addr` - Store value from source into memory address
- `ADD src1, src2, tgt` - Add two values and store in target register
- `MUL src1, src2, tgt` - Multiply two values and store in target register
- `SUB src1, src2, tgt` - Subtract src2 from src1 and store in target register
- `READ tgt` - Read integer from input into target register
- `WRITE src` - Write value to output
- `JUMP cond, src, addr` - Jump to address if condition is met

### Conditions
- `zero` - Jump if value is zero
- `pos` - Jump if value is positive
- `neg` - Jump if value is negative

### Values
- Registers: `r0` through `r15`
- Literals: Any integer value (e.g., `42`, `-17`)

## Example Program

This program is in the [program.txt](program.txt) file. Hence, you can run it by executing the following command:

```
# Calculate factorial of input number
CP 1, r2           # Initialize result to 1
READ r1            # Read input number
JUMP zero, r1, 7   # If input is 0, jump to end
MUL r2, r1, r2     # Multiply result by current number
SUB r1, 1, r1      # Decrement counter
JUMP pos, r1, 3    # If counter > 0, continue multiplication
WRITE r2           # Print result
```
