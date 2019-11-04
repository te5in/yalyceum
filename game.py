import pygame
import sys, os
import random

SCREEN = pygame.Rect((0, 0, 800, 640))
SV_GRAVITY = pygame.math.Vector2(0, 0.3)
TILE = 32

level = ["WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
         "W       E                                  W",
         "W      WWWW                                W",
         "W                      B                   W",
         "W                OOOOOOOOOOOOO             W",
         "W                                          W",
         "W                                          W",
         "W       B                                  W",
         "W    OOOOOOOO                              W",
         "W                                          W",
         "W                      B   OOOOOOO         W",
         "W                 OOOOOO                   W",
         "W                                          W",
         "W         OOOOOOO                          W",
         "W                                          W",
         "W                     OOOOOO               W",
         "W                                          W",
         "W   OOOOOOOOOOO                            W",
         "W                        B                 W",
         "W                 OOOOOOOOOOO              W",
         "W                                          W",
         "W                                          W",
         "W                                          W",
         "W                                    B     W",
         "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW", ]


class Camera(pygame.sprite.LayeredUpdates):
    def __init__(self, target, world_size):
        super().__init__()
        self.target = target
        self.cam = pygame.math.Vector2(0, 0)
        self.world_size = world_size
        self.lost_sprites = []
        if self.target:
            self.add(target)

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + SCREEN.width / 2
            y = -self.target.rect.center[1] + SCREEN.height / 2
            self.cam += 0.1 * (pygame.Vector2(x, y) - self.cam)
            self.cam.x = max(-(self.world_size.width - SCREEN.width), min(0, self.cam.x))
            self.cam.y = max(-(self.world_size.height - SCREEN.height), min(0, self.cam.y))

    def draw(self, surface):
        sprite_dict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lost_sprites

        dirty_append = dirty.append
        init_rect = self._init_rect
        for sprite in self.sprites():
            rec = sprite_dict[sprite]
            new_rect = surface_blit(sprite.image, sprite.rect.move(self.cam))
            if rec is init_rect:
                dirty_append(new_rect)
            else:
                if new_rect.colliderect(rec):
                    dirty_append(new_rect.union(rec))
                else:
                    dirty_append(new_rect)
                    dirty_append(rec)
            sprite_dict[sprite] = new_rect
        return dirty


class Thing(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((TILE, TILE))
        self.rect = self.image.get_rect(topleft=pos)


class Player(Thing):
    def __init__(self, platforms, bukas, pos):
        super().__init__(pos)
        player_image = load_image('mario.png')
        self.image = player_image
        self.vel = pygame.Vector2(0, 0)
        self.onGround = False
        self.platforms = platforms
        self.bukas = bukas
        self.speed = 8
        self.jump_strength = 10
        self.x_vel = self.y_vel = 0

    def update(self):
        pressed = pygame.key.get_pressed()
        up = pressed[pygame.K_UP]
        left = pressed[pygame.K_LEFT]
        right = pressed[pygame.K_RIGHT]
        running = pressed[pygame.K_SPACE]

        if up:
            if self.onGround:
                self.vel.y = -self.jump_strength
        if left:
            self.vel.x = -self.speed
        if right:
            self.vel.x = self.speed
        if running:
            self.vel.x *= 1.5
        if not self.onGround:
            self.vel += SV_GRAVITY
            if self.vel.y > 100:
                self.vel.y = 100
        if not (left or right):
            self.vel.x = 0

        self.rect.left += self.vel.x
        self.collide(self.vel.x, 0, self.platforms, self.bukas)
        self.rect.top += self.vel.y
        self.onGround = False
        self.collide(0, self.vel.y, self.platforms, self.bukas)

    def collide(self, x_vel, y_vel, platforms, bukas):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, Princess):
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                if x_vel > 0:
                    self.rect.right = p.rect.left
                if x_vel < 0:
                    self.rect.left = p.rect.right
                if y_vel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.y_vel = 0
                if y_vel < 0:
                    self.rect.top = p.rect.bottom
                if isinstance(p, Platform):
                    if p.rect[1] < self.rect[1]:
                        p.kill()
        for b in bukas:
            if pygame.sprite.collide_rect(self, b):
                if isinstance(b, Buka):
                    if b.rect[1] > self.rect[1]:
                        b.kill()
                    else:
                        self.kill()
                        pygame.event.post(pygame.event.Event(pygame.QUIT))



class Princess(Thing):
    def __init__(self, pos, *groups):
        super().__init__(pos, *groups)
        princess_image = load_image('princess.png')
        self.image = princess_image


class Buka(Thing):
    def __init__(self, pos, platforms, *groups):
        super().__init__(pos, *groups)
        player_image = load_image('buka.png')
        self.image = player_image
        self.vel = pygame.Vector2(int(random.choice([-1, 1])), 0)
        self.onGround = True
        self.platforms = platforms

    def update(self):
        if not self.onGround:
            self.vel += SV_GRAVITY
            if self.vel.y > 100:
                self.vel.y = 100

        self.rect.left += self.vel.x
        self.collide(self.vel.x, 0, self.platforms)
        self.rect.top += self.vel.y
        self.onGround = False
        self.collide(0, self.vel.y, self.platforms)

    def collide(self, x_vel, y_vel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if x_vel > 0:
                    self.rect.right = p.rect.left
                    self.vel.x *= -1
                if x_vel < 0:
                    self.rect.left = p.rect.right
                    self.vel.x *= -1
                if y_vel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.y_vel = 0
                if y_vel < 0:
                    self.rect.top = p.rect.bottom


class Wall(Thing):
    def __init__(self, pos, *groups):
        super().__init__(pos, *groups)
        wall_image = load_image('wall.png')
        self.image = wall_image


class Platform(Thing):
    def __init__(self, pos, *groups):
        super().__init__(pos, *groups)
        brick_image = load_image('brick.png')
        self.image = brick_image
        self.exist = True


def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
    return image


def level_draw(level, platforms, bukas, entities):
    x = 0
    y = 0
    buka = list()
    for row in level:
        for col in row:
            if col == "O":
                Platform((x, y), platforms, entities)
            elif col == "E":
                Princess((x, y), platforms, entities)
            elif col == "W":
                Wall((x, y), platforms, entities)
            elif col == "B":
                buka.append(Buka((x, y), platforms, bukas, entities))

            x += TILE
        y += TILE
        x = 0


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)
    pygame.display.set_caption("ur princess is in another castle!")
    timer = pygame.time.Clock()

    # level = []
    # for i in range(24):
    #     s = ""
    #     a = random.randint(0, 24)
    #     b = random.randint(0, 48)
    #     for j in range(48):
    #         if i == 0 or j == 0 or i == 23 or j == 47:
    #             s += "O"
    #         elif a <= j <= b:
    #             s += "O"
    #         else:
    #             s += " "
    #     level.append(s)

    platforms = pygame.sprite.Group()
    bukas = pygame.sprite.Group()
    player = Player(platforms, bukas, (TILE, TILE))
    width = len(level[0]) * TILE
    height = len(level) * TILE
    entities = Camera(player, pygame.Rect(0, 0, width, height))

    level_draw(level, platforms, bukas, entities)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit_game()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                exit_game()

        entities.update()

        screen.fill((0, 0, 0))
        entities.draw(screen)
        pygame.display.update()
        timer.tick(100)


def exit_game():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
