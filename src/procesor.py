# src/procesor.py

import time
from .alu import ClassicalALU, QuantumALU
from .memory import ClassicalMemory
from .registers import ClassicalRegisters, QuantumRegisters
from .io import InputHandler, OutputHandler, ProgramLoader

class Procesor:
    def __init__(self, mode="classical", debug=False, cycle_delay=0):
        """
        Initialize the processor.

        mode: "classical", "quantum", or "hybrid"
        debug: enable debug output
        cycle_delay: delay in seconds between cycles (0 = no delay)
        """
        self.mode = mode
        self.debug = debug
        self.running = False
        self.clock = 0  # Clock cycle counter
        self.cycle_delay = cycle_delay

        # Core components
        self.registers = ClassicalRegisters()
        self.memory = ClassicalMemory()
        self.input_handler = InputHandler()
        self.output_handler = OutputHandler(log_to_file=debug)
        self.program_loader = ProgramLoader()

        # ALUs
        self.classical_alu = ClassicalALU(bit_width=8)
        if mode in ("quantum", "hybrid"):
            self.quantum_registers = QuantumRegisters(num_qubits=8)
            self.quantum_alu = QuantumALU(self.quantum_registers)
        else:
            self.quantum_registers = None
            self.quantum_alu = None

        self.program = []
        self._debug_print(f"Procesor initialized in {mode} mode")

    def _debug_print(self, message):
        if self.debug:
            self.output_handler.print_debug(message, debug_enabled=True)

    def load_program_from_string(self, program_str):
        try:
            if hasattr(self.program_loader, 'parse_program_str'):
                self.program = self.program_loader.parse_program_str(program_str)
            else:
                lines = [line.strip() for line in program_str.strip().splitlines() if line.strip() and not line.strip().startswith('#')]
                instructions = []
                for line in lines:
                    parts = line.split()
                    opcode = parts[0]
                    operands = parts[1:] if len(parts) > 1 else []
                    instructions.append({"opcode": opcode, "operands": operands})
                self.program = instructions

            self.registers.set("pc", 0)
            self.clock = 0
            self._debug_print(f"Loaded {len(self.program)} instructions from string")
            return True
        except Exception as e:
            self.output_handler.print_error(f"Failed to load program from string: {e}")
            return False


    def status(self, include_ram=False, include_registers=False, include_current_instruction=False, include_pc=False, include_clock=False):
        """
        Return a dict representing current processor status parts based on flags.

        Parameters:
            include_ram (bool): Include a snapshot of classical memory (dict or list).
            include_registers (bool): Include classical registers states.
            include_current_instruction (bool): Include the instruction at the current program counter.
            include_pc (bool): Include the current program counter value.
            include_clock (bool): Include the current clock cycle count.

        Returns:
            dict: Status snapshot with selected information.
        """
        status = {}

        if include_ram:
            # Assuming self.memory has a .dump() or similar method; else provide your own copy
            if hasattr(self.memory, 'dump'):
                status['ram'] = self.memory.dump()
            else:
                # Fallback: shallow copy if .memory attribute is e.g. a list or dict
                status['ram'] = dict(self.memory.memory) if hasattr(self.memory, 'memory') else None

        if include_registers:
            # Assuming self.registers has a method or attribute to get all registers as dict
            if hasattr(self.registers, 'dump'):
                status['registers'] = self.registers.regs  # e.g. a method that returns al
            else:
                # Fallback: shallow copy of .registers dict attribute or however registers are stored
                status['registers'] = [0]*8

        if include_pc:
            if hasattr(self.registers, 'get'):
                status['pc'] = self.registers.get("pc")
            else:
                status['pc'] = None

        if include_current_instruction:
            pc = status.get('pc')
            if pc is None:
                # Try to get pc now if not already fetched
                if hasattr(self.registers, 'get'):
                    pc = self.registers.get("pc")
            if pc is not None and 0 <= pc < len(self.program):
                status['current_instruction'] = self.program[pc]
            else:
                status['current_instruction'] = None

        if include_clock:
            status['clock'] = getattr(self, 'clock', None)

        return status


    def load_program(self, filename):
        """Load program from file."""
        try:
            self.program = self.program_loader.load_program(filename)
            self.registers.set("pc", 0)
            self.clock = 0  # Reset clock when loading new program
            self._debug_print(f"Loaded {len(self.program)} instructions")
            return True
        except Exception as e:
            self.output_handler.print_error(f"Failed to load: {e}")
            return False

    def run(self):
        """Run the processor until completion."""
        self.running = True
        self.output_handler.print_output("Processor starting...")
        while self.running:
            if not self.step():
                break
        self.output_handler.print_output("Processor stopped")
        self.report_clock()

    def step(self):
        """Execute one instruction."""
        if not self.program:
            self.output_handler.print_error("No program loaded")
            return False

        pc = self.registers.get("pc")
        if pc >= len(self.program):
            self.output_handler.print_output("Program finished")
            self.running = False
            return False

        instr = self.program[pc]
        self.execute_instruction(instr)

        # Increment clock cycle
        self.clock += 1
        self._debug_print(f"Clock cycle: {self.clock}")

        # Optional delay between cycles
        if self.cycle_delay > 0:
            time.sleep(self.cycle_delay)

        # Increment PC unless modified by a jump
        if self.registers.get("pc") == pc:
            self.registers.set("pc", pc + 1)
        return True

    def report_clock(self):
        """Report total clock cycles used."""
        self.output_handler.print_output(f"Total cycles: {self.clock}")

    def execute_instruction(self, instr):
        """Dispatch and execute a single instruction."""
        opcode = instr["opcode"].lower()
        operands = instr.get("operands", [])
        self._debug_print(f"Exec {opcode} {operands}")

        try:
            # Classical ALU ops
            if opcode == "mov": return self._execute_mov(operands)
            if opcode == "add": return self._execute_alu(self.classical_alu.add, operands)
            if opcode == "sub": return self._execute_alu(self.classical_alu.sub, operands)
            if opcode == "mul": return self._execute_mul(operands)
            if opcode == "dvd": return self._execute_dvd(operands)
            if opcode == "neg": return self._execute_neg(operands)

            # Quantum gates
            if opcode in ("h","x","y","z","s","t","rx","ry","rz",
                          "cx","cnot","cz","cy","ccx","toffoli","swap"):
                return self._execute_quantum_gate(opcode, operands)

            # Measurement & reset
            if opcode == "measure": return self._execute_measure(operands)
            if opcode == "reset": return self._execute_reset(operands)

            # Control, I/O, queue, logic, jumps
            if opcode == "cmp": return self._execute_cmp(operands)
            if opcode == "eqq": return self._execute_eqq(operands)
            if opcode == "and": return self._execute_and(operands)
            if opcode == "or": return self._execute_or(operands)
            if opcode == "not": return self._execute_not(operands)
            if opcode == "jmp": return self._execute_jmp(operands)
            if opcode == "jmpif": return self._execute_jmpif(operands)
            if opcode == "out": return self._execute_out(operands)
            if opcode == "in": return self._execute_in(operands)
            if opcode == "push": return self._execute_push(operands)
            if opcode == "pop": return self._execute_pop(operands)
            if opcode == "pp": return self._execute_pp(operands)

            raise ValueError(f"Unknown opcode: {opcode}")

        except Exception as e:
            self.output_handler.print_error(f"Error executing {opcode}: {e}")
            self.running = False

    # === Classical ALU helpers ===

    def _execute_alu(self, fn, ops):
        if len(ops) != 2:
            raise ValueError(f"ALU operation requires 2 operands")
        dst_t, dst_v = self.parse_operand(ops[0])
        src_t, src_v = self.parse_operand(ops[1])
        a = self.get_operand_value(dst_t, dst_v)
        b = self.get_operand_value(src_t, src_v)
        res, _ = fn(a, b)
        self.set_operand_value(dst_t, dst_v, res)

    def _execute_mov(self, ops):
        if len(ops) != 2:
            raise ValueError("MOV requires 2 operands")
        src_t, src_v = self.parse_operand(ops[0])
        dst_t, dst_v = self.parse_operand(ops[1])
        val = self.get_operand_value(src_t, src_v)
        self.set_operand_value(dst_t, dst_v, val)

    def _execute_mul(self, ops):
        if len(ops) != 2:
            raise ValueError("MUL requires 2 operands")
        dst_t, dst_v = self.parse_operand(ops[0])
        src_t, src_v = self.parse_operand(ops[1])
        a = self.get_operand_value(dst_t, dst_v)
        b = self.get_operand_value(src_t, src_v)
        result = a * b
        self.set_operand_value(dst_t, dst_v, result)

    def _execute_dvd(self, ops):
        if len(ops) != 2:
            raise ValueError("DVD requires 2 operands")
        dst_t, dst_v = self.parse_operand(ops[0])
        src_t, src_v = self.parse_operand(ops[1])
        a = self.get_operand_value(dst_t, dst_v)
        b = self.get_operand_value(src_t, src_v)
        if b == 0:
            raise ValueError("Division by zero")
        result = a // b
        self.set_operand_value(dst_t, dst_v, result)

    def _execute_neg(self, ops):
        if len(ops) != 1:
            raise ValueError("NEG requires 1 operand")
        dst_t, dst_v = self.parse_operand(ops[0])
        a = self.get_operand_value(dst_t, dst_v)
        result = -a
        self.set_operand_value(dst_t, dst_v, result)

    # === Quantum gate dispatcher ===

    def _execute_quantum_gate(self, opcode, ops):
        if self.mode not in ("quantum", "hybrid"):
            raise RuntimeError("Quantum instructions disabled in classical mode")

        mapping = {
            "h":"h_gate","x":"x_gate","y":"y_gate","z":"z_gate",
            "s":"s_gate","t":"t_gate",
            "rx":"rx_gate","ry":"ry_gate","rz":"rz_gate",
            "cx":"cnot_gate","cnot":"cnot_gate",
            "cz":"cz_gate","cy":"cy_gate",
            "ccx":"ccx_gate","toffoli":"ccx_gate",
            "swap":"swap_gate"
        }
        method = mapping[opcode]
        fn = getattr(self.quantum_alu, method)

        # Rotations: angle, qubit
        if opcode in ("rx","ry","rz"):
            angle = float(ops[0])
            qubit = self.parse_qubit(ops[1])
            fn(qubit, angle)
            return

        # Toffoli: 3 qubits
        if opcode in ("ccx","toffoli"):
            c1 = self.parse_qubit(ops[0])
            c2 = self.parse_qubit(ops[1])
            tgt = self.parse_qubit(ops[2])
            fn(c1, c2, tgt)
            return

        # Single or two-qubit gates
        qubits = [self.parse_qubit(o) for o in ops]
        fn(*qubits)

    # === Measurement & Reset ===

    def _execute_measure(self, ops):
        if len(ops) != 2:
            raise ValueError("MEASURE requires 2 operands")
        q = self.parse_qubit(ops[0])
        dst_t, dst_v = self.parse_operand(ops[1])
        bit = self.quantum_registers.measure(q)
        self.set_operand_value(dst_t, dst_v, bit)

    def _execute_reset(self, ops):
        if len(ops) != 1:
            raise ValueError("RESET requires 1 operand")
        q = self.parse_qubit(ops[0])
        self.quantum_registers.set(q, 0)

    # === Control / Logic / Jumps ===

    def _execute_cmp(self, ops):
        if len(ops) != 2:
            raise ValueError("CMP requires 2 operands")
        a_t, a_v = self.parse_operand(ops[0])
        b_t, b_v = self.parse_operand(ops[1])
        a = self.get_operand_value(a_t, a_v)
        b = self.get_operand_value(b_t, b_v)
        result = a > b
        self.registers.set("b", result)

    def _execute_eqq(self, ops):
        if len(ops) != 2:
            raise ValueError("EQQ requires 2 operands")
        a_t, a_v = self.parse_operand(ops[0])
        b_t, b_v = self.parse_operand(ops[1])
        a = self.get_operand_value(a_t, a_v)
        b = self.get_operand_value(b_t, b_v)
        result = a == b
        self.registers.set("b", result)

    def _execute_and(self, ops):
        if len(ops) != 1:
            raise ValueError("AND requires 1 operand")
        src_t, src_v = self.parse_operand(ops[0])
        a = self.get_operand_value(src_t, src_v)
        b = self.registers.get("b")
        result = bool(a) and bool(b)
        self.registers.set("b", result)

    def _execute_or(self, ops):
        if len(ops) != 1:
            raise ValueError("OR requires 1 operand")
        src_t, src_v = self.parse_operand(ops[0])
        a = self.get_operand_value(src_t, src_v)
        b = self.registers.get("b")
        result = bool(a) or bool(b)
        self.registers.set("b", result)

    def _execute_not(self, ops):
        if len(ops) != 1 or ops[0] != 'b':
            raise ValueError("NOT only works for b register")
        value = self.registers.get('b')
        self.registers.set('b', not value)

    def _execute_jmp(self, ops):
        if len(ops) != 1:
            raise ValueError("JMP requires 1 operand")
        target = int(ops[0])
        if 0 <= target < len(self.program):
            self.registers.set("pc", target)
        else:
            raise ValueError(f"Jump target {target} out of range")

    def _execute_jmpif(self, ops):
        if len(ops) != 1:
            raise ValueError("JMPIF requires 1 operand")
        if self.registers.get("b"):
            target = int(ops[0])
            if 0 <= target < len(self.program):
                self.registers.set("pc", target)
            else:
                raise ValueError(f"Jump target {target} out of range")

    # === I/O Operations ===

    def _execute_out(self, ops):
        if len(ops) != 1:
            raise ValueError("OUT requires 1 operand")
        t, v = self.parse_operand(ops[0])
        value = self.get_operand_value(t, v)
        self.output_handler.print_output(f"OUT: {value}")

    def _execute_in(self, ops):
        if len(ops) != 1:
            raise ValueError("IN requires 1 operand")
        t, v = self.parse_operand(ops[0])
        input_val = self.input_handler.read_keyboard_input(f"IN for {ops[0]}: ")
        self.set_operand_value(t, v, int(input_val))

    # === Queue Operations ===

    def _execute_push(self, ops):
        if len(ops) != 1:
            raise ValueError("PUSH requires 1 operand")
        t, v = self.parse_operand(ops[0])
        value = self.get_operand_value(t, v)
        self.memory.memory.append(value)

    def _execute_pop(self, ops):
        if len(ops) != 1:
            raise ValueError("POP requires 1 operand")
        t, v = self.parse_operand(ops[0])
        if self.memory.memory:
            value = self.memory.memory.popleft()
            self.set_operand_value(t, v, value)

    def _execute_pp(self, ops):
        """Peek and push - move front element to back"""
        if self.memory.memory:
            value = self.memory.memory.popleft()
            self.memory.memory.append(value)

    # === Operands and Registers ===

    def parse_operand(self, op):
        """Parse p0..pn, [p0], h1234, b, or immediate."""
        if op.startswith('p') and op[1:].isdigit():
            idx = int(op[1:])
            return "register", idx
        if op.startswith('[p') and op.endswith(']'):
            idx = int(op[2:-1])
            return "memory_ref", idx
        if op.startswith('h') and op[1:].isdigit():
            addr = int(op[1:])
            return "memory_addr", addr
        if op == 'b':
            return "boolean", None
        if op.isdigit() or (op.startswith('-') and op[1:].isdigit()):
            return "immediate", int(op)
        raise ValueError(f"Invalid operand: {op}")

    def get_operand_value(self, t, v):
        if t == "register":
            return self.registers.get(v)
        if t == "memory_ref":
            addr = self.registers.get(v)
            return self.memory.read(addr)
        if t == "memory_addr":
            return self.memory.read(v)
        if t == "boolean":
            return self.registers.get("b")
        if t == "immediate":
            return v
        raise ValueError(f"Unknown operand type: {t}")

    def set_operand_value(self, t, v, val):
        if t == "register":
            self.registers.set(v, val)
        elif t == "memory_addr":
            self.memory.write(v, val)
        elif t == "boolean":
            self.registers.set("b", val)
        else:
            raise ValueError(f"Cannot set operand type: {t}")

    def parse_qubit(self, op):
        if op.startswith('q') and op[1:].isdigit():
            q = int(op[1:])
            if self.quantum_registers and 0 <= q < self.quantum_registers.num_qubits:
                return q
        raise ValueError(f"Invalid qubit: {op}")
