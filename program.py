import pygame

pygame.init()

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
white = pygame.Color('white')

def draw():
    rectPoint = ((51, 100), (350, 60))
    pygame.draw.line(screen, white, (50, 450), (50, 100))
    pygame.draw.rect(screen, white, rectPoint)

draw()

while pygame.event.wait().type != pygame.QUIT:
    pygame.display.flip()

pygame.quit()
