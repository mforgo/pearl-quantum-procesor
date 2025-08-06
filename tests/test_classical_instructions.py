import pytest
from src.procesor import Procesor

@pytest.fixture
def cpu():
    c = Procesor(mode="classical", debug=False)
    # load a simple program manually
    c.program = [
        {"opcode":"mov","operands":["5","p0"]},
        {"opcode":"mov","operands":["2","p1"]},
        {"opcode":"add","operands":["p0","p1"]},
        {"opcode":"mov","operands":["p0","h0"]},
        {"opcode":"cmp","operands":["p0","p1"]},
        {"opcode":"jmpif","operands":["7"]},
        {"opcode":"mov","operands":["0","p2"]},
        {"opcode":"mov","operands":["1","p2"]}
    ]
    c.registers.set("pc",0)
    c.running = True
    return c

def test_add_and_compare(cpu):
    # Run all steps
    while cpu.running and cpu.step():
        pass
    # After add: p0 = 7
    assert cpu.registers.get(0) == 7
    # Memory[0] == 7
    assert cpu.memory.read(0) == 7
    # Compare 7>2 sets b True
    assert cpu.registers.get("b") is True
    # Following jmpif should skip mov 0 p2, set p2=1
    assert cpu.registers.get(2) == 1

def test_push_pop(cpu):
    # Reset memory queue
    cpu.memory.reset()
    # push p0 (initially 7 after first two instructions)
    cpu.registers.set(0, 9)
    cpu._execute_push(["p0"])
    assert list(cpu.memory.memory) == [9]
    # pop back into p3
    cpu._execute_pop(["p3"])
    assert cpu.registers.get(3) == 9
    # queue is now empty
    assert len(cpu.memory.memory) == 0
