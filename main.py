# main.py

import pygame

from src.rendering import render_main
from src.procesor import Procesor

def main():
    pygame.init()
    rendering = render_main.RenderMain()
    cpu = Procesor(debug=True)
    cpu_running = ""  # Track CPU run state: "", "run", or "step"

    while True:
        now = pygame.time.get_ticks()
        rendering.clock.tick(20)  # Limit to ~20 FPS

        if not rendering.run():
            break  # Exit main loop if GUI is closed

        start = rendering.get_buttons()

        # Start CPU run or step on button presses and load program code from GUI editor
        if start["run"] or cpu_running == "run":
            if cpu_running == "":
                # Load program from GUI code editor string to processor (fixed)
                program_code = rendering.get_code()
                if not cpu.load_program_from_string(program_code):
                    rendering.set_console_text("Error loading program from GUI editor.")
                    cpu_running = ""
                    continue
                cpu_running = "run"
                cpu.step() and now % 1000 == 0  # Step once to initialize
            elif cpu_running == "run":
                cpu.step()
        elif start["step"]: or cpu_running == "step":
            if cpu_running == "":
                program_code = rendering.get_code()
                if not cpu.load_program_from_string(program_code):
                    rendering.set_console_text("Error loading program from GUI editor.")
                    cpu_running = ""
                    continue
                cpu_running = "step"
            cpu.step()
            # After stepping one instruction, stop stepping
            if cpu_running == "step":
                cpu_running = ""

        elif start["stop"]:
            cpu_running = ""

        # Get status info and update GUI register and memory views
        try:
            status = cpu.status(include_registers=True, include_ram=True)
            if 'registers' in status:
                rendering.set_registers(status['registers'].items())
            if 'ram' in status:
                rendering.set_memory(status['ram'].items())
        except Exception as e:
            # Silently catch errors or optionally log
            pass

    pygame.quit()

if __name__ == "__main__":
    main()
