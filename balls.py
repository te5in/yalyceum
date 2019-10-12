import pygame
import random

BLACK = (0, 0, 0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
BALL_SIZE = 10


class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def make_ball(x, y):
    ball = Ball()

    ball.x = x
    ball.y = y

    return ball


def main():
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Падающие шары")

    done = False

    clock = pygame.time.Clock()

    ball_list = []

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ball = make_ball(event.pos[0], event.pos[1])
                ball_list.append(ball)

        for ball in ball_list:
            if not ball.y > SCREEN_HEIGHT - BALL_SIZE - 2:
                ball.y += 1

        screen.fill(BLACK)

        for ball in ball_list:
            pygame.draw.circle(screen, ball.color, [ball.x, ball.y], BALL_SIZE)

        clock.tick(100)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()