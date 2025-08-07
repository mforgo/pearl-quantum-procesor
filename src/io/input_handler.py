# io/input_handler.py

import sys

class InputHandler:
    def __init__(self):
        self.input_buffer = []
    
    def read_keyboard_input(self, prompt="Enter input: "):
        """Read input from keyboard"""
        try:
            user_input = input(prompt)
            return user_input
        except KeyboardInterrupt:
            print("\nInput interrupted")
            return None
        except EOFError:
            print("\nEnd of input")
            return None
    
    def read_file_input(self, filename):
        """Read input from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file '{filename}' not found")
        except IOError as e:
            raise IOError(f"Error reading input file: {e}")

    def load_program_from_string(self, program_str):
        """
        Load a program given as a multiline string of instructions.

        Args:
            program_str (str): ASM code as a multiline string.
        
        Returns:
            bool: True if loading succeeded, False otherwise.
        """
        try:
            # Use the existing program_loader's internal parsing method if available
            # Otherwise, parse manually here by splitting lines etc.

            # If your ProgramLoader has a method to parse from string, use it:
            if hasattr(self.program_loader, 'parse_program_str'):
                self.program = self.program_loader.parse_program_str(program_str)
            else:
                # Basic fallback: parse lines manually
                lines = [line.strip() for line in program_str.strip().splitlines() if line.strip() and not line.strip().startswith('#')]
                instructions = []
                for line in lines:
                    # Simple parser: split opcode and operands
                    # Adjust parsing logic to match your actual assembler syntax and parser
                    parts = line.split()
                    opcode = parts[0]
                    operands = parts[1:] if len(parts) > 1 else []
                    instructions.append({"opcode": opcode, "operands": operands})
                self.program = instructions

            self.registers.set("pc", 0)
            self.clock = 0  # reset clock if you have it
            self._debug_print(f"Loaded {len(self.program)} instructions from string")
            return True
        except Exception as e:
            self.output_handler.print_error(f"Failed to load program from string: {e}")
            return False

    
    def buffer_input(self, data):
        """Add data to input buffer"""
        if isinstance(data, str):
            self.input_buffer.extend(data.split('\n'))
        else:
            self.input_buffer.append(str(data))
    
    def get_buffered_input(self):
        """Get next item from input buffer"""
        if self.input_buffer:
            return self.input_buffer.pop(0)
        return None
    
    def has_buffered_input(self):
        """Check if there's buffered input available"""
        return len(self.input_buffer) > 0
    
    def clear_buffer(self):
        """Clear input buffer"""
        self.input_buffer.clear()
