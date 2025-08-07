# Intructions in md for alu

Here are the instruction details in Markdown format for the Arithmetic Logic Unit (ALU) used in your Pearl Quantum Processor, encompassing both classical and quantum operations:

# ALU Instructions for Pearl Quantum Processor

## Classical ALU Instructions

These instructions operate on classical registers and memory, performing basic arithmetic and bitwise operations.


| Instruction | Description | Operands | Details |
| :-- | :-- | :-- | :-- |
| `add` | Add two values | `add dst src` | `dst = dst + src` with wrap-around, updates flags |
| `sub` | Subtract source from destination | `sub dst src` | `dst = dst - src` with wrap-around, updates flags |
| `mul` | Multiply two values | `mul dst src` | `dst = dst * src` (simple multiply) |
| `dvd` | Integer division | `dvd dst src` | `dst = dst // src`, error on division by zero |
| `neg` | Negate value | `neg dst` | `dst = -dst` |
| `mov` | Move or copy value | `mov src dst` | `dst = src` |
| `cmp` | Compare two values | `cmp a b` | Sets boolean flag if `a > b` |
| `eqq` | Equality test | `eqq a b` | Sets boolean flag if `a == b` |
| `and` | Boolean AND | `and src` | `b = b AND src` |
| `or` | Boolean OR | `or src` | `b = b OR src` |
| `not` | Boolean NOT | `not b` | `b = NOT b` |
| `jmp` | Unconditional jump | `jmp target` | Jump to instruction at `target` |
| `jmpif` | Conditional jump | `jmpif target` | Jump if boolean flag `b` is true |
| `push` | Push to queue/memory stack | `push src` | Pushes value onto internal memory queue |
| `pop` | Pop from queue/memory stack | `pop dst` | Pops value from queue into destination |
| `pp` | Peek and push (cycle front queue element) | `pp` | Moves front of queue to back |
| `out` | Output value | `out src` | Prints or logs value |
| `in` | Input value from keyboard | `in dst` | Reads input into destination register |

## Quantum ALU Instructions

These operate on quantum registers (qubits) using quantum gates, measurements, and reset operations.


| Instruction | Description | Operands | Details |
| :-- | :-- | :-- | :-- |
| `h` | Hadamard gate | `h qN` | Creates superposition on qubit `qN` |
| `x` | Pauli-X (NOT) gate | `x qN` | Bit-flip gate on qubit `qN` |
| `y` | Pauli-Y gate | `y qN` | Bit-phase flip gate |
| `z` | Pauli-Z gate | `z qN` | Phase-flip gate |
| `s` | Phase gate (π/2) | `s qN` | Applies phase of π/2 |
| `t` | T gate (π/4 phase) | `t qN` | Applies phase of π/4 |
| `rx` | Rotation around X axis | `rx angle qN` or `rx pN qN` | Angle in radians; accepts float or register |
| `ry` | Rotation around Y axis | `ry angle qN` or `ry pN qN` | Angle in radians; accepts float or register |
| `rz` | Rotation around Z axis | `rz angle qN` or `rz pN qN` | Angle in radians; accepts float or register |
| `cx` / `cnot` | Controlled-NOT (CNOT) gate | `cx control target` | Flip target if control is |
| `cz` | Controlled-Z gate | `cz control target` | Phase flip if both are |
| `cy` | Controlled-Y gate | `cy control target` | Y gate controlled |
| `ccx` / `toffoli` | Toffoli (CCX) gate | `ccx control1 control2 target` | Flip target if both controls |
| `swap` | Swap gate | `swap q1 q2` | Swaps states of two qubits |
| `measure` | Measure qubit and store result | `measure qN pN` | Measures qubit `qN`, stores classical bit in register `pN` |
| `reset` | Reset qubit to | 0⟩ | `reset qN` |
| `qft` | Quantum Fourier Transform | `qft qN1 qN2 ...` | Applies QFT on all specified qubits |

## Notes:

- Classical operands (`pN`, immediate values) represent classical registers or immediate integers.
- Quantum operands (`qN`) represent qubit indices.
- Rotation gates (`rx`, `ry`, `rz`) accept either float angles directly or scaled integer values stored in classical registers (with internal scaling to float).
- The ALU functions and processor respect wrap-around and overflow flags for arithmetic.
- Measurement results are always classical bits stored in classical registers.
- Control flow instructions use a boolean flag register `b`.

This instruction summary complements your existing docs and source code implementations of `ClassicalALU` and `QuantumALU` modules.