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
