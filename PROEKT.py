import pygame, sys
from all_needed_things import Enemy, balls_collide as b_k
import pygame.freetype #ДЛЯТЕКСТАСМЕРТИ
import random

pygame.init()
window = pygame.display.set_mode((1280,720))

pygame.display.set_caption('my game')

x, y, radius, speed, jump_height, in_jump, in_fall, facing, hp, in_attack, steps_attack = 100, 610, 10, 7, 5, False, True, 1, 12, False, -3
enemies = []

GAME_FONT = pygame.freetype.Font('times.ttf', 60) #ДЛЯТЕКСТА

schetchikcooldowna = 0 # для куллдауна атаки
kovonazhnaC = 0        # это тоже
platforms = [(0,700,1280), (239, 675, 495), (458, 650, 488), (514, 625, 775), (99, 625, 206), (820, 625, 1200), (0, 600, 70)]
run = True

for elem in random.sample(platforms, random.randint(4, 6)): # ГЕНЕРАТОР ВРАГОВ
    if elem != (99, 625, 206):
        radiuse = random.randint(7, 15)
        enemies.append(Enemy(elem[0], elem[1]-radiuse, elem[2], random.randint(elem[0], elem[2]), elem[1]-radiuse, radiuse, random.randint(2, 10), random.randint(10, 20)))
    else:
        continue

while run: # Цикл игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
    if hp == 0:
        GAME_FONT.render_to(window, (450, 300), "ты умер ( ͡° ʖ̯ ͡°)", (255, 50, 50)) #ТЕКСТ СМЕРТИ
        pygame.display.flip() # для текста тож
        pygame.time.delay(1250)
        break
    if len(enemies) == 0:
        GAME_FONT.render_to(window, (450, 300), "ты победил :D", (50, 50, 255)) #ТЕКСТ Победы
        pygame.display.flip() # для текста тож
        pygame.time.delay(1250)
        break
    pygame.time.delay(35)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    if keys[pygame.K_LEFT] and x - radius > 5:
        x -= speed
        facing = -1
    if keys[pygame.K_RIGHT] and x <1275 - radius:
        x += speed
        facing = 1
    if keys[pygame.K_c] and schetchikcooldowna == 0:
        kovonazhnaC += 1 # счетчик нажатий клавиши С, для куллдауна
        in_attack = True
    for elem in platforms:
        if y + radius == elem[1] and (elem[0]<=x<=elem[2]):
            in_fall = False
    if keys[pygame.K_DOWN] and y != 700 - radius:
        in_fall = True
    if not in_jump and not in_fall:
        if keys[pygame.K_SPACE]:
            in_jump = True
            in_fall = True
    if in_jump:
        if jump_height >= -5:
            if jump_height > 0:
                y -= jump_height**2
            elif in_fall:
                y += jump_height**2
            else:
                in_jump = False
                jump_height = 6
            jump_height -= 1
        else:
            in_jump = False
            jump_height = 5
    if in_fall and not in_jump:
        y += 5
    in_fall = True

    if in_attack:                   # атака
        schetchikcooldowna = 9
        if steps_attack != 3:
            y_attack = y - 3
            x_attack = x + facing * 5
            steps_attack += 1
        else:
            steps_attack = -3
            in_attack = False
    elif kovonazhnaC != 0:          # для куллдауна атаки
        while schetchikcooldowna > 0:
            schetchikcooldowna -= 1
            break
    for enemy in enemies:
        enemy.move()
        if b_k((x, y, radius), (enemy.x, enemy.y, enemy.radius)): # отнимаем жизнь у игрока при соприкосновении с врагом
            hp -= 1
        if in_attack:       # отнимаем жизнь у врагов при атаке игрока
            if b_k((x_attack, y_attack, 10), (enemy.x, enemy.y, enemy.radius)):
                enemy.hp -= 1
                if enemy.hp <= 0:
                    enemies.remove(enemy) # враги умирают
    window.fill((0,0,0))
    if in_attack:
        pygame.draw.circle(window, (128, 128, 0), (x_attack, y_attack), 13)
    pygame.draw.circle(window, (0,150,90), (x, y), radius)
    for param in enemies:
        pygame.draw.circle(window, (255,80,80),(param.x, param.y), param.radius) #тут враги
    for elem in platforms:
        pygame.draw.line(window, (0,128,0), (elem[0],elem[1]), (elem[2],elem[1]))
    pygame.display.update()



pygame.quit()
sys.exit()
