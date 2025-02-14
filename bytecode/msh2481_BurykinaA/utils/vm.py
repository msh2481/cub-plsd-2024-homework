from dataclasses import dataclass
from typing import Protocol

from utils.parsing import Instruction, Register, Literal, Value, Condition, TokenType


class Target(Protocol):
    def get(self) -> int:
        """Get the current value"""
        ...

    def set(self, value: int) -> None:
        """Set a new value"""
        ...


@dataclass
class RegisterTarget:
    vm: 'VM'
    register: int

    def get(self) -> int:
        return self.vm.registers[self.register]

    def set(self, value: int) -> None:
        self.vm.registers[self.register] = value


@dataclass
class MemoryTarget:
    vm: 'VM'
    address: int

    def get(self) -> int:
        return self.vm.memory[self.address]

    def set(self, value: int) -> None:
        self.vm.memory[self.address] = value


class VM:
    def __init__(self, program: list[Instruction]):
        self.program = program
        self.pc = 0
        self.registers = [0] * 16
        self.memory = {}
        self.running = True

    def resolve_target(self, value: Value) -> Target:
        """Convert a Value (Register or Literal) into a Target object"""
        if isinstance(value, Register):
            return RegisterTarget(self, value.number)
        elif isinstance(value, Literal):
            return MemoryTarget(self, value.value)
        else:
            raise ValueError(f"Invalid target type: {type(value)}")

    def get_value(self, value: Value) -> int:
        """Get the integer value from a Register or Literal"""
        if isinstance(value, Register):
            return self.registers[value.number]
        elif isinstance(value, Literal):
            return value.value
        else:
            raise ValueError(f"Invalid value type: {type(value)}")

    def resolve_condition(self, condition: Condition, value: int) -> bool:
        """Check if a condition is satisfied for a given value"""
        if condition == Condition.ZERO:
            return value == 0
        elif condition == Condition.POS:
            return value > 0
        elif condition == Condition.NEG:
            return value < 0
        else:
            raise ValueError(f"Invalid condition: {condition}")

    def step(self) -> bool:
        """Execute one instruction. Returns True if the machine should continue running."""
        if not self.running or self.pc >= len(self.program):
            return False

        instruction = self.program[self.pc]
        self.pc += 1

        if instruction.opcode == TokenType.CP:
            src, tgt = instruction.args
            tgt_reg = self.resolve_target(tgt)
            tgt_reg.set(self.get_value(src))

        elif instruction.opcode == TokenType.LOAD:
            addr, tgt = instruction.args
            mem = self.resolve_target(addr)
            tgt_reg = self.resolve_target(tgt)
            tgt_reg.set(mem.get())

        elif instruction.opcode == TokenType.STORE:
            src, addr = instruction.args
            mem = self.resolve_target(addr)
            mem.set(self.get_value(src))

        elif instruction.opcode == TokenType.ADD:
            src1, src2, tgt = instruction.args
            tgt_reg = self.resolve_target(tgt)
            tgt_reg.set(self.get_value(src1) + self.get_value(src2))

        elif instruction.opcode == TokenType.MUL:
            src1, src2, tgt = instruction.args
            tgt_reg = self.resolve_target(tgt)
            tgt_reg.set(self.get_value(src1) * self.get_value(src2))

        elif instruction.opcode == TokenType.SUB:
            src1, src2, tgt = instruction.args
            tgt_reg = self.resolve_target(tgt)
            tgt_reg.set(self.get_value(src1) - self.get_value(src2))

        elif instruction.opcode == TokenType.READ:
            tgt = instruction.args[0]
            tgt_reg = self.resolve_target(tgt)
            value = int(input("Enter a number: "))
            tgt_reg.set(value)

        elif instruction.opcode == TokenType.WRITE:
            src = instruction.args[0]
            print(self.get_value(src))

        elif instruction.opcode == TokenType.JUMP:
            cond, src, addr = instruction.args
            if self.resolve_condition(cond, self.get_value(src)):
                self.pc = self.get_value(addr)

        else:
            raise ValueError(f"Invalid instruction: {instruction}")

        return True

    def run(self) -> None:
        while self.step():
            pass