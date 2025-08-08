# io/gui_output_handler.py

class GUIOutputHandler:
    """
    Custom output handler that sends output to the GUI console.
    """
    def __init__(self, rendering_system):
        self.rendering = rendering_system
    
    def print_output(self, message, end='\n'):
        """Send output to GUI console"""
        if self.rendering:
            self.rendering.add_console_text(message)
    
    def print_error(self, error_message):
        """Send error to GUI console"""
        if self.rendering:
            self.rendering.add_console_text(f"ERROR: {error_message}")
    
    def print_debug(self, debug_message, debug_enabled=False):
        """Send debug message to GUI console if enabled"""
        if debug_enabled and self.rendering:
            self.rendering.add_console_text(f"DEBUG: {debug_message}")
    
    def buffer_output(self, message):
        """Add message to output buffer (not used in GUI)"""
        pass
    
    def flush_buffer(self):
        """Flush output buffer (not used in GUI)"""
        pass
    
    def clear_buffer(self):
        """Clear output buffer (not used in GUI)"""
        pass
