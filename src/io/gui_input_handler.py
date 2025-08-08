# io/gui_input_handler.py

class GUIInputHandler:
    """
    Custom input handler that gets input from the GUI console.
    """
    def __init__(self, rendering_system):
        self.rendering = rendering_system
        self.pending_input = None
        self.waiting_for_input = False
    
    def read_keyboard_input(self, prompt="Enter input: "):
        """Request input from GUI console"""
        if self.rendering:
            self.rendering.add_console_text(prompt)
            self.rendering.request_console_input()
            self.waiting_for_input = True
            # Don't return a value yet - wait for actual input
            return None
        return "0"
    
    def check_for_input(self):
        """Check if input is available from GUI console"""
        if self.rendering and not self.rendering.is_console_waiting_for_input():
            input_value = self.rendering.get_console_input()
            if input_value is not None:
                self.waiting_for_input = False
                return input_value
        return None
    
    def is_waiting(self):
        """Check if waiting for input"""
        return self.waiting_for_input
    
    def buffer_input(self, data):
        """Add data to input buffer (not used in GUI)"""
        pass
    
    def get_buffered_input(self):
        """Get next item from input buffer (not used in GUI)"""
        return None
    
    def has_buffered_input(self):
        """Check if there's buffered input available (not used in GUI)"""
        return False
    
    def clear_buffer(self):
        """Clear input buffer (not used in GUI)"""
        pass
