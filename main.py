import pygame
import os
import colorsys
import math
from matrix import matrix_multiplication

os.environ["SDL_VIDEO_CENTERED"] = "1"
width, height = 800, 600
size = (width, height)
white, black = (200, 200, 200), (0, 0, 0)
pygame.init()
pygame.display.set_caption("Lorenz Attractor")
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60

sigma = 10
rho = 28
beta = 8/3
x, y, z = 0.01, 0, 0
scale = 8
points = []
angle = 0
previous = None

def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

run=True
while run:
    screen.fill(black)
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    rotation_x = [
        [1, 0, 0], 
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ]

    rotation_y = [
        [math.cos(angle), 0, -math.sin(angle)],
        [0, 1, 0],
        [math.sin(angle), 0, math.cos(angle)]
    ]

    rotation_z = [
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ]

    time = 0.01
    dx = (sigma * (y-x)) * time
    dy = (x * (rho - z) - y) * time
    dz = (x * y - beta * z) * time

    x = x + dx
    y = y + dy
    z = z + dz
    hue = 0

    point = [[x], [y], [z]]
    points.append(point)

    for p in range(len(points)):
        rotated_2d = matrix_multiplication(rotation_y, points[p])
        projection_matrix = [
            [1, 0, 0],
            [0, 1, 0]
        ]
        projected_2d = matrix_multiplication(projection_matrix, rotated_2d)

        x_pos = int(projected_2d[0][0] * scale) + width//2 + 100
        y_pos = int(projected_2d[1][0] * scale) + height//2

        if hue > 1:
            hue = 0

        if previous is not None:
            if hue > 0.006:
                pygame.draw.circle(screen, (hsv2rgb(hue, 1, 1)), (x_pos, y_pos), 2)
       
        previous = (x_pos, y_pos)
        hue += 0.006
    
    # for rotation
    angle += 0.01
    pygame.display.update()

pygame.quit()