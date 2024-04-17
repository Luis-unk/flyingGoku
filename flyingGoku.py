# -*- coding: utf-8 -*-
import pygame
import random
from pygame.locals import *

# Definição das constantes do jogo
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 200

class Goku(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.speed = SPEED

        self.current_image = 0

        self.image = pygame.image.load("pngwing.com.png").subsurface(0, 104, 34, 44).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):   

        self.speed += GRAVITY

        # Update height
        self.rect[1] += self.speed
    
    def bump(self):
        self.speed = -SPEED

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH,PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
    
    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load('fundo2.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

goku_group = pygame.sprite.Group()
goku = Goku()
goku_group.add(goku)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()

# Botão para iniciar o jogo
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (200, 200, 200)
BUTTON_TEXT_COLOR = (0, 0, 0)
BUTTON_TEXT = 'Iniciar Jogo'
FONT_SIZE = 30
font = pygame.font.Font(None, FONT_SIZE)
BUTTON_X = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
BUTTON_Y = (SCREEN_HEIGHT - BUTTON_HEIGHT) // 2

# Variável para controlar o estado do jogo
game_started = False

while not game_started:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT:
                game_started = True

    screen.blit(BACKGROUND, (0, 0))

    # Desenha o botão na tela
    pygame.draw.rect(screen, BUTTON_COLOR, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    text_surface = font.render(BUTTON_TEXT, True, BUTTON_TEXT_COLOR)

        # Desenha o texto do botão na tela
    text_rect = text_surface.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
    screen.blit(text_surface, text_rect)

    pygame.display.update()

# Loop principal do jogo
running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                goku.bump()

    screen.blit(BACKGROUND, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(SCREEN_WIDTH * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    goku_group.update()
    ground_group.update()
    pipe_group.update()

    goku_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update() 

    if (pygame.sprite.groupcollide(goku_group, ground_group, False, False, pygame.sprite.collide_mask) or
       pygame.sprite.groupcollide(goku_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        
        # Game over
        running = False

pygame.quit()

