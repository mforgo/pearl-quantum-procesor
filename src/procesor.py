# src/procesor.py

from src.alu import ClassicalALU, QuantumALU
from src.memory import ClassicalMemory
from src.registers import ClassicalRegisters
from src.io import InputHandler, OutputHandler, ProgramLoader

class Procesor:
    def __init__(self, mode="classical", debug=False):
        """
        Initialize the processor
        
        Args:
            mode: "classical" or "quantum" 
            debug: Enable debug output
        """
        self.mode = mode
        self.debug = debug
        self.running = False
        
        # Initialize components
        self.registers = ClassicalRegisters()
        self.memory = ClassicalMemory()
        self.input_handler = InputHandler()
        self.output_handler = OutputHandler(log_to_file=debug)
        self.program_loader = ProgramLoader()
        
        # Initialize ALU based on mode
        if mode == "quantum":
            self.alu = QuantumALU(num_qubits=4)
        else:
            self.alu = ClassicalALU(bit_width=8)
        
        # Program and execution state
        self.program = []
        self.current_instruction = 0
        
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