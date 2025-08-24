import pygame
import random
import cv2
import numpy as np

# Initialize Pygame
pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("DVD Bouncing Logo")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('screen_recording.mov', fourcc, 30.0, (WIDTH, HEIGHT))

logos = [
    pygame.transform.scale(pygame.image.load("LOGOS/ROBOSTORE+Unitree_logo-White.png"), (400, 75)),
    pygame.transform.scale(pygame.image.load("/Users/kamilszwed/Documents/robostore/LOGOS/ROBOSTORE_gears_icon-White.png"), (100, 100)),
    pygame.transform.scale(pygame.image.load("LOGOS/ROBOSTORE+Unitree_logo-White.png"), (400, 75)),
    pygame.transform.scale(pygame.image.load("/Users/kamilszwed/Documents/robostore/LOGOS/ROBOSTORE_gears_icon-White.png"), (100, 100))
]

logo_sizes = [
    (400, 75),
    (100, 100),
    (400, 75),
    (100, 100)
]

logo_idx = random.randint(0, len(logos) - 1)
x, y = random.randint(0, WIDTH - logo_sizes[logo_idx][0]), random.randint(0, HEIGHT - logo_sizes[logo_idx][1])
speed_x, speed_y = 5, 5

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the logo
    x += speed_x
    y += speed_y

    # Get current logo size
    current_width, current_height = logo_sizes[logo_idx]

    hit_corner = False
    if x <= 0 or x + current_width >= WIDTH:
        speed_x = -speed_x
        hit_corner = True
    if y <= 0 or y + current_height >= HEIGHT:
        speed_y = -speed_y
        hit_corner = True

    if hit_corner:
        logo_idx = random.randint(0, len(logos) - 1)
        current_width, current_height = logo_sizes[logo_idx]
        x = min(max(x, 0), WIDTH - current_width)
        y = min(max(y, 0), HEIGHT - current_height)

    screen.fill((0, 0, 0))
    screen.blit(logos[logo_idx], (x, y))
    pygame.display.flip()

    frame = pygame.surfarray.array3d(pygame.display.get_surface())
    frame = np.rot90(frame)
    frame = np.flip(frame, axis=1)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    out.write(frame)

    clock.tick(60)

# Release video writer and quit
out.release()
pygame.quit()

