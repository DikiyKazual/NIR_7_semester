import pygame, sys
from all_needed_things import Enemy, Boss, balls_collide as b_k
import pygame.freetype #ДЛЯТЕКСТАСМЕРТИ
import random

pygame.init()
window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

displ = pygame.display.Info()
#1024, 600 1280, 720 1366, 768 1440, 810 1600, 900 1920, 1080 нодвысот6
winx, winy = displ.current_w, displ.current_h

pygame.display.set_caption('my game')

x, y, radius, speed, jump_step, in_jump, in_fall, facing, hp, in_attack, steps_attack, fallspeed = int(winx*0.08), int(winy*0.8), int(winy*0.0146484375), int(winx*0.00875), 5, False, True, 1, 12, False, -3, winy*0.016666667
jump_speed = [0, int(winy * 0.001666667), int(winy * 0.006666667), int(winy * 0.015), int(winy * 0.026666666), int(winy * 0.041666666)]
enemies = []

GAME_FONT = pygame.freetype.Font('times.ttf', 60) #ДЛЯТЕКСТА

cool_down_count, C_press_Count, enemy_cool_down_count = 0, 0, 0  # для куллдауна атаки
D_not_pressed_timer = 100 # это чтобы спрыг вниз нормально работал
win = False # флаг убийства босса
jump_cool_down = 0 # вроде понятно
platforms = [(0,int(winy*0.99),winx), (int(winx*0.18671875), int(winy*0.94), int(winx*0.38671875)), (int(winx*0.33), int(winy*0.89), int(winx*0.40)), (int(winx*0.4015625), int(winy*0.84), int(winx*0.60546875)), (int(winx*0.07734375), int(winy*0.84), int(winx*0.1609375)), (int(winx*0.640625), int(winy*0.84), int(winx*0.9375)), (0, int(winy*0.84), int(winx*0.0546875)), (int(winx*0.2), int(winy*0.79), int(winx*0.7)), (0, int(winy*0.74), int(winx*0.2)), (int(winx*0.7), int(winy*0.74), winx), (0, int(winy*0.59), winx), (int(winx*0.2), int(winy*0.49), int(winx*0.7)), (0, int(winy*0.49), int(winx*0.1)), (int(winx*0.1), int(winy*0.39), int(winx*0.2)), (int(winx*0.3), int(winy*0.39), int(winx*0.8))]
run = True

radiuse = 30
enemies.append(Boss(int(winx*0.3), int(winy*0.39)-radiuse, int(winx*0.8), random.randint(int(winx*0.3), int(winx*0.8)), int(winy*0.39)-radiuse, radiuse, 8, random.randint(50, 100)))

for elem in random.sample(platforms, random.randint(4, 6)): # ГЕНЕРАТОР ВРАГОВ
    if elem != (int(winx*0.07734375), int(winy*0.84), int(winx*0.1609375)) and elem != (int(winx*0.3), int(winy*0.39), int(winx*0.8)):
        radiuse = random.randint(int(winy*0.009722222), int(winy*0.0208333333))
        enemies.append(Enemy(elem[0], elem[1]-radiuse, elem[2], random.randint(elem[0], elem[2]), elem[1]-radiuse, radiuse, random.randint(2, 10), random.randint(10, 20)))
    else:
        continue
clock = pygame.time.Clock()

while run: # Цикл игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
    clock.tick(30)
    if hp == 0:
        GAME_FONT.render_to(window, (int(winx*0.3515625), int(winy*0.4166666666)), "ты умер ( ͡° ʖ̯ ͡°)", (255, 50, 50)) #ТЕКСТ СМЕРТИ
        pygame.display.flip() # для текста тож
        pygame.time.delay(1250)
        break
    if len(enemies) == 0 or win:
        GAME_FONT.render_to(window, (int(winx*0.3515625), int(winy*0.41666666666)), "ты победил :D", (50, 50, 255)) #ТЕКСТ Победы
        pygame.display.flip() # для текста тож
        pygame.time.delay(1250)
        break
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    if keys[pygame.K_LEFT] and x - radius > int(winx*0.00390625):
        x -= speed
        facing = -1
    if keys[pygame.K_RIGHT] and x < int(winx*0.99609375) - radius:
        x += speed
        facing = 1
    if keys[pygame.K_c] and cool_down_count == 0:
        C_press_Count += 1 # счетчик нажатий клавиши С, для куллдауна
        in_attack = True
    for elem in platforms:
        if abs(y + radius - elem[1]) < int(fallspeed + winy * 0.001666667) and y + radius - elem[1] <= 0 and elem[0]<=x<=elem[2] and D_not_pressed_timer > 0: # ЕСЛИ ПРОВАЛИВАЕТСЯ СКВОЗЬ ПЛАТФОРМЫ, ИСПРАВИТЬ  НА
            if not in_jump:
                y -= y + radius - elem[1]
            in_fall = False
            fallspeed = winy*0.0166666667
    if keys[pygame.K_DOWN] and y != int(winy*0.99) - radius and D_not_pressed_timer > 5 and not in_jump:
        D_not_pressed_timer = 0
        in_fall = True
    if D_not_pressed_timer <= 5:
        D_not_pressed_timer += 1
    if not in_jump and not in_fall:
        if keys[pygame.K_SPACE] and jump_cool_down == 0:
            in_jump = True
            in_fall = True
    if in_jump:
        if jump_step >= -5:
            if jump_step >= 0:
                y -= jump_speed[jump_step]
            elif in_fall:
                y += jump_speed[-jump_step]
                if jump_step != -5:
                    for elem in platforms:
                        if abs(y + radius - elem[1]) < jump_speed[-jump_step + 1] and (elem[0]<=x<=elem[2]):
                            y -= y + radius - elem[1]
            else:
                in_jump = False
                jump_step = 6
                jump_cool_down = 2
            jump_step -= 1
        else:
            in_jump = False
            jump_step = 5
            jump_cool_down = 2
    elif jump_cool_down > 0:
        jump_cool_down -= 1
    if in_fall and not in_jump:
        y += int(fallspeed)
        if fallspeed < winy*0.025:
            fallspeed += winy*0.00166666667
    in_fall = True

    if in_attack:               # атака
        cool_down_count = 7
        if steps_attack != 3:
            y_attack = y - 3
            x_attack = x + facing * int(winx*0.00390625)
            steps_attack += 1
        else:
            steps_attack = -3
            in_attack = False
    elif C_press_Count != 0:    # для куллдауна атаки
        if cool_down_count > 0:
            cool_down_count -= 1

    if enemy_cool_down_count > 0:
        enemy_cool_down_count -= 1


    for enemy in enemies:
        enemy.move() # занес внутрь чтобы не делать несколько раз цикл
        if b_k((x, y, radius), (enemy.x, enemy.y, enemy.radius)) and enemy_cool_down_count == 0: # отнимаем жизнь у игрока при соприкосновении с врагом
            if enemy == enemies[0]:
                hp -= 2
            else:
                hp -= 1
            enemy_cool_down_count = 10
        if in_attack:       # отнимаем жизнь у врагов при атаке игрока
            if b_k((x_attack, y_attack, int(winy*0.021166666)), (enemy.x, enemy.y, enemy.radius)):
                enemy.hp -= 2
                if enemy.hp <= 0:
                    if enemy == enemies[0]:
                        win = True
                    enemies.remove(enemy) # враги умирают
    window.fill((0,0,0))
    if in_attack:
        pygame.draw.circle(window, (128, 128, 0), (x_attack, y_attack), int(winy*0.021166666))
    pygame.draw.circle(window, (0,150,90), (x, y), radius)
    for enemy in enemies:
        pygame.draw.circle(window, (255,80,80),(enemy.x, enemy.y), enemy.radius) #тут враги
        pygame.draw.line(window, (0,128,0), (enemy.x - 10, enemy.y - enemy.radius - winx*0.004), (enemy.x + 10 - int(20 * ((enemy.max_hp - enemy.hp) / enemy.max_hp)), enemy.y - enemy.radius - winx*0.004), 2)
        # поднял полоски над врагами, переписал на enemy, так понятней, теперь полоски уменьшаются при уменьшении hp врага
    if hp != 0: # иначе из-за округления рисует немного при 0
        pygame.draw.rect(window, (255,20,20), (int(winx*0.02), int(winy*0.024), hp*18, int(winy*0.02)))  #ПОЛОСКА ХП ИГРОКА
    for elem in platforms:
        pygame.draw.line(window, (0,128,0), (elem[0],elem[1]), (elem[2],elem[1]))
    pygame.display.update()



pygame.quit()
sys.exit()
