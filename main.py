import pygame
from os import path, walk
from random import randint


# Game object classes -----------------------------------------------------------
class Background(pygame.sprite.Sprite):
    def __init__(self, w, h):
        super().__init__()

        self.images = []
        for _, _, image in walk(path.join("assets", "images", "background")):
            for i in image:
                image_surf = pygame.transform.scale(
                    pygame.image.load(path.join("assets", "images", "background", i)).convert(), (w, h))
                self.images.append(image_surf)

        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()

    def animate(self):
        self.image_index += 0.14
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.image = self.images[int(self.image_index)]

    def update(self):
        self.animate()


class Player(pygame.sprite.Sprite):
    def __init__(self, w, h):
        super().__init__()

        self.player_walk = []
        for _, _, image in walk(path.join("assets", "images", "player", "player_run")):
            for i in image:
                image_surf = pygame.transform.scale(
                    pygame.image.load(path.join("assets", "images", "player", "player_run", i)).convert_alpha(), (w, h))
                self.player_walk.append(image_surf)

        self.player_index = 0
        self.player_jump = pygame.transform.scale(
            pygame.image.load(path.join("assets", "images", "player", "player_jump.png")).convert_alpha(), (w, h))
        self.image = self.player_walk[self.player_index]
        self.plane = 536
        self.rect = self.image.get_rect(midbottom=(80, self.plane))
        self.gravity = 0
        self.mask = pygame.mask.from_surface(self.image)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.plane:
            self.rect.bottom = self.plane

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= self.plane:
            self.gravity = -23

    def animate(self):
        if self.rect.bottom < self.plane:
            self.image = self.player_jump
        else:
            self.player_index += 0.18
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.input()
        self.apply_gravity()
        self.animate()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, value):
        super().__init__()

        self.plane = 550
        if value == 'golem_1':
            self.frames = []
            for _, _, image in walk(path.join("assets", "images", "enemy", "golem_1")):
                for i in image:
                    image_surf = pygame.transform.scale(
                        pygame.image.load(path.join("assets", "images", "enemy", "golem_1", i)).convert_alpha(),
                        (75, 85))
                    self.frames.append(image_surf)
            self.plane = 535
            self.speed = 5
        elif value == 'golem_2':
            self.frames = []
            for _, _, image in walk(path.join("assets", "images", "enemy", "golem_2")):
                for i in image:
                    image_surf = pygame.transform.scale(
                        pygame.image.load(path.join("assets", "images", "enemy", "golem_2", i)).convert_alpha(),
                        (75, 85))
                    self.frames.append(image_surf)
            self.plane = 535
            self.speed = 5
        elif value == 'golem_3':
            self.frames = []
            for _, _, image in walk(path.join("assets", "images", "enemy", "golem_3")):
                for i in image:
                    image_surf = pygame.transform.scale(
                        pygame.image.load(path.join("assets", "images", "enemy", "golem_3", i)).convert_alpha(),
                        (75, 85))
                    self.frames.append(image_surf)
            self.plane = 535
            self.speed = 5

        elif value == 'big_golem_1':
            self.frames = []
            for _, _, image in walk(path.join("assets", "images", "enemy", "golem_1")):
                for i in image:
                    image_surf = pygame.transform.scale(
                        pygame.image.load(path.join("assets", "images", "enemy", "golem_1", i)).convert_alpha(),
                        (95, 105))
                    self.frames.append(image_surf)
            self.plane = 536
            self.speed = 6
        elif value == 'big_golem_2':
            self.frames = []
            for _, _, image in walk(path.join("assets", "images", "enemy", "golem_2")):
                for i in image:
                    image_surf = pygame.transform.scale(
                        pygame.image.load(path.join("assets", "images", "enemy", "golem_2", i)).convert_alpha(),
                        (95, 105))
                    self.frames.append(image_surf)
            self.plane = 536
            self.speed = 6
        else:
            self.frames = []
            for _, _, image in walk(path.join("assets", "images", "enemy", "golem_3")):
                for i in image:
                    image_surf = pygame.transform.scale(
                        pygame.image.load(path.join("assets", "images", "enemy", "golem_3", i)).convert_alpha(),
                        (95, 105))
                    self.frames.append(image_surf)
            self.plane = 536
            self.speed = 6

        self.animation_index = 0
        self.score = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(1100, 1500), self.plane))
        self.mask = pygame.mask.from_surface(self.image)

    def animation_state(self):
        self.animation_index += 0.16
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -self.rect.width:
            self.kill()


# Making a probability system for which obstacle to spawn
def probability(weights):
    total_weight = sum(weights)
    rand = randint(1, total_weight)

    for i in range(len(weights)):
        if rand <= weights[i]:
            return i
        else:
            rand -= weights[i]
    return 0


# Checking collision between player and enemy
def check_collision():
    global heart
    if pygame.sprite.spritecollide(player.sprite, enemy, True, pygame.sprite.collide_mask):
        heart -= 1
        if heart == 0:
            enemy.empty()
            return 0
        else:
            return 1
    else:
        return 1


def display_score():
    text = font.render("Score: " + str(score), True, (60, 60, 60))
    text_rect = text.get_rect(center=(width // 2, 40))
    board_surf = pygame.transform.scale(
        pygame.image.load(path.join("assets", "images", "ui", "board.png")).convert_alpha(), (248, 80))
    board_rect = board_surf.get_rect(topleft=(10, 40))
    screen.blit(board_surf, board_rect)
    screen.blit(text, text_rect)


def display_heart(display, heart_val):
    health_bar = pygame.transform.scale(
        pygame.image.load(path.join("assets", "images", "ui", f"health_{heart_val}.png")).convert_alpha(), (180, 26))
    health_bar_rect = health_bar.get_rect(topleft=(10, 10))
    display.blit(health_bar, health_bar_rect)


pygame.init()

width, height = 1000, 9 * 1000 // 16

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Riverside")
font = pygame.font.Font(path.join("assets", "fonts", "evil_empire.ttf"), 50)
running = True
game_state = 1
score = 0
heart = 5

clock = pygame.time.Clock()

# The Sprite groups 
background = pygame.sprite.Group()
background.add(Background(width, height))

player = pygame.sprite.GroupSingle()
player.add(Player(75, 110))

enemy = pygame.sprite.Group()

# User events
spawn_enemy = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_enemy, 2000)

score_update = pygame.USEREVENT + 2
pygame.time.set_timer(score_update, 4000)

heal = pygame.USEREVENT + 3
pygame.time.set_timer(heal, 20000)

while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == 1:
            if event.type == heal:
                if heart < 5:
                    list_heart = [1, 0, 2]
                    h_index = probability([950, 40, 10])
                    if h_index == 2 and heart == 4:
                        heart += 1
                    else:
                        heart += list_heart[h_index]
            if event.type == score_update:
                score += 1
            if event.type == spawn_enemy:
                enemy_list = ["golem_1", "golem_2", "golem_3", "big_golem_1", "big_golem_2", "big_golem_3"]
                enemy_name = enemy_list[probability([500, 400, 100, 50, 40, 10])]
                enemy.add(Enemy(enemy_name))
        if game_state == 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    score = 0
                    game_state = 1
                    heart = 5
                    enemy.empty()

    if game_state == 1:
        # Drawing the background   
        background.draw(screen)
        background.update()

        # Drawing the player
        player.draw(screen)
        player.update()

        # Drawing the enemy
        enemy.draw(screen)
        enemy.update()

        display_score()

        # Checking collision
        game_state = check_collision()

        # Drawing the health bar
        display_heart(screen, heart)

    if game_state == 0:
        pass

    pygame.display.update()
    clock.tick(60)
