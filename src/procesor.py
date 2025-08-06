# src/procesor.py

from .alu import ClassicalALU, QuantumALU
from .memory import ClassicalMemory
from .registers import ClassicalRegisters, QuantumRegisters
from .io import InputHandler, OutputHandler, ProgramLoader

class Procesor:
    def __init__(self, mode="classical", debug=False):
        self.mode = mode
        self.debug = debug
        self.running = False

        # Common classical registers for PC and b
        self.registers = ClassicalRegisters()
        self.memory    = ClassicalMemory()
        self.input_handler  = InputHandler()
        self.output_handler = OutputHandler(log_to_file=debug)
        self.program_loader = ProgramLoader()

        if mode == "quantum":
            # Create quantum registers
            self.quantum_registers = QuantumRegisters(num_qubits=4)
            # Pass registers into ALU
            self.alu = QuantumALU(self.quantum_registers)
        else:
            self.alu = ClassicalALU(bit_width=8)

        self.program = []
        self._debug_print(f"Procesor initialized in {mode} mode")
    
    def _debug_print(self, message):
        """Print debug message if debug is enabled"""
        if self.debug:
            self.output_handler.print_debug(message, debug_enabled=True)
    
    def load_program(self, filename):
        """Load program from file"""
        try:
            self.program = self.program_loader.load_program(filename)
            self.registers.set("pc", 0)
            self._debug_print(f"Loaded program with {len(self.program)} instructions")
            return True
        except Exception as e:
            self.output_handler.print_error(f"Failed to load program: {e}")
            return False
    
    def parse_operand(self, operand):
        """Parse operand and return (type, value)"""
        if operand.startswith('p') and operand[1:].isdigit():
            # Register reference (p0, p1, etc.)
            reg_num = int(operand[1:])
            if 0 <= reg_num <= 7:
                return ("register", reg_num)
        elif operand.startswith('[p') and operand.endswith(']'):
            # Memory reference [p2]
            reg_num = int(operand[2:-1])
            if 0 <= reg_num <= 7:
                return ("memory_ref", reg_num)
        elif operand.startswith('h') and operand[1:].isdigit():
            # Direct memory address (h1234)
            addr = int(operand[1:])
            return ("memory_addr", addr)
        elif operand == 'b':
            # Boolean register
            return ("boolean", None)
        elif operand.isdigit() or (operand.startswith('-') and operand[1:].isdigit()):
            # Immediate value
            return ("immediate", int(operand))
        else:
            raise ValueError(f"Invalid operand: {operand}")
    
    def get_operand_value(self, operand_type, operand_value):
        """Get actual value from operand"""
        if operand_type == "register":
            return self.registers.get(operand_value)
        elif operand_type == "memory_ref":
            addr = self.registers.get(operand_value)
            return self.memory.read(addr)
        elif operand_type == "memory_addr":
            return self.memory.read(operand_value)
        elif operand_type == "boolean":
            return self.registers.get("b")
        elif operand_type == "immediate":
            return operand_value
        else:
            raise ValueError(f"Unknown operand type: {operand_type}")
    
    def set_operand_value(self, operand_type, operand_value, value):
        """Set value to operand"""
        if operand_type == "register":
            self.registers.set(operand_value, value)
        elif operand_type == "memory_addr":
            self.memory.write(operand_value, value)
        elif operand_type == "boolean":
            self.registers.set("b", value)
        else:
            raise ValueError(f"Cannot set value to operand type: {operand_type}")
    
    def execute_instruction(self, instruction):
        """Execute a single instruction"""
        opcode = instruction['opcode'].lower()
        operands = instruction.get('operands', [])
        
        self._debug_print(f"Executing: {opcode} {' '.join(operands)}")
        
        try:
            if opcode == 'mov':
                self._execute_mov(operands)
            elif opcode == 'add':
                self._execute_add(operands)
            elif opcode == 'sub':
                self._execute_sub(operands)
            elif opcode == 'dvd':
                self._execute_dvd(operands)
            elif opcode == 'mul':
                self._execute_mul(operands)
            elif opcode == 'neg':
                self._execute_neg(operands)
            elif opcode == 'cmp':
                self._execute_cmp(operands)
            elif opcode == 'eqq':
                self._execute_eqq(operands)
            elif opcode == 'and':
                self._execute_and(operands)
            elif opcode == 'or':
                self._execute_or(operands)
            elif opcode == 'jmp':
                self._execute_jmp(operands)
            elif opcode == 'jmpif':
                self._execute_jmpif(operands)
            elif opcode == 'out':
                self._execute_out(operands)
            elif opcode == 'in':
                self._execute_in(operands)
            elif opcode == 'push':
                self._execute_push(operands)
            elif opcode == 'pop':
                self._execute_pop(operands)
            elif opcode == 'pp':
                self._execute_pp(operands)
            elif opcode == 'not':
                self._execute_not(operands)

            # === JEDNOQUBITOVÉ KVANTOVÉ BRÁNY ===
            elif opcode == 'h':
                self._execute_h(operands)
            elif opcode == 'x':
                self._execute_x(operands)
            elif opcode == 'y':
                self._execute_y(operands)
            elif opcode == 'z':
                self._execute_z(operands)
            elif opcode == 's':
                self._execute_s(operands)
            elif opcode == 't':
                self._execute_t(operands)
            elif opcode == 'rx':
                self._execute_rx(operands)
            elif opcode == 'ry':
                self._execute_ry(operands)
            elif opcode == 'rz':
                self._execute_rz(operands)
                
            # === DVOUQUBITOVÉ KVANTOVÉ BRÁNY ===
            elif opcode == 'cx' or opcode == 'cnot':
                self._execute_cx(operands)
            elif opcode == 'cz':
                self._execute_cz(operands)
            elif opcode == 'cy':
                self._execute_cy(operands)
            elif opcode == 'ccx' or opcode == 'toffoli':
                self._execute_ccx(operands)
            elif opcode == 'swap':
                self._execute_swap(operands)
                
            # === KVANTOVÉ MĚŘENÍ A RESET ===
            elif opcode == 'measure':
                self._execute_measure(operands)
            elif opcode == 'reset':
                self._execute_reset(operands)
                
            # === KVANTOVÉ ALGORITMY ===
            elif opcode == 'bell':
                self._execute_bell(operands)
            elif opcode == 'qft':
                self._execute_qft(operands)
            else:
                raise ValueError(f"Unknown opcode: {opcode}")
                
        except Exception as e:
            self.output_handler.print_error(f"Error executing {opcode}: {e}")
            self.running = False
    
    def _execute_mov(self, operands):
        """Execute MOV instruction"""
        if len(operands) != 2:
            raise ValueError("MOV requires 2 operands")
        
        src_type, src_val = self.parse_operand(operands[0])
        dst_type, dst_val = self.parse_operand(operands[1])
        
        value = self.get_operand_value(src_type, src_val)
        self.set_operand_value(dst_type, dst_val, value)
    
    def _execute_add(self, operands):
        """Execute ADD instruction"""
        if len(operands) != 2:
            raise ValueError("ADD requires 2 operands")
        
        dst_type, dst_val = self.parse_operand(operands[0])
        src_type, src_val = self.parse_operand(operands[1])
        
        a = self.get_operand_value(dst_type, dst_val)
        b = self.get_operand_value(src_type, src_val)
        
        result, carry = self.alu.add(a, b)
        self.set_operand_value(dst_type, dst_val, result)
    
    def _execute_sub(self, operands):
        """Execute SUB instruction"""
        if len(operands) != 2:
            raise ValueError("SUB requires 2 operands")
        
        dst_type, dst_val = self.parse_operand(operands[0])
        src_type, src_val = self.parse_operand(operands[1])
        
        a = self.get_operand_value(dst_type, dst_val)
        b = self.get_operand_value(src_type, src_val)
        
        result, borrow = self.alu.sub(a, b)
        self.set_operand_value(dst_type, dst_val, result)
    
    def _execute_dvd(self, operands):
        """Execute DVD (divide) instruction"""
        if len(operands) != 2:
            raise ValueError("DVD requires 2 operands")
        
        dst_type, dst_val = self.parse_operand(operands[0])
        src_type, src_val = self.parse_operand(operands[1])
        
        a = self.get_operand_value(dst_type, dst_val)
        b = self.get_operand_value(src_type, src_val)
        
        if b == 0:
            raise ValueError("Division by zero")
        
        result = a // b  # Integer division
        self.set_operand_value(dst_type, dst_val, result)
    
    def _execute_mul(self, operands):
        """Execute MUL instruction"""
        if len(operands) != 2:
            raise ValueError("MUL requires 2 operands")
        
        dst_type, dst_val = self.parse_operand(operands[0])
        src_type, src_val = self.parse_operand(operands[1])
        
        a = self.get_operand_value(dst_type, dst_val)
        b = self.get_operand_value(src_type, src_val)
        
        result = a * b
        self.set_operand_value(dst_type, dst_val, result)
    
    def _execute_neg(self, operands):
        """Execute NEG instruction"""
        if len(operands) != 1:
            raise ValueError("NEG requires 1 operand")
        
        dst_type, dst_val = self.parse_operand(operands[0])
        value = self.get_operand_value(dst_type, dst_val)
        
        result = -value
        self.set_operand_value(dst_type, dst_val, result)
    
    def _execute_cmp(self, operands):
        """Execute CMP instruction"""
        if len(operands) != 2:
            raise ValueError("CMP requires 2 operands")
        
        a_type, a_val = self.parse_operand(operands[0])
        b_type, b_val = self.parse_operand(operands[1])
        
        a = self.get_operand_value(a_type, a_val)
        b = self.get_operand_value(b_type, b_val)
        
        result = a > b
        self.registers.set("b", result)
    
    def _execute_eqq(self, operands):
        """Execute EQQ instruction"""
        if len(operands) != 2:
            raise ValueError("EQQ requires 2 operands")
        
        a_type, a_val = self.parse_operand(operands[0])
        b_type, b_val = self.parse_operand(operands[1])
        
        a = self.get_operand_value(a_type, a_val)
        b = self.get_operand_value(b_type, b_val)
        
        result = a == b
        self.registers.set("b", result)
    
    def _execute_and(self, operands):
        """Execute AND instruction"""
        if len(operands) != 1:
            raise ValueError("AND requires 1 operand")
        
        src_type, src_val = self.parse_operand(operands[0])
        
        a = self.get_operand_value(src_type, src_val)
        b = self.registers.get("b")
        
        result = bool(a) and bool(b)
        self.registers.set("b", result)
    
    def _execute_or(self, operands):
        """Execute OR instruction"""
        if len(operands) != 1:
            raise ValueError("OR requires 1 operand")
        
        src_type, src_val = self.parse_operand(operands[0])
        
        a = self.get_operand_value(src_type, src_val)
        b = self.registers.get("b")
        
        result = bool(a) or bool(b)
        self.registers.set("b", result)
    
    def _execute_jmp(self, operands):
        """Execute JMP instruction"""
        if len(operands) != 1:
            raise ValueError("JMP requires 1 operand")
        
        target = int(operands[0])
        if 0 <= target < len(self.program):
            self.registers.set("pc", target)
        else:
            raise ValueError(f"Jump target {target} out of range")
    
    def _execute_jmpif(self, operands):
        """Execute JMPIF instruction"""
        if len(operands) != 1:
            raise ValueError("JMPIF requires 1 operand")
        
        if self.registers.get("b"):
            target = int(operands[0])
            if 0 <= target < len(self.program):
                self.registers.set("pc", target)
            else:
                raise ValueError(f"Jump target {target} out of range")
        
    def _execute_out(self, operands):
        if len(operands) != 1:
            raise ValueError("OUT requires 1 operand")
        typ, val = self.parse_operand(operands[0])
        value = self.get_operand_value(typ, val)
        self.output_handler.print_output(f"OUT: {value}")

    def _execute_in(self, operands):
        if len(operands) != 1:
            raise ValueError("IN requires 1 operand")
        typ, val = self.parse_operand(operands[0])
        input_val = self.input_handler.read_keyboard_input(f"IN for {operands[0]}: ")
        self.set_operand_value(typ, val, int(input_val))  # nebo podle potřeby typ

    def _execute_push(self, operands):
        if len(operands) != 1:
            raise ValueError("PUSH requires 1 operand")
        typ, val = self.parse_operand(operands[0])
        value = self.get_operand_value(typ, val)
        self.memory.memory.append(value)  # pokud používáte deque nebo list

    def _execute_pop(self, operands):
        if len(operands) != 1:
            raise ValueError("POP requires 1 operand")
        typ, val = self.parse_operand(operands[0])
        if self.memory.memory:
            value = self.memory.memory.pop(0)
            self.set_operand_value(typ, val, value)
        # else: leave unchanged

    def _execute_pp(self, operands):
        # žádné operandy
        if not self.memory.memory:
            return
        value = self.memory.memory.pop(0)
        self.memory.memory.insert(0, value)

    def _execute_not(self, operands):
        if len(operands) != 1 or operands[0] != 'b':
            raise ValueError("NOT only works for b")
        value = self.registers.get('b')
        self.registers.set('b', not value)

    # === JEDNOQUBITOVÉ BRÁNY ===

    def _execute_h(self, operands):
        """Execute Hadamard gate"""
        if len(operands) != 1:
            raise ValueError("H requires 1 operand")
        qubit = self.parse_qubit(operands[0])
        if self.mode == "quantum":
            self.alu.h_gate(qubit)

    def _execute_x(self, operands):
        """Execute Pauli-X gate"""
        if len(operands) != 1:
            raise ValueError("X requires 1 operand")
        qubit = self.parse_qubit(operands[0])
        if self.mode == "quantum":
            self.alu.x_gate(qubit)

    def _execute_y(self, operands):
        """Execute Pauli-Y gate"""
        if len(operands) != 1:
            raise ValueError("Y requires 1 operand")
        qubit = self.parse_qubit(operands[0])
        if self.mode == "quantum":
            self.alu.y_gate(qubit)

    def _execute_z(self, operands):
        """Execute Pauli-Z gate"""
        if len(operands) != 1:
            raise ValueError("Z requires 1 operand")
        qubit = self.parse_qubit(operands[0])
        if self.mode == "quantum":
            self.alu.z_gate(qubit)

    def _execute_s(self, operands):
        """Execute S gate (phase π/2)"""
        if len(operands) != 1:
            raise ValueError("S requires 1 operand")
        qubit = self.parse_qubit(operands[0])
        if self.mode == "quantum":
            self.alu.s_gate(qubit)

    def _execute_t(self, operands):
        """Execute T gate (phase π/4)"""
        if len(operands) != 1:
            raise ValueError("T requires 1 operand")
        qubit = self.parse_qubit(operands[0])
        if self.mode == "quantum":
            self.alu.t_gate(qubit)

    def _execute_rx(self, operands):
        """Execute X-rotation gate"""
        if len(operands) != 2:
            raise ValueError("RX requires 2 operands: angle qubit")
        angle = float(operands[0])
        qubit = self.parse_qubit(operands[1])
        if self.mode == "quantum":
            self.alu.rx_gate(qubit, angle)

    def _execute_ry(self, operands):
        """Execute Y-rotation gate"""
        if len(operands) != 2:
            raise ValueError("RY requires 2 operands: angle qubit")
        angle = float(operands[0])
        qubit = self.parse_qubit(operands[1])
        if self.mode == "quantum":
            self.alu.ry_gate(qubit, angle)

    def _execute_rz(self, operands):
        """Execute Z-rotation gate"""
        if len(operands) != 2:
            raise ValueError("RZ requires 2 operands: angle qubit")
        angle = float(operands[0])
        qubit = self.parse_qubit(operands[1])
        if self.mode == "quantum":
            self.alu.rz_gate(qubit, angle)

    # === DVOUQUBITOVÉ BRÁNY ===

    def _execute_cx(self, operands):
        """Execute CNOT gate"""
        if len(operands) != 2:
            raise ValueError("CX requires 2 operands")
        control = self.parse_qubit(operands[0])
        target = self.parse_qubit(operands[1])
        if self.mode == "quantum":
            self.alu.cnot_gate(control, target)

    def _execute_cz(self, operands):
        """Execute Controlled-Z gate"""
        if len(operands) != 2:
            raise ValueError("CZ requires 2 operands")
        control = self.parse_qubit(operands[0])
        target = self.parse_qubit(operands[1])
        if self.mode == "quantum":
            self.alu.cz_gate(control, target)

    def _execute_cy(self, operands):
        """Execute Controlled-Y gate"""
        if len(operands) != 2:
            raise ValueError("CY requires 2 operands")
        control = self.parse_qubit(operands[0])
        target = self.parse_qubit(operands[1])
        if self.mode == "quantum":
            self.alu.cy_gate(control, target)

    def _execute_ccx(self, operands):
        """Execute Toffoli (CCX) gate"""
        if len(operands) != 3:
            raise ValueError("CCX requires 3 operands")
        control1 = self.parse_qubit(operands[0])
        control2 = self.parse_qubit(operands[1])
        target = self.parse_qubit(operands[2])
        if self.mode == "quantum":
            self.alu.ccx_gate(control1, control2, target)

    def _execute_swap(self, operands):
        """Execute SWAP gate"""
        if len(operands) != 2:
            raise ValueError("SWAP requires 2 operands")
        q1 = self.parse_qubit(operands[0])
        q2 = self.parse_qubit(operands[1])
        if self.mode == "quantum":
            self.alu.swap_gate(q1, q2)

    # === MĚŘENÍ A RESET ===

    def _execute_measure(self, operands):
        """Execute measurement"""
        if len(operands) != 2:
            raise ValueError("MEASURE requires 2 operands: qubit register")
        qubit = self.parse_qubit(operands[0])
        reg_type, reg_val = self.parse_operand(operands[1])
        
        if self.mode == "quantum":
            result = self.quantum_registers.measure(qubit)
            self.set_operand_value(reg_type, reg_val, result)

    def _execute_reset(self, operands):
        """Execute qubit reset"""
        if len(operands) != 1:
            raise ValueError("RESET requires 1 operand")
        qubit = self.parse_qubit(operands[0])
        if self.mode == "quantum":
            self.quantum_registers.set(qubit, 0)  # Reset to |0⟩

    # === KVANTOVÉ ALGORITMY ===

    def _execute_bell(self, operands):
        """Create Bell state between two qubits"""
        if len(operands) != 2:
            raise ValueError("BELL requires 2 operands")
        q1 = self.parse_qubit(operands[0])
        q2 = self.parse_qubit(operands[1])
        if self.mode == "quantum":
            self.alu.create_bell_state(q1, q2)

    def _execute_qft(self, operands):
        """Execute Quantum Fourier Transform"""
        if len(operands) < 1:
            raise ValueError("QFT requires at least 1 operand")
        qubits = [self.parse_qubit(op) for op in operands]
        if self.mode == "quantum":
            self.alu.quantum_fourier_transform(qubits)

    # === POMOCNÉ FUNKCE ===

    def parse_qubit(self, operand):
        """Parse qubit notation q0, q1, etc."""
        if operand.startswith('q') and operand[1:].isdigit():
            qubit_num = int(operand[1:])
            if 0 <= qubit_num < self.quantum_registers.num_qubits:
                return qubit_num
            else:
                raise ValueError(f"Qubit {qubit_num} out of range")
        else:
            raise ValueError(f"Invalid qubit: {operand}")

    def print_quantum_state(self):
        """Print current quantum state for debugging"""
        if self.mode == "quantum":
            state = self.quantum_registers.get_full_state()
            self.output_handler.print_output("=== Quantum State ===")
            for i, amplitude in enumerate(state):
                if abs(amplitude) > 1e-10:  # Only show non-zero amplitudes
                    binary = format(i, f'0{self.quantum_registers.num_qubits}b')
                    self.output_handler.print_output(f"|{binary}⟩: {amplitude:.4f}")
            
            # Show probabilities for each qubit
            self.output_handler.print_output("=== Qubit Probabilities ===")
            for q in range(self.quantum_registers.num_qubits):
                prob_0 = self.quantum_registers.get_probability(q, 0)
                prob_1 = self.quantum_registers.get_probability(q, 1)
                self.output_handler.print_output(f"q{q}: |0⟩={prob_0:.4f}, |1⟩={prob_1:.4f}")
        
    def step(self):
        """Execute one instruction"""
        if not self.program:
            self.output_handler.print_error("No program loaded")
            return False
        
        pc = self.registers.get("pc")
        if pc >= len(self.program):
            self.output_handler.print_output("Program finished")
            self.running = False
            return False
        
        instruction = self.program[pc]
        self.execute_instruction(instruction)
        
        # Increment PC unless changed by jump
        if self.registers.get("pc") == pc:
            self.registers.set("pc", pc + 1)
        
        return True


    def run(self):
        """Run the processor"""
        self.running = True
        self.output_handler.print_output("Starting...")
        while self.running:
            if not self.step():
                break
        self.output_handler.print_output("Stopped")