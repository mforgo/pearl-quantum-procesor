import pygame

pygame.init()

screen = pygame.display.set_mode((400, 300))

# Two clocks
fast_clock = pygame.time.Clock()  # 20 FPS
slow_clock = pygame.time.Clock()  # 1 FPS

fast_timer = 0
slow_timer = 0

running = True
while running:
    now = pygame.time.get_ticks()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fast loop stuff (20 FPS)
    fast_clock.tick(20)
    if now - fast_timer >= 50:  # ~20Hz
        print("Fast update")
        fast_timer = now

    # Slow loop stuff (1 FPS)
    if now - slow_timer >= 1000:  # 1Hz
        print("Slow update")
        slow_timer = now

    # Drawing etc.
    screen.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()