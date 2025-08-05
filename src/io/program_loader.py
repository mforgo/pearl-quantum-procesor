# io/program_loader.py

import os
import json

class ProgramLoader:
    def __init__(self):
        self.supported_extensions = ['.asm', '.txt', '.json', '.qasm']
    
    def load_program(self, filename):
        """Load program from file and return as list of instructions"""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Program file '{filename}' not found")
        
        _, ext = os.path.splitext(filename)
        
        if ext not in self.supported_extensions:
            raise ValueError(f"Unsupported file extension '{ext}'. Supported: {self.supported_extensions}")
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                
            if ext == '.json':
                return self._parse_json_program(content)
            else:
                return self._parse_text_program(content)
                
        except IOError as e:
            raise IOError(f"Error reading program file: {e}")
    
    def _parse_text_program(self, content):
        """Parse text-based program (assembly-like)"""
        instructions = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Remove comments and whitespace
            line = line.split('#')[0].strip()
            if not line:
                continue
            
            # Split instruction and operands
            parts = line.split()
            if parts:
                instruction = {
                    'line': line_num,
                    'opcode': parts[0],
                    'operands': parts[1:] if len(parts) > 1 else []
                }
                instructions.append(instruction)
        
        return instructions
    
    def _parse_json_program(self, content):
        """Parse JSON-formatted program"""
        try:
            data = json.loads(content)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'instructions' in data:
                return data['instructions']
            else:
                raise ValueError("JSON program must contain 'instructions' array")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
    
    def save_program(self, instructions, filename, format='text'):
        """Save program to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                if format == 'json':
                    json.dump(instructions, file, indent=2)
                else:
                    for instr in instructions:
                        if isinstance(instr, dict):
                            line = f"{instr['opcode']}"
                            if 'operands' in instr and instr['operands']:
                                line += " " + " ".join(instr['operands'])
                            file.write(line + '\n')
                        else:
                            file.write(str(instr) + '\n')
        except IOError as e:
            raise IOError(f"Error saving program file: {e}")
    
    def validate_program(self, instructions):
        """Basic validation of program structure"""
        valid_opcodes = {
            'mov', 'add', 'sub', 'dvd', 'mul', 'neg',
            'cmp', 'eqq', 'and', 'or', 'jmp', 'jmpif'
        }
        
        errors = []
        
        for i, instr in enumerate(instructions):
            if isinstance(instr, dict):
                opcode = instr.get('opcode', '').lower()
                if opcode not in valid_opcodes:
                    errors.append(f"Line {i+1}: Unknown opcode '{opcode}'")
            else:
                errors.append(f"Line {i+1}: Invalid instruction format")
        
        return errors
    
    def create_sample_program(self, filename):
        """Create a sample program file"""
        sample_program = [
            "# Sample program for Pearl Quantum Processor",
            "mov 5 p0      # Load 5 into register p0",
            "mov 3 p1      # Load 3 into register p1", 
            "add p0 p1     # Add p0 and p1, result in p0",
            "mov p0 h100   # Store result to memory address 100",
            "cmp p0 p1     # Compare p0 > p1, result in b",
            "jmpif 8       # Jump to line 8 if b is true",
            "mov 0 p2      # Set p2 to 0",
            "mov 1 p2      # Set p2 to 1"
        ]
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('\n'.join(sample_program))
