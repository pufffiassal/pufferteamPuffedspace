import pygame
import random
import sys

# Inicializáció
pygame.init()

# Képernyő mérete
WIDTH, HEIGHT = 1600, 900

# Színek
WHITE = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
IDK = (70, 130, 10)

# Játékablak létrehozása
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puffedspace")

clock = pygame.time.Clock()


# Karakterválasztó menü háttere
character_menu_img = pygame.image.load("character_menu.png")
character_menu_img = pygame.transform.scale(character_menu_img, (WIDTH, HEIGHT))

# Karakterek listája
characters = [
    pygame.image.load("character1.png"),
    pygame.image.load("character2.png"),
    pygame.image.load("character3.png")
]

# Karakterek méretének módosítása
for i in range(len(characters)):
    characters[i] = pygame.transform.scale(characters[i], (50, 50))

# Kiválasztott karakter indexe
selected_character = 0

# Kezdőmenü megjelenítése
character_menu = True
while character_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            character_menu = False  # Karakterválasztó menü bezárása és elindítása a játék

    screen.blit(character_menu_img, (0, 0))

    # Karakterek megjelenítése a karakterválasztó menüben
    for i, character in enumerate(characters):
        character_rect = character.get_rect()
        character_rect.topleft = (30 + i * 70, HEIGHT - 200)
        screen.blit(character, character_rect)

        # Ha a játékos rákattint egy karakterre a menüben
        if character_rect.collidepoint(pygame.mouse.get_pos()):
            selected_character = i

    pygame.display.flip()

# Űrhajó kép betöltése és méretének módosítása a választott karakterrel
spaceship_img = characters[selected_character]
spaceship_rect = spaceship_img.get_rect()
spaceship_rect.centerx = WIDTH // 2
spaceship_rect.centery = HEIGHT - 50

# Akadályok listája
obstacles = []

# Akadályok létrehozása
def create_obstacle():
    obstacle = pygame.Rect(random.randint(0, WIDTH - 50), 0, 50, 50)
    obstacles.append(obstacle)

# Lövedékek listája
bullets = []

# Lövés cooldown és következő lövési időpont inicializálása
cooldown = 3  # 3 másodperces cooldown
next_shot_time = 0

# Lövedék létrehozása
def create_bullet():
    bullet = pygame.Rect(spaceship_rect.centerx - 5, spaceship_rect.y - 20, 10, 20)
    bullets.append({"rect": bullet, "speed": -10})  # Hozzáadjuk a lövedékhez a sebességét is

# Szörnyök listája
enemies = []

# Szörnyök létrehozása
class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 50), 0, 50, 50)
        self.speed = 5

    def move(self):
        self.rect.y += self.speed

    def can_shoot(self):
        # Itt meghatározhatod, mikor lő a szörny
        # Példa: minden 2 másodpercben
        return pygame.time.get_ticks() % 500 < 10

    def shoot(self):
        # Itt hozd létre és mozgasd a szörny lövedékét
        # Példa:
        enemy_bullet = pygame.Rect(self.rect.centerx, self.rect.bottom, 10, 20)
        enemy_bullets.append(enemy_bullet)

# Szorzók listája
multipliers = []

# Szorzók létrehozása
class Multiplier:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 50), 0, 20, 20)
        self.speed = 5

    def apply_effect(self):
        global score_multiplier, score_multiplier_timer
        score_multiplier = 2
        score_multiplier_timer = pygame.time.get_ticks() + 5000  # 5 másodpercig tart a hatás

# Szörny lövedékek listája
enemy_bullets = []

# Szörny lövedék létrehozása
def create_enemy_bullet(enemy):
    enemy_bullet = pygame.Rect(enemy.rect.centerx, enemy.rect.bottom, 10, 20)
    enemy_bullets.append(enemy_bullet)

# Szorzó lövedékek listája
multiplier_bullets = []

# Szorzó lövedék létrehozása
def create_multiplier_bullet(multiplier):
    multiplier_bullet = pygame.Rect(multiplier.rect.centerx, multiplier.rect.bottom, 10, 20)
    multiplier_bullets.append(multiplier_bullet)

# Restart menü
def restart_game():
    global spaceship_rect, obstacles, bullets, score, game_over, kozmic_hp, cooldown
    spaceship_rect.centerx = WIDTH // 2
    spaceship_rect.centery = HEIGHT - 50
    obstacles = []
    bullets = []
    enemies = []
    multipliers = []
    score = 0
    game_over = False
    kozmic_hp = 3  # Kozmic életerje visszaállítása
    cooldown = 3  # Lövési cooldown visszaállítása
    score_multiplier = 1
    score_multiplier_timer = 0

# Hanghatások betöltése
death_sound = pygame.mixer.Sound("death_sound.wav")
shoot_sound = pygame.mixer.Sound("shoot_sound.wav")
multiplier_sound = pygame.mixer.Sound("multiplier_sound.wav")  # Új hangeffekt a szorzókhoz
damage_sound = pygame.mixer.Sound("damage_sound.wav")  # Új hangeffekt a sebzéshez

# Pontszám
score = 0

# Játékállapot
game_over = False

# Háttérzene betöltése
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.9)  # Hangerejének beállítása (0.0 - 1.0)
pygame.mixer.music.play(-1)  # Végtelen ismétlés

# Kozmic életereje
kozmic_hp = 3

# Pontszám szorzó és időzítő
score_multiplier = 1
score_multiplier_timer = 0


# Font inicializálása
font = pygame.font.Font(None, 36)


# Óra inicializálása
clock = pygame.time.Clock()


# Fő játék ciklus
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                spaceship_rect.x -= 20
            if event.key == pygame.K_RIGHT:
                spaceship_rect.x += 20
            if event.key == pygame.K_SPACE:
                if pygame.time.get_ticks() >= next_shot_time:
                    create_bullet()  # Lövés létrehozása
                    shoot_sound.play()  # Lövés hanghatás lejátszása
                    next_shot_time = pygame.time.get_ticks() + cooldown * 1000  # Következő lövési időpont beállítása

    if not game_over:
        # Akadályok mozgatása
        for obstacle in obstacles:
            obstacle.y += 10

        # Szörnyök mozgatása és lövés
        for enemy in enemies:
            enemy.move()
            if enemy.can_shoot():
                create_enemy_bullet(enemy)

        # Szörnyök lövedékek mozgatása
        for enemy_bullet in enemy_bullets:
            enemy_bullet.y += 10

        # Szorzók mozgatása
        for multiplier in multipliers:
            multiplier.rect.y += multiplier.speed

        # Lövedékek mozgatása
        for bullet in bullets:
            bullet["rect"].y += bullet["speed"]

        # Szorzó lövedékek mozgatása
        for multiplier_bullet in multiplier_bullets:
            multiplier_bullet.y += 10

        # Új akadályok, szorzók és szörnyek létrehozása
        if random.randint(0, 100) < 5:
            create_obstacle()
        if random.randint(0, 100) < 2:
            multiplier = Multiplier()
            multipliers.append(multiplier)
        if random.randint(0, 100) < 2:
            enemy = Enemy()
            enemies.append(enemy)

        # Ütközések ellenőrzése a fő karakter és az akadályok között
        for obstacle in obstacles:
            if spaceship_rect.colliderect(obstacle):
                game_over = True
                death_sound.play()  # Halál hanghatás lejátszása
                damage_sound.play()  # Sebzés hanghatás lejátszása

        # Ütközés ellenőrzése a lövedékek és az akadályok között
        for bullet in bullets:
            for obstacle in obstacles:
                if bullet["rect"].colliderect(obstacle):
                    bullets.remove(bullet)
                    obstacles.remove(obstacle)
                    score += 10 * score_multiplier  # Pontszám növelése a szorzóval

        # Ütközés ellenőrzése a fő karakter és a szorzók között
        for multiplier in multipliers:
            if spaceship_rect.colliderect(multiplier.rect):
                # Itt kezelheted a szorzók felvételét és pontszám növelését
                multipliers.remove(multiplier)
                multiplier.apply_effect()
                score_multiplier = 2
                multiplier_sound.play()  # Hangeffekt lejátszása a szorzó felvételénél

        # Ütközés ellenőrzése a fő karakter és a szörny lövedékek között
        for enemy_bullet in enemy_bullets:
            if spaceship_rect.colliderect(enemy_bullet):
                kozmic_hp -= 1
                enemy_bullets.remove(enemy_bullet)
                if kozmic_hp <= 0:
                    game_over = True
                    death_sound.play()
                    damage_sound.play()  # Sebzés hanghatás lejátszása

        # Ütközés ellenőrzése a szörnyök lövedékei és a lövedékek között
        for enemy_bullet in enemy_bullets:
            for bullet in bullets:
                if enemy_bullet.colliderect(bullet["rect"]):
                    enemy_bullets.remove(enemy_bullet)
                    bullets.remove(bullet)

        # Ütközés ellenőrzése a szörnyök és a lövedékek között
        for enemy in enemies:
            for bullet in bullets:
                if enemy.rect.colliderect(bullet["rect"]):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 10 * score_multiplier  # Pontszám növelése a szorzóval

        # Pontszám szorzó időzítő kezelése
        if pygame.time.get_ticks() > score_multiplier_timer:
            score_multiplier = 1

        # Képernyő frissítése
        screen.fill(WHITE)
        screen.blit(spaceship_img, spaceship_rect)

        # Akadályok rajzolása
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, obstacle)

        # Lövedékek rajzolása kék színnel
        for bullet in bullets:
            pygame.draw.rect(screen, (0, 0, 255), bullet["rect"])  # Kék szín (RGB: 0, 0, 255)

        # Szorzók rajzolása sárga színnel
        for multiplier in multipliers:
            pygame.draw.rect(screen, (255, 255, 0), multiplier.rect)  # Sárga szín (RGB: 255, 255, 0)

        # Szörnyök rajzolása piros színnel
        for enemy in enemies:
            pygame.draw.rect(screen, IDK, enemy.rect)

        # Szörny lövedékek rajzolása piros színnel
        for enemy_bullet in enemy_bullets:
            pygame.draw.rect(screen, RED, enemy_bullet)

        # Pontszám megjelenítése
        score_text =font.render(f"Pontszám: {score}", True, GREEN)
        screen.blit(score_text, (10, 10))

        # Kozmic életerjének megjelenítése
        hp_text = font.render(f"Kozmic HP: {kozmic_hp}", True, GREEN)
        screen.blit(hp_text, (WIDTH - 170, 10))

        # Lövés cooldown szöveg megjelenítése
        cooldown_text = font.render(f"Lövés cooldown: {max(0, int((next_shot_time - pygame.time.get_ticks()) / 1000))}s", True, GREEN)
        screen.blit(cooldown_text, (10, 50))

        # Szorzó hatásának időzítőjének megjelenítése
        if pygame.time.get_ticks() < score_multiplier_timer:
            multiplier_timer_text = font.render(f"Szorzó hatása: {int((score_multiplier_timer - pygame.time.get_ticks()) / 1000)}s", True, GREEN)
            screen.blit(multiplier_timer_text, (WIDTH - 250, 50))

    else:
        # Restart menü háttere
        screen.fill(WHITE)

        # Restart menü képének megjelenítése
        restart_button_img = pygame.image.load("restart_button.png")
        restart_button_img = pygame.transform.scale(restart_button_img, (600, 900))
        restart_button_rect = restart_button_img.get_rect()
        restart_button_rect.centerx = WIDTH // 2
        restart_button_rect.centery = HEIGHT // 2
        screen.blit(restart_button_img, restart_button_rect)

        # Kiválasztott karakter képének megjelenítése
        if selected_character is not None:
            selected_character_image = characters[selected_character]
            selected_character_rect = selected_character_image.get_rect()
            selected_character_rect.center = (WIDTH // 2, HEIGHT // 2 - 50)
            screen.blit(selected_character_image, selected_character_rect)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    restart_game()
                    selected_character = None

    pygame.display.flip()
    clock.tick(30)
