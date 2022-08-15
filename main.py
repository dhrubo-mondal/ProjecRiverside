import pygame
from os import path, walk, mkdir, getenv
from random import randint


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
    def __init__(self, value, sc):
        super().__init__()

        if value == 'golem_1':
            self.frames = []
            for _, _, image in walk(path.join("assets", "images", "enemy", "golem_1")):
                for i in image:
                    image_surf = pygame.transform.scale(
                        pygame.image.load(path.join("assets", "images", "enemy", "golem_1", i)).convert_alpha(),
                        (75, 85))
                    self.frames.append(image_surf)
            self.speed = 5 + sc // 20
        elif value == 'golem_2':
            self.frames = []
            for _, _, image in walk(path.join("assets", "images", "enemy", "golem_2")):
                for i in image:
                    image_surf = pygame.transform.scale(
                        pygame.image.load(path.join("assets", "images", "enemy", "golem_2", i)).convert_alpha(),
                        (75, 85))
                    self.frames.append(image_surf)
            self.speed = 5 + sc // 20
        elif value == 'golem_3':
            self.frames = []
            for _, _, image in walk(path.join("assets", "images", "enemy", "golem_3")):
                for i in image:
                    image_surf = pygame.transform.scale(
                        pygame.image.load(path.join("assets", "images", "enemy", "golem_3", i)).convert_alpha(),
                        (75, 85))
                    self.frames.append(image_surf)
            self.speed = 5 + sc // 20

        elif value == 'big_golem_1':
            self.frames = []
            for _, _, image in walk(path.join("assets", "images", "enemy", "golem_1")):
                for i in image:
                    image_surf = pygame.transform.scale(
                        pygame.image.load(path.join("assets", "images", "enemy", "golem_1", i)).convert_alpha(),
                        (95, 105))
                    self.frames.append(image_surf)
            self.speed = 6 + sc // 20
        elif value == 'big_golem_2':
            self.frames = []
            for _, _, image in walk(path.join("assets", "images", "enemy", "golem_2")):
                for i in image:
                    image_surf = pygame.transform.scale(
                        pygame.image.load(path.join("assets", "images", "enemy", "golem_2", i)).convert_alpha(),
                        (95, 105))
                    self.frames.append(image_surf)
            self.speed = 6 + sc // 20
        else:
            self.frames = []
            for _, _, image in walk(path.join("assets", "images", "enemy", "golem_3")):
                for i in image:
                    image_surf = pygame.transform.scale(
                        pygame.image.load(path.join("assets", "images", "enemy", "golem_3", i)).convert_alpha(),
                        (95, 105))
                    self.frames.append(image_surf)
            self.speed = 6 + sc // 20

        self.plane = 535
        self.score = 0
        self.animation_index = 0
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
    global hit_sound
    global game_over_sound
    if pygame.sprite.spritecollide(player.sprite, enemy, True, pygame.sprite.collide_mask):
        heart -= 1
        if heart == 0:
            enemy.empty()
            game_over_sound.play()
            return 0
        else:
            hit_sound.play()
            return 1
    else:
        return 1


def display_score(x, y, draw_board, instance_font):
    text = instance_font.render("Score: " + str(score), True, (241, 211, 202))
    text_rect = text.get_rect(center=(x, y))
    board_surface = pygame.transform.scale(
        pygame.image.load(path.join("assets", "images", "ui", "board.png")).convert_alpha(), (250, 180))
    board_rect_element = board_surface.get_rect(center=(width // 2, -10))
    if draw_board:
        screen.blit(board_surface, board_rect_element)
    screen.blit(text, text_rect)


def display_stats(hs, tp, font_instance):
    text_1 = font_instance.render("Highscore: " + str(hs), True, (241, 211, 202))
    text_1_rect = text_1.get_rect(center=(width // 2, height // 2 - 80))
    screen.blit(text_1, text_1_rect)

    sec = tp // 1000
    temp_min = sec // 60

    hr = temp_min // 60
    temp_min = temp_min - (hr * 60)
    sec = sec - (temp_min * 60)

    text_1 = font_instance.render("Time Played: " + str(hr) + "h " + str(temp_min) + "m " + str(sec) + "s",
                                  True, (241, 211, 202))
    text_1_rect = text_1.get_rect(center=(width // 2, height // 2 - 40))
    screen.blit(text_1, text_1_rect)


def display_heart(display, heart_val):
    health_bar = pygame.transform.scale(
        pygame.image.load(path.join("assets", "images", "ui", f"health_{heart_val}.png")).convert_alpha(), (180, 26))
    health_bar_rect = health_bar.get_rect(topleft=(10, 10))
    display.blit(health_bar, health_bar_rect)


def read_property():
    global file_exists
    global file_location

    if file_exists:
        file = open(file_location, "rt")
        read = file.readlines()
        file.close()
        return read
    else:
        write_property()
        return [0, 0, 1]


def write_property(val_score=0, val_time=0, music=1):
    global file_exists
    global file_location
    lines = [val_score, val_time, music]

    if file_exists:
        file = open(file_location, "wt")
        for line in lines:
            file.writelines(str(line) + "\n")
        file.close()
    else:
        if not path.exists(path.join(getenv("APPDATA"), "Riverside", "data")):
            mkdir(path.join(getenv("APPDATA"), "Riverside"))
            mkdir((file_location[0:len(file_location) - 9]).rstrip("\\").rstrip("/"))
            file_exists = True
        else:
            file_exists = True
        write_property()


def get_font(size):
    return pygame.font.Font(path.join("assets", "fonts", "evil_empire.ttf"), size)


pygame.init()

width, height = 1000, 9 * 1000 // 16

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Riverside")

running = True
menu_pressed = False
file_location = path.join(getenv("APPDATA"), "Riverside", "data", "value.txt")
file_exists = path.exists(file_location)
game_state = 1
score = 0
heart = 5

data_val = read_property()
high_score = int(data_val[0])
time_played = int(data_val[1])
music_playing = int(data_val[2])

# The sounds
heal_sound = pygame.mixer.Sound(path.join("assets", "sounds", "game-heal-sound.mp3"))
jump_sound = pygame.mixer.Sound(path.join("assets", "sounds", "game-jump-sound.mp3"))
hit_sound = pygame.mixer.Sound(path.join("assets", "sounds", "game-hit-sound.mp3"))
button_sound = pygame.mixer.Sound(path.join("assets", "sounds", "game-button-sound.mp3"))
game_over_sound = pygame.mixer.Sound(path.join("assets", "sounds", "game-over-sound.mp3"))

if music_playing == 1:
    music_y = 36
    no_music_y = -100
    music_2_y = (height // 2) + 80
    no_music_2_y = -100
    heal_sound.set_volume(1)
    jump_sound.set_volume(1)
    hit_sound.set_volume(1)
    button_sound.set_volume(1)
    game_over_sound.set_volume(0.25)
else:
    music_y = -100
    no_music_y = 36
    music_2_y = -100
    no_music_2_y = (height // 2) + 80
    heal_sound.set_volume(0)
    jump_sound.set_volume(0)
    hit_sound.set_volume(0)
    button_sound.set_volume(0)
    game_over_sound.set_volume(0)

clock = pygame.time.Clock()

# Game over screen elements
black_screen = pygame.Surface((width, height))
black_screen.set_alpha(200)
black_screen_rect = black_screen.get_rect(topleft=(0, 0))

board_surf = pygame.transform.scale(
    pygame.image.load(path.join("assets", "images", "ui", "board.png")), (400, 350))
board_rect = board_surf.get_rect(center=(width // 2, height // 2))

plate_surf = pygame.transform.scale(
    pygame.image.load(path.join("assets", "images", "ui", "plate.png")), (340, 120))
plate_rect = plate_surf.get_rect(center=(width // 2, height // 2 - 60))

plate_2_surf = pygame.transform.scale(
    pygame.image.load(path.join("assets", "images", "ui", "plate.png")), (340, 150))
plate_2_rect = plate_2_surf.get_rect(center=(width // 2, height // 2 - 55))

music_surf = pygame.transform.scale(
    pygame.image.load(path.join("assets", "images", "ui", "music.png")), (60, 60))
music_rect = music_surf.get_rect(center=(width - 70, music_y))

no_music_surf = pygame.transform.scale(
    pygame.image.load(path.join("assets", "images", "ui", "no_music.png")), (60, 60))
no_music_rect = no_music_surf.get_rect(center=(width - 70, no_music_y))

retry_surf = pygame.transform.scale(
    pygame.image.load(path.join("assets", "images", "ui", "retry.png")), (90, 90))
retry_rect = retry_surf.get_rect(center=(width // 2, (height // 2) + 80))

info_surf = pygame.transform.scale(
    pygame.image.load(path.join("assets", "images", "ui", "info.png")), (90, 90))
info_rect = info_surf.get_rect(center=(width // 2 - 110, (height // 2) + 80))

music_surf_2 = pygame.transform.scale(
    pygame.image.load(path.join("assets", "images", "ui", "music.png")), (90, 90))
music_rect_2 = music_surf_2.get_rect(center=(width // 2 + 110, music_2_y))

no_music_surf_2 = pygame.transform.scale(
    pygame.image.load(path.join("assets", "images", "ui", "no_music.png")), (90, 90))
no_music_rect_2 = no_music_surf_2.get_rect(center=(width // 2 + 110, no_music_2_y))

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == 1:
            if event.type == pygame.KEYDOWN and player.sprite.rect.bottom >= int(
                    player.sprite.__getattribute__("plane")):
                jump_sound.play()
            if event.type == heal:
                if heart < 5:
                    list_heart = [1, 0, 2]
                    h_index = probability([950, 40, 10])
                    if h_index == 2 and heart == 4:
                        heart += 1
                        heal_sound.play()
                    else:
                        heart += list_heart[h_index]
                        heal_sound.play()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if music_rect.collidepoint(pygame.mouse.get_pos()):
                    button_sound.play()
                    music_playing = 0
                    no_music_y = 36
                    music_y = -100
                    music_2_y = -100
                    no_music_2_y = (height // 2) + 80
                    heal_sound.set_volume(0)
                    jump_sound.set_volume(0)
                    hit_sound.set_volume(0)
                    button_sound.set_volume(0)
                    game_over_sound.set_volume(0)

                if no_music_rect.collidepoint(pygame.mouse.get_pos()):
                    music_playing = 1
                    music_y = 36
                    no_music_y = -100
                    music_2_y = (height // 2) + 80
                    no_music_2_y = -100
                    heal_sound.set_volume(1)
                    jump_sound.set_volume(1)
                    hit_sound.set_volume(1)
                    button_sound.set_volume(1)
                    game_over_sound.set_volume(0.25)

            if event.type == score_update:
                score += 1

            if event.type == spawn_enemy:
                enemy_list = ["golem_1", "golem_2", "golem_3", "big_golem_1", "big_golem_2", "big_golem_3"]
                enemy_name = enemy_list[probability([500, 400, 100, 50, 40, 10])]
                enemy.add(Enemy(enemy_name, score))

        if game_state == 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if info_rect.collidepoint(pygame.mouse.get_pos()):
                    button_sound.play()
                    if menu_pressed:
                        menu_pressed = False
                    else:
                        menu_pressed = True

                if retry_rect.collidepoint(pygame.mouse.get_pos()):
                    button_sound.play()
                    score = 0
                    game_state = 1
                    heart = 5
                    enemy.empty()

                if music_rect_2.collidepoint(pygame.mouse.get_pos()):
                    button_sound.play()
                    no_music_y = 36
                    music_y = -100
                    music_playing = 0
                    music_2_y = -100
                    no_music_2_y = (height // 2) + 80
                    heal_sound.set_volume(0)
                    jump_sound.set_volume(0)
                    hit_sound.set_volume(0)
                    button_sound.set_volume(0)
                    game_over_sound.set_volume(0)

                if no_music_rect_2.collidepoint(pygame.mouse.get_pos()):
                    music_playing = 1
                    no_music_y = -100
                    music_y = 36
                    music_2_y = (height // 2) + 80
                    no_music_2_y = -100
                    heal_sound.set_volume(1)
                    jump_sound.set_volume(1)
                    hit_sound.set_volume(1)
                    button_sound.set_volume(1)
                    game_over_sound.set_volume(0.25)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    score = 0
                    game_state = 1
                    heart = 5
                    enemy.empty()

    # Drawing the background
    background.draw(screen)
    background.update()

    if game_state == 1:
        # Drawing the player
        player.draw(screen)
        player.update()

        # Drawing the enemy
        enemy.draw(screen)
        enemy.update()

        # Drawing the score
        display_score(width // 2, 34, True, get_font(50))

        # Checking collision
        game_state = check_collision()

        # Drawing the health bar
        display_heart(screen, heart)

        # Drawing the music button
        music_rect.center = (width - 40, music_y)
        screen.blit(music_surf, music_rect)
        no_music_rect.center = (width - 40, no_music_y)
        screen.blit(no_music_surf, no_music_rect)

    if game_state == 0:
        screen.blit(black_screen, black_screen_rect)
        screen.blit(board_surf, board_rect)
        screen.blit(info_surf, info_rect)
        screen.blit(retry_surf, retry_rect)

        # Drawing the music button
        music_rect_2.center = (width // 2 + 110, music_2_y)
        screen.blit(music_surf_2, music_rect_2)
        no_music_rect_2.center = (width // 2 + 110, no_music_2_y)
        screen.blit(no_music_surf_2, no_music_rect_2)

        if not menu_pressed:
            screen.blit(plate_surf, plate_rect)
            display_score(width // 2, 220, False, get_font(50))
        else:
            screen.blit(plate_2_surf, plate_2_rect)
            display_stats(high_score, time_played, get_font(30))

    if score > high_score:
        high_score = score

    pygame.display.update()
    clock.tick(60)

# Update after game window is closed
time_played += pygame.time.get_ticks()
write_property(high_score, time_played, music_playing)
