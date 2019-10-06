import pygame

pygame.init()

size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def draw():
    pygame.draw.line(screen, pygame.Color('white'), (50, 450), (50, 100))
    blue()

def blue():
    pygame.draw.rect(screen, pygame.Color('blue'), ((50, 160), (350, 60)))

draw()

while pygame.event.wait().type != pygame.QUIT:
    pygame.display.flip()

pygame.quit()
