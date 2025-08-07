# main.py
import pygame
from src.rendering import render_main
from src.procesor import Procesor  

def main():
    rendering = render_main.RenderMain()
    cpu = Procesor()
    # cpu.run()
    while True:
        now = pygame.time.get_ticks()
        rendering.clock.tick(20)
        if now % 1000 == 0:
            print("Main loop running at 1 FPS")

        if not rendering.run():
            break

    pygame.quit()


if __name__ == "__main__":
    main()
