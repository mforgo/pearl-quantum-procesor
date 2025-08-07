# main.py
import pygame
from src.rendering import render_main
from src.procesor import Procesor  

def main():
    rendering = render_main.RenderMain()
    cpu = Procesor()
    cpu_running = ""
    cpu.status()
    cpu.step()
    while True:
        now = pygame.time.get_ticks()
        rendering.clock.tick(20)
        if now % 1000 == 0:
            print("Main loop running at 1 FPS")

        if not rendering.run():
            break

        start = rendering.get_buttons()
        if start["run"] or cpu_running == "run":
            if cpu_running == "":
                code = rendering.get_code()
                print(f"Loading code: {code}")
                cpu.input_handler.load_program_from_string(code)
                cpu_running = "run"
                cpu.step()
            elif cpu_running == "run":
                cpu.step()
        elif start["step"]:
            if cpu_running == "":
                code = rendering.get_code()
                print(f"Loading code: {code}")
                cpu.input_handler.load_program_from_string(code)
                cpu_running = "step"
            elif cpu_running == "step":
                cpu.step()
        elif start["stop"]:
            cpu_running = ""
        
        status = cpu.status(include_registers=True, include_ram=True)
        try:
            rendering.set_registers(status['registers'].items())
            rendering.set_memory(status['ram'].items())
        except Exception as e:
            pass

    pygame.quit()


if __name__ == "__main__":
    main()
