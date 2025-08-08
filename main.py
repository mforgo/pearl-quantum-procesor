# main.py

import pygame

from src.rendering import render_main
from src.procesor import Procesor
from src.io.gui_output_handler import GUIOutputHandler
from src.io.gui_input_handler import GUIInputHandler
from copy import copy
from src.parsing import parsing

def convert_piquang_to_assembly(piquang_code):
    """
    Convert Piquang code to assembly.
    This is a placeholder implementation - you can expand this based on your Piquang language specification.
    """
    # For now, just return the code as-is (treating it as assembly)
    # You can implement the actual conversion logic here
    code = parsing.Parse(parsing.Tokenize(piquang_code))
    return code

def main():
    pygame.init()
    rendering = render_main.RenderMain()
    highlight_line = None
    
    # Create custom output and input handlers for GUI integration
    gui_output_handler = GUIOutputHandler(rendering)
    gui_input_handler = GUIInputHandler(rendering)
    
    # Toggleable debug mode - set to False to disable debug output
    debug_mode = False
    cpu = Procesor(debug=debug_mode, custom_output_handler=gui_output_handler, custom_input_handler=gui_input_handler, mode="hybrid")

    cpu_running = ""  # Track CPU run state: "", "run", or "step"
    memory_display = ""
    mod = 0

    code_idk = []
    with open("src/parsing/code.txt", "r", encoding="utf-8") as f:
        code_idk = f.read().split("\n")
    
    print(code_idk)
    rendering.set_code(code_idk)

    while True:
        now = pygame.time.get_ticks()
        rendering.clock.tick(20)  # Limit to ~20 FPS
        rendering.set_highlight_line(highlight_line)

        # Debug output - only show when debug_mode is True
        if debug_mode:
            print(cpu.registers.regs)
            print("Memory contents:")
            if cpu.memory.memory:  
                for address, value in sorted(cpu.memory.memory.items()):
                    print(f"  Address {address}: {value}")
            else:
                print("  Memory is empty")
        
        # Format memory for rendering display
        if cpu.memory.memory:
            memory_lines = []
            for address, value in sorted(cpu.memory.memory.items()):
                memory_lines.append(f"{address}: {value}")
            memory_display = ", ".join(memory_lines)
        else:
            memory_display = "Memory is empty"

        registers = copy(cpu.registers.regs)
        registers[7] = cpu.registers.get("b")

        if not rendering.run(memory_display, registers):
            break  # Exit main loop if GUI is closed
        
        # Check if processor wants input
        waiting_for_input = cpu.input_handler.is_waiting()
        
            
            # Check if console has input ready (when Enter is pressed)
        if not rendering.is_console_waiting_for_input():
            input_value = rendering.get_console_input()
            if input_value is not None:
                # Process the input value
                try:
                    input_int = int(input_value)
                    # Set the input value for the CPU to use
                    cpu.input_handler.pending_input = input_int
                    # Reset the waiting state
                    cpu.input_handler.waiting_for_input = False
                except ValueError:
                    rendering.add_console_text(f"Invalid input: {input_value}")
                    # Reset the waiting state even for invalid input
                    cpu.input_handler.waiting_for_input = False
        
        # Activate console and show input prompt when waiting for input
        if waiting_for_input and cpu_running != "":
            # Request console input (shows "in:" prompt automatically)
            rendering.request_console_input()

        # Normal CPU execution - only if not waiting for input
        if not waiting_for_input:
            # Disable console input when program is not running
            if cpu_running == "":
                rendering.console_window.waiting_for_input = False
                rendering.console_window.input_buffer = ""
            
            start = rendering.get_buttons()
            
            # Start CPU run or step on button presses and load program code from GUI editor
            if start["run"] or cpu_running == "run":
                if cpu_running == "":
                    # Load program from GUI code editor string to processor
                    code_info = rendering.get_code_with_language()
                    program_code = code_info["code"]
                    current_language = code_info["language"]
                    
                    # Handle different languages
                    if current_language == "piquang":
                        # Convert Piquang to assembly (placeholder for now)
                        program_code = convert_piquang_to_assembly(program_code)
                        rendering.set_code(program_code.split("\n"))
                        continue
                    
                    if not cpu.load_program_from_string(program_code):
                        rendering.set_console_text("Error loading program from GUI editor.")
                        cpu_running = ""
                        continue
                    # Clear console when starting new program
                    rendering.clear_console()
                    cpu_running = "run"
                    mod = copy(now)
                if now - mod > 1000:
                    mod = copy(now)
                    highlight_line = cpu.get_current_source_line()
                    cpu.step()  # Step once to initialize
            if cpu_running == "step" and start["step"]:
                highlight_line = cpu.get_current_source_line()
                cpu.step()
            elif start["step"]:
                if cpu_running == "":
                    cpu_running = "step"
                    code_info = rendering.get_code_with_language()
                    program_code = code_info["code"]
                    current_language = code_info["language"]
                    
                    # Handle different languages
                    if current_language == "piquang":
                        # Convert Piquang to assembly (placeholder for now)
                        program_code = convert_piquang_to_assembly(program_code)
                    
                    if not cpu.load_program_from_string(program_code):
                        rendering.set_console_text("Error loading program from GUI editor.")
                        cpu_running = ""
                        continue
                    # Clear console when starting new program
                    rendering.clear_console()
                    highlight_line = cpu.get_current_source_line()
                    cpu.step()
            if start["stop"]:
                highlight_line = None
                # Debug output - only show when debug_mode is True
                if debug_mode:
                    print("stop")
                cpu_running = ""
                cpu.registers.regs = [0, 0, 0, 0, 0, 0, 0, 0]
                # Clear console when stopping
                rendering.clear_console()
            
            # Debug output - only show when debug_mode is True
            if debug_mode:
                print(cpu_running)
                print(start)
        
        # Debug output - only show when debug_mode is True
        if debug_mode:
            print(cpu_running)
            print(start)

if __name__ == "__main__":
    main()
