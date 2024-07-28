import pygame
import numpy as np
from math import *

# Defining colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Screen
WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Rendering points
scale = 100
circle_pos = [WIDTH/2, HEIGHT/2]  # x, y

# Rotating
angle = 0

points = []

# all the vertices for cube
points.append(np.matrix([-1, -1, 1]))
points.append(np.matrix([1, -1, 1]))
points.append(np.matrix([1,  1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))


projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]   # line not necessary
])


projected_points = [
    [n, n] for n in range(len(points))
]


def connect_points(i, j, points):
    pygame.draw.line(screen, BLACK,
                     (points[i][0], points[i][1]),
                     (points[j][0], points[j][1]))

# limiting frame rate
clock = pygame.time.Clock()
while True:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # Basic 3D rotations from this wiki page:
    # https://en.wikipedia.org/wiki/Rotation_matrix
    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])
    angle += 0.01

    screen.fill(WHITE)

    # Drawing stuff & points in array
    i = 0
    for point in points:
        # .reshape helps us read cube vertices from 1D arrays to 2D array
        rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)

        projected2d = np.dot(projection_matrix, rotated2d)

        # x, y are projected coordinates
        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, RED, (x, y), 5)
        i += 1

    # Connecting cube dots algorithm
    for p in range(4):
        # For every point add one line until 4th p is reached
        # Used for dots 0, 1, 2, 3 to make 1st square
        connect_points(p, (p+1) % 4, projected_points)
        # Used for dots 4, 5, 6, 7 to make 2nd square
        connect_points(p+4, ((p+1) % 4) + 4, projected_points)
        # Used to connect both squares and make a 3D cube
        connect_points(p, (p+4), projected_points)

    pygame.display.update()