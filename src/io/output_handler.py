# io/output_handler.py

import sys
from datetime import datetime

class OutputHandler:
    def __init__(self, log_to_file=False, log_filename="processor_output.log"):
        self.log_to_file = log_to_file
        self.log_filename = log_filename
        self.output_buffer = []
        
        if self.log_to_file:
            self._init_log_file()
    
    def _init_log_file(self):
        """Initialize log file with header"""
        try:
            with open(self.log_filename, 'w', encoding='utf-8') as file:
                file.write(f"# Processor Output Log - {datetime.now()}\n\n")
        except IOError as e:
            print(f"Warning: Could not initialize log file: {e}")
            self.log_to_file = False
    
    def print_output(self, message, end='\n'):
        """Print to console"""
        print(message, end=end)
        sys.stdout.flush()
        
        if self.log_to_file:
            self._log_to_file(message + end)
    
    def print_error(self, error_message):
        """Print error message to stderr"""
        print(f"ERROR: {error_message}", file=sys.stderr)
        sys.stderr.flush()
        
        if self.log_to_file:
            self._log_to_file(f"ERROR: {error_message}\n")
    
    def print_debug(self, debug_message, debug_enabled=False):
        """Print debug message if debug is enabled"""
        if debug_enabled:
            print(f"DEBUG: {debug_message}")
            
            if self.log_to_file:
                self._log_to_file(f"DEBUG: {debug_message}\n")
    
    def write_to_file(self, filename, content):
        """Write content to specified file"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
        except IOError as e:
            raise IOError(f"Error writing to file '{filename}': {e}")
    
    def append_to_file(self, filename, content):
        """Append content to specified file"""
        try:
            with open(filename, 'a', encoding='utf-8') as file:
                file.write(content)
        except IOError as e:
            raise IOError(f"Error appending to file '{filename}': {e}")
    
    def _log_to_file(self, message):
        """Internal method to log to file"""
        try:
            with open(self.log_filename, 'a', encoding='utf-8') as file:
                file.write(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        except IOError:
            pass  # Silently fail if logging doesn't work
    
    def buffer_output(self, message):
        """Add message to output buffer"""
        self.output_buffer.append(message)
    
    def flush_buffer(self):
        """Print all buffered output"""
        for message in self.output_buffer:
            self.print_output(message)
        self.output_buffer.clear()
    
    def clear_buffer(self):
        """Clear output buffer without printing"""
        self.output_buffer.clear()
