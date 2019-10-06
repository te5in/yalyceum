import pygame

pygame.init()

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
white = pygame.Color('white')

def draw():
    red()
    rectPoint = ((51, 100), (350, 60))
    pygame.draw.line(screen, white, (50, 450), (50, 100))
    pygame.draw.rect(screen, white, rectPoint)
    blue()

def red():
    pygame.draw.rect(screen, pygame.Color('red'), ((50, 220), (350, 60)))
def blue():
    pygame.draw.rect(screen, pygame.Color('blue'), ((50, 160), (350, 60)))

draw()

while pygame.event.wait().type != pygame.QUIT:
    pygame.display.flip()

pygame.quit()
