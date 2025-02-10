## Virtual Machine Specification

### 1. Overview
The virtual machine (VM) executes a simple bytecode-based instruction set. It operates on a register-based architecture with stack support and interacts with main memory.

### 2. Registers
The VM includes the following registers:
- **16 General-Purpose Registers**: Named `r0` through `r15`.
- **IP (Instruction Pointer)**: Alias for `r15`, holds the address of the next instruction to execute.
- **SP (Stack Pointer)**: Alias for `r14`, points to the top of the stack.

### 3. Memory Model
- **Main Memory**: A contiguous block of reasonably large size, accessible for both instructions and data.

### 4. Instruction Set
A program is a sequence of instructions. Each instruction consists of an operation followed by arguments. The argument types are:
- **src**: Source register or literal.
- **tgt**: Target register.
- **memref**: Register or literal, containing memory address.
- **cond**: Condition flag (`zero`, `pos`, or `neg`).

The VM supports the following instructions:

#### 4.1. Data Movement
- **CP src, tgt**: Copies the value from `src` to `tgt`.
  - `src`: Source register or literal.
  - `tgt`: Target register.

- **LOAD memref, tgt**: Loads a value from memory address `memref` into register `tgt`.
  - `memref`: Source memory reference (register or literal, dereferenced).
  - `tgt`: Destination register.

- **STORE src, memref**: Stores the value from `src` into memory address `memref`.
  - `src`: Source register or literal.
  - `memref`: Destination memory reference (register or literal, dereferenced).

#### 4.2. Arithmetic Operations
- **ADD src, src, tgt**: Adds two values and stores the result in `tgt`.
  - `src`: Source value (register or literal).
  - `src`: Second source value.
  - `tgt`: Target register.

- **MUL src, src, tgt**: Multiplies two values and stores the result in `tgt`.

- **SUB src, src, tgt**: Subtracts the second source from the first and stores the result in `tgt`.

#### 4.3. I/O Operations
- **READ tgt**: Reads an input and stores it in `tgt`.
- **WRITE src**: Writes the value in `src` to output.

#### 4.4. Control Flow
- **JUMP cond, src, addr**: Jumps to an address based on a condition.
  - `cond`: Conditional flag (`zero`, `pos`, or `neg`).
  - `src`: Value to compare.
  - `addr`: Address to jump to.

### 5. Execution Model
1. The VM starts execution at the address stored in `IP` (`r15`).
2. Instructions are fetched sequentially, decoded, and executed.
3. The Stack Pointer (`SP`, `r14`) manages function calls and local storage if applicable.

This specification serves as a formal definition of the VM architecture and instruction set.



