## Design

In the lecture, we designed a bytecode machine and an instruction set for it.

### Exercise 1

In your `README.md`, write a short description of the design. Make sure to address:
- What state does the machine have? (Registers, heap, etc.)
- What instructions are there?
- What arguments do these instructions take?
- What do the instructions do?

## Implementation

Our implementation will take a sequence of instructions as a string, turn it into a more convenient representation, and then execute it by interpreting the instructions. We do this in three steps:

1. **Lexing**: Convert the string to a sequence of tokens.
2. **Parsing**: Build instructions from the token stream.
3. **Interpretation**: Step through the instructions and execute them.

For a simple language like this, splitting lexing and parsing may seem like overkill. However, it is recommended to do it this way so that the lexer can be reused in future assignments. If you are familiar with lexing and parsing and want to use a more advanced technique like parser generators or parser combinators, feel free to do so.

### Lexing

A lexer takes a string as input, splits it into tokens, and attaches information to these tokens that will be useful for the parser. For example, a lexer for arithmetic could take the string `2*(a + b)` and split it into the tokens `2`, `*`, `(`, `a`, `+`, `b`, `)`. The output could look like:

#### Haskell:
```
Literal 2
Operation "*"
OpenParenthesis
Variable "a"
Operation "+"
Variable "b"
CloseParenthesis
```
#### Kotlin, Rust:
```
Literal(2)
Operation("*")
OpenParenthesis()
Variable("a")
Operation("+")
Variable("b")
CloseParenthesis()
```
#### Python:
```
('LITERAL', 2)
('OPERATION', '*')
('OPEN_PAREN', None)
('VARIABLE', 'a')
('OPERATION', '+')
('VARIABLE', 'b')
('CLOSE_PAREN', None)
```

A lexer should provide an interface that lets you get the next token on demand, making the parser simpler.

### Exercise 2
Define a `Token` type.

### Exercise 3
Implement a `Lexer` class that takes a string at construction and provides a `next` function to get the next token (if any).

**Hints:**
- Regular expressions can be useful to determine what kind of token you’re seeing.
- You can make a `Rule` type that maps regexes to handlers. A lexer just needs to try all rules.
- Don’t forget to skip over whitespace.

### Parsing

Now it’s time to turn tokens into a program. For most programming languages, parsing results in tree structures. However, since we have a very simple language, we can get away with representing the program as just a list of instructions.

### Exercise 4
Define an `Instruction` type.

### Exercise 5
Implement a `parse` function that takes your lexer and returns a list of instructions.

**Hint:**
- Since you may often know what token to expect next, it may be worth adding a function to your lexer that gets a token and checks it is of a certain type.

### Interpretation

We now implement the bytecode machine itself, which we’ll call the VM. This involves representing all the state that the machine has and specifying for each instruction what effect it has on the state.

### Exercise 6
Define a `VM` class that takes the program at construction and contains all the state that the bytecode machine has.

### Exercise 7
Define a `Target` type with `get` and `set` methods. Implement a `resolve_target` function that takes an instruction target and returns a `Target` object.

**Example usage:**
```
# For instruction mov a b
ra = resolve_target(a)
rb = resolve_target(b)
ra.set(rb.get())
```

### Exercise 8
Implement a `step` function in `VM` that interprets a single instruction and returns whether the machine has halted.

### Exercise 9
Implement a `run` function in `VM` that runs the machine for as long as possible.

**Hints:**
- A little time spent writing debugging tools can save a lot of time debugging.
- Depending on the language, you may want a similar `resolve_condition` function for conditional jumps.

## Next Steps

Congratulations, you’re done with the initial implementation! However, languages rarely stay the same over time.

### Exercise 10
Come up with a new feature for this language. Describe what it looks like and how it behaves in your `README.md`.

### Exercise 11
Write two example programs that use your feature.

### Exercise 12
Extend your lexer, parser, and VM to support this feature.

## If You’re Done Early…

### Exercise 13
Find an ambiguity in our specification and clarify it in your `README.md`.

### Exercise 14
Suppose we want to compile a language with functions to this bytecode. What would a function call look like? Write a specification for it.

### Exercise 15
When writing in a low-level language, we typically want to use labels rather than absolute jumps. Introduce a syntax for labels and implement a label resolution function in your interpreter.

