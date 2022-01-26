import pygame
import sys
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, window, width, height):
        super().__init__()
        self.window = window
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.image.fill(self.generate_random_color())
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(100, 796)
        self.rect.y = random.randrange(100, 412)

        # attributes
        self.alive = True
        self.speed = 4
        self.health = 100
        self.score = 0

    def update(self):
        self.movement()

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.rect.y > 0 + 60:
                self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.rect.y < 512 - self.height - 20:
                self.rect.y += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.rect.x > 0 + 20:
                self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.rect.x < 896 - self.width - 20:
                self.rect.x += self.speed
        if keys[pygame.K_ESCAPE]:
            sys.exit()

    def generate_random_color(self):
        color_values = []
        for i in range(3):
            randomNumber = random.randrange(1, 255)
            color_values.append(randomNumber)
        color = tuple(color_values)
        
        return color

class Enemy(pygame.sprite.Sprite):
    def __init__(self, window, width, height, x, y):
        super().__init__()
        self.window = window
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # attributes
        self.alive = True
        self.health = 100
        self.speed = 1.7

    def update(self):
        self.movement()
        self.collision()

    def movement(self):
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        if self.rect.y > player.rect.y:
            self.rect.y -= self.speed

    def collision(self):
        if self.rect.colliderect(player.rect):
            player.health -= 1
            if player.health == 0:
                player.alive = False

class Coin(pygame.sprite.Sprite):
    def __init__(self, window, width, height):
        super().__init__()
        self.window = window
        self.width = width
        self.height = height
        self.alive = True
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(100, 796)
        self.rect.y = random.randrange(100, 412)

    def update(self):
        if player.rect.colliderect(self.rect):
            player.score += 1
            self.alive = False
            self.kill()

        if len(coin_group) == 0:
            add_coins()

        if player.score == 50:
            enemy.speed = 1.8
        elif player.score == 100:
            enemy.speed = 1.9
        elif player.score == 150:
            enemy.speed = 2
        elif player.score == 200:
            player.speed = 5.5
            enemy.speed = 2.1

# window settings
pygame.init()
width, height = 896, 512
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Block Runner 2D")
clock = pygame.time.Clock()

# player
player = Player(window, 40, 40)
player_group = pygame.sprite.Group()
player_group.add(player)

# enemy
enemy_group = pygame.sprite.Group()   
enemy = Enemy(window, 30, 30, 200, 200)
enemy_group.add(enemy)

# coin
coin_group = pygame.sprite.Group()
def add_coins():
    for i in range(10):
        coin = Coin(window, 10, 10)
        coin_group.add(coin)
add_coins()

# health label
font = pygame.font.Font('freesansbold.ttf', 32)
health_label = font.render(f"Health: {player.health}", 1, (0, 0, 0))
health_label_rect = health_label.get_rect()
health_label_rect.center = (100, 20)

# score label
font = pygame.font.Font('freesansbold.ttf', 32)
score_label = font.render(f"Score: {player.score}", 1, (0, 0, 0))
score_label_rect = score_label.get_rect()
score_label_rect.center = (750, 20)

# player died menu
def dead_menu():
    death_font = pygame.font.Font('freesansbold.ttf', 64)
    death_text = death_font.render("YOU DIED!", 1, (255, 255, 255))
    death_textRect = death_text.get_rect()
    death_textRect.center = (width // 2, height // 2 - 100)

    main_menufont = pygame.font.Font('freesansbold.ttf', 32)
    main_menutext = main_menufont.render("MAIN MENU", 1, (255, 255, 255))
    main_menutextRect = main_menutext.get_rect()
    main_menutextRect.center = (width // 2, height // 2)

    quitfont = pygame.font.Font('freesansbold.ttf', 32)
    quittext = quitfont.render("QUIT", 1, (255, 255, 255))
    quittextRect = quittext.get_rect()
    quittextRect.center = (width // 2, height // 2 + 60)
    
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # MOUSE BUTTON PRESSED
            if event.type == pygame.MOUSEBUTTONDOWN:
                # MAIN MENU BUTTON
                if mouse[0] > 355:
                    if mouse[0] < 543:
                        if mouse[1] > 241:
                            if mouse[1] < 265:
                                main_menu()

                # QUIT BUTTON
                if mouse[0] > 409:
                    if mouse [0] < 490:
                        if mouse[1] > 301:
                            if mouse[1] < 326:
                                pygame.quit()
                                sys.exit()

        pygame.display.update()

        window.fill((255, 0, 0))
        window.blit(death_text, death_textRect)
        window.blit(main_menutext, main_menutextRect)
        window.blit(quittext, quittextRect)

        clock.tick(60)

# start menu before game
def main_menu():
    start_menu_bg = pygame.image.load("Assets/background.png")

    # button images
    start_button_img = pygame.image.load("Assets/start-button.png")
    start_button_rect = start_button_img.get_rect()
    start_button_width = start_button_img.get_width()
    start_button_height = start_button_img.get_height()
    start_button_rect.center = (896 / 2, 512 / 2)

    shop_button_img = pygame.image.load("Assets/shop-button.png")
    shop_button_rect = shop_button_img.get_rect()
    shop_button_width = shop_button_img.get_width()
    shop_button_height = shop_button_img.get_height()
    shop_button_rect.center = (896 / 2, 512 / 2 + 60)

    quit_button_img = pygame.image.load("Assets/quit-button.png")
    quit_button_rect = quit_button_img.get_rect()
    quit_button_width = quit_button_img.get_width()
    quit_button_height = quit_button_img.get_height()
    quit_button_rect.center = (896 / 2, 512 / 2 + 120)

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # MOUSE BUTTON HOVER
            
            # start button
            if mouse[0] > 399:
                if mouse[0] < 499:
                    if mouse[1] > 244:
                        if mouse[1] < 269:
                            start_button_img = pygame.image.load("Assets/start-button-hover.png")
                        else:
                            start_button_img = pygame.image.load("Assets/start-button.png")
                    else:
                        start_button_img = pygame.image.load("Assets/start-button.png")
                else:
                    start_button_img = pygame.image.load("Assets/start-button.png")
            else:
                start_button_img = pygame.image.load("Assets/start-button.png")

            # shop button
            # NOT DONE ##############################################################################################

            # quit button
            if mouse[0] > 408:
                if mouse[0] < 489:
                    if mouse[1] > 361:
                        if mouse[1] < 387:
                            quit_button_img = pygame.image.load("Assets/quit-button-hover.png")
                        else:
                            quit_button_img = pygame.image.load("Assets/quit-button.png")
                    else:
                        quit_button_img = pygame.image.load("Assets/quit-button.png")
                else:
                    quit_button_img = pygame.image.load("Assets/quit-button.png")
            else:
                quit_button_img = pygame.image.load("Assets/quit-button.png")

            
            # MOUSE BUTTON PRESSED
            if event.type == pygame.MOUSEBUTTONDOWN:

                # start button
                if mouse[0] > 399:
                    if mouse[0] < 499:
                        if mouse[1] > 244:
                            if mouse[1] < 269:
                                player.alive = True
                                player.health = 100
                                player.score = 0
                                game()

                # shop button
                # NOT DONE ##############################################################################################

                # quit button
                if mouse[0] > 408:
                    if mouse[0] < 489:
                        if mouse[1] > 361:
                            if mouse[1] < 387:
                                pygame.quit()
                                sys.exit()

        pygame.display.update()

        window.blit(start_menu_bg, (0, 0))
        window.blit(start_button_img, start_button_rect)
        window.blit(shop_button_img, shop_button_rect)
        window.blit(quit_button_img, quit_button_rect)

        clock.tick(60)

# main game loop
def game():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

        if player.alive:
            # draw objects to the window
            window.fill((255, 255, 255))

            health_label = font.render(f"Health: {player.health}", 1, (0, 0, 0))
            window.blit(health_label, health_label_rect)

            score_label = font.render(f"Score: {player.score}", 1, (0, 0, 0))
            window.blit(score_label, score_label_rect)

            player_group.draw(window)
            player_group.update()

            coin_group.draw(window)
            coin_group.update()

            enemy_group.draw(window)
            enemy_group.update()
        else:
            dead_menu()

        clock.tick(60)

if __name__ == '__main__':
    main_menu()