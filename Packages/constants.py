import pygame

WIDTH, HEIGHT = 750, 750
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (220,20,60)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (93, 63, 211)
GREY = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load(r'S:\Projects\Programing Projects\-\Projects\Rockets\assets\crown.png'), (50, 50))
ROCKET = pygame.transform.scale(pygame.image.load(r'S:\Projects\Programing Projects\-\Projects\Rockets\assets\EjSEK-wUwAAKjMm.png'), (20, 20))

