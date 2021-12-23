import pygame, sys
from all_needed_things import Enemy, Boss, Heal_pack, balls_collide as b_k
import random

pygame.init()
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

displ = pygame.display.Info()
winx, winy = displ.current_w, displ.current_h
pygame.display.set_caption('my game')
frame_delay = 25  # регулирует скорость игры

# for music
music_volume = 0.0  # 0.2 is default
file = 'Resources/OST.mp3'
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(music_volume)
pygame.event.wait()

# описание параметров игрока
x, y, radius, speed, jump_step, in_jump, in_fall, facing, hp, max_hp, in_attack, radius_attack, steps_attack, fallspeed = int(
    winx * 0.08), int(winy * 0.99) - int(winy * 0.02), int(winy * 0.02), int(
    winx * 0.00875), 5, False, True, 1, 15, 15, False, int(winy * 0.03), -3, winy * 0.016666667
jump_speed = [0, int(winy * 0.001666667), int(winy * 0.006666667), int(winy * 0.015), int(winy * 0.026666666),
              int(winy * 0.041666666)]  # при смене радиуса тут^тож исправить^
y_attack = y - int(radius * 0.4)
x_attack = x + facing * int(radius * 1.2)
frame_iteration = 0

# ДЛЯ СПРАЙТОВ
player_picture_number = 1
attack_x_scale = int(4.45 * radius)
attack_y_scale = int(3.51 * radius)

player_in_attack1 = pygame.image.load('Resources/PLAYER_IN_ATTACK1.png')
player_in_attack1 = pygame.transform.scale(player_in_attack1, (attack_x_scale, attack_y_scale))
player_in_attack2 = pygame.image.load('Resources/PLAYER_IN_ATTACK2.png')
player_in_attack2 = pygame.transform.scale(player_in_attack2, (attack_x_scale, attack_y_scale))
player_in_attack3 = pygame.image.load('Resources/PLAYER_IN_ATTACK3.png')
player_in_attack3 = pygame.transform.scale(player_in_attack3, (attack_x_scale, attack_y_scale))
player_in_attack4 = pygame.image.load('Resources/PLAYER_IN_ATTACK4.png')
player_in_attack4 = pygame.transform.scale(player_in_attack4, (attack_x_scale, attack_y_scale))
player_in_attack5 = pygame.image.load('Resources/PLAYER_IN_ATTACK5.png')
player_in_attack5 = pygame.transform.scale(player_in_attack5, (attack_x_scale, attack_y_scale))
player_in_attack6 = pygame.image.load('Resources/PLAYER_IN_ATTACK6.png')
player_in_attack6 = pygame.transform.scale(player_in_attack6, (attack_x_scale, attack_y_scale))
player_in_attack_1 = pygame.image.load('Resources/PLAYER_IN_ATTACK-1.png')
player_in_attack_1 = pygame.transform.scale(player_in_attack_1, (attack_x_scale, attack_y_scale))
player_in_attack_2 = pygame.image.load('Resources/PLAYER_IN_ATTACK-2.png')
player_in_attack_2 = pygame.transform.scale(player_in_attack_2, (attack_x_scale, attack_y_scale))
player_in_attack_3 = pygame.image.load('Resources/PLAYER_IN_ATTACK-3.png')
player_in_attack_3 = pygame.transform.scale(player_in_attack_3, (attack_x_scale, attack_y_scale))
player_in_attack_4 = pygame.image.load('Resources/PLAYER_IN_ATTACK-4.png')
player_in_attack_4 = pygame.transform.scale(player_in_attack_4, (attack_x_scale, attack_y_scale))
player_in_attack_5 = pygame.image.load('Resources/PLAYER_IN_ATTACK-5.png')
player_in_attack_5 = pygame.transform.scale(player_in_attack_5, (attack_x_scale, attack_y_scale))
player_in_attack_6 = pygame.image.load('Resources/PLAYER_IN_ATTACK-6.png')
player_in_attack_6 = pygame.transform.scale(player_in_attack_6, (attack_x_scale, attack_y_scale))
player_in_attack_list = [player_in_attack1, player_in_attack2, player_in_attack3, player_in_attack4, player_in_attack5,
                         player_in_attack6, player_in_attack_1, player_in_attack_2, player_in_attack_3,
                         player_in_attack_4, player_in_attack_5, player_in_attack_6]

background_count = 1
background_sprite1 = pygame.image.load('Resources/BACKGROUND1.png')
background_sprite1 = pygame.transform.scale(background_sprite1, (winx, winy))
background_sprite2 = pygame.image.load('Resources/BACKGROUND2.png')
background_sprite2 = pygame.transform.scale(background_sprite2, (winx, winy))
background_sprite3 = pygame.image.load('Resources/BACKGROUND3.png')
background_sprite3 = pygame.transform.scale(background_sprite3, (winx, winy))
background_sprite4 = pygame.image.load('Resources/BACKGROUND4.png')
background_sprite4 = pygame.transform.scale(background_sprite4, (winx, winy))
background_sprite5 = pygame.image.load('Resources/BACKGROUND5.png')
background_sprite5 = pygame.transform.scale(background_sprite5, (winx, winy))
background_sprite6 = pygame.image.load('Resources/BACKGROUND6.png')
background_sprite6 = pygame.transform.scale(background_sprite6, (winx, winy))
background_sprite7 = pygame.image.load('Resources/BACKGROUND7.png')
background_sprite7 = pygame.transform.scale(background_sprite7, (winx, winy))
background_sprite8 = pygame.image.load('Resources/BACKGROUND8.png')
background_sprite8 = pygame.transform.scale(background_sprite8, (winx, winy))
background_sprite_list = [background_sprite1, background_sprite2, background_sprite3, background_sprite4,
                          background_sprite5, background_sprite6, background_sprite7, background_sprite8]
platform_sprite = pygame.image.load('Resources/PLATFORM_SPRITE.png')

walk_skale = int(radius * 3.5)
walk_x_shift = radius * 1.82  # сдвиг спрайта над хитбоксом, используется при отрисовке
walk_y_shift = radius * 2.1

attack_right_x_shift = radius * 1.801  # больше - левее
attack_right_y_shift = radius * 2.09
attack_left_x_shift = radius * 2.6579
attack_left_y_shift = radius * 2.09

PLAYER1 = pygame.image.load('Resources/PLAYER1.png')
PLAYER1 = pygame.transform.scale(PLAYER1, (walk_skale, walk_skale))
PLAYER2 = pygame.image.load('Resources/PLAYER2.png')
PLAYER2 = pygame.transform.scale(PLAYER2, (walk_skale, walk_skale))
PLAYER3 = pygame.image.load('Resources/PLAYER3.png')
PLAYER3 = pygame.transform.scale(PLAYER3, (walk_skale, walk_skale))
PLAYER4 = pygame.image.load('Resources/PLAYER4.png')
PLAYER4 = pygame.transform.scale(PLAYER4, (walk_skale, walk_skale))
PLAYER5 = pygame.image.load('Resources/PLAYER5.png')
PLAYER5 = pygame.transform.scale(PLAYER5, (walk_skale, walk_skale))
PLAYER6 = pygame.image.load('Resources/PLAYER6.png')
PLAYER6 = pygame.transform.scale(PLAYER6, (walk_skale, walk_skale))
PLAYER7 = pygame.image.load('Resources/PLAYER7.png')
PLAYER7 = pygame.transform.scale(PLAYER7, (walk_skale, walk_skale))
PLAYER8 = pygame.image.load('Resources/PLAYER8.png')
PLAYER8 = pygame.transform.scale(PLAYER8, (walk_skale, walk_skale))
PLAYER9 = pygame.image.load('Resources/PLAYER9.png')
PLAYER9 = pygame.transform.scale(PLAYER9, (walk_skale, walk_skale))
PLAYER10 = pygame.image.load('Resources/PLAYER10.png')
PLAYER10 = pygame.transform.scale(PLAYER10, (walk_skale, walk_skale))
PLAYER11 = pygame.image.load('Resources/PLAYER11.png')
PLAYER11 = pygame.transform.scale(PLAYER11, (walk_skale, walk_skale))
PLAYER12 = pygame.image.load('Resources/PLAYER12.png')
PLAYER12 = pygame.transform.scale(PLAYER12, (walk_skale, walk_skale))
PLAYER_1 = pygame.image.load('Resources/PLAYER-1.png')
PLAYER_1 = pygame.transform.scale(PLAYER_1, (walk_skale, walk_skale))
PLAYER_2 = pygame.image.load('Resources/PLAYER-2.png')
PLAYER_2 = pygame.transform.scale(PLAYER_2, (walk_skale, walk_skale))
PLAYER_3 = pygame.image.load('Resources/PLAYER-3.png')
PLAYER_3 = pygame.transform.scale(PLAYER_3, (walk_skale, walk_skale))
PLAYER_4 = pygame.image.load('Resources/PLAYER-4.png')
PLAYER_4 = pygame.transform.scale(PLAYER_4, (walk_skale, walk_skale))
PLAYER_5 = pygame.image.load('Resources/PLAYER-5.png')
PLAYER_5 = pygame.transform.scale(PLAYER_5, (walk_skale, walk_skale))
PLAYER_6 = pygame.image.load('Resources/PLAYER-6.png')
PLAYER_6 = pygame.transform.scale(PLAYER_6, (walk_skale, walk_skale))
PLAYER_7 = pygame.image.load('Resources/PLAYER-7.png')
PLAYER_7 = pygame.transform.scale(PLAYER_7, (walk_skale, walk_skale))
PLAYER_8 = pygame.image.load('Resources/PLAYER-8.png')
PLAYER_8 = pygame.transform.scale(PLAYER_8, (walk_skale, walk_skale))
PLAYER_9 = pygame.image.load('Resources/PLAYER-9.png')
PLAYER_9 = pygame.transform.scale(PLAYER_9, (walk_skale, walk_skale))
PLAYER_10 = pygame.image.load('Resources/PLAYER-10.png')
PLAYER_10 = pygame.transform.scale(PLAYER_10, (walk_skale, walk_skale))
PLAYER_11 = pygame.image.load('Resources/PLAYER-11.png')
PLAYER_11 = pygame.transform.scale(PLAYER_11, (walk_skale, walk_skale))
PLAYER_12 = pygame.image.load('Resources/PLAYER-12.png')
PLAYER_12 = pygame.transform.scale(PLAYER_12, (walk_skale, walk_skale))
player_sprite_list = [PLAYER1, PLAYER2, PLAYER3, PLAYER4, PLAYER5, PLAYER6, PLAYER7, PLAYER8, PLAYER9, PLAYER10,
                      PLAYER11, PLAYER12, PLAYER_1, PLAYER_2, PLAYER_3, PLAYER_4, PLAYER_5, PLAYER_6, PLAYER_7,
                      PLAYER_8, PLAYER_9, PLAYER_10, PLAYER_11, PLAYER_12]


def reset_game():
    global x, y, in_jump, in_fall, facing, hp, in_attack, steps_attack
    x, y, in_jump, in_fall, facing, hp, in_attack, steps_attack = int(winx * 0.08), int(winy * 0.99) - int(
        winy * 0.02), False, True, 1, 15, False, -3
    global player_picture_number, background_count
    player_picture_number, background_count = 1, 1
    global enemies, heal_packs
    enemies, heal_packs = [], []
    global increase, decrease
    increase, decrease = False, False  # для пульсации лечилок
    global cool_down_count, D_press_Count, enemy_cool_down_count
    cool_down_count, D_press_Count, enemy_cool_down_count = 0, 0, 0  # для куллдауна атаки
    global D_not_pressed_timer
    D_not_pressed_timer = 100 # чтобы спрыг вниз нормально работал
    global win
    win = False  # флаг убийства босса
    global jump_cool_down
    jump_cool_down = 0
    global run
    run = True
    global radiuse
    radiuse = int(winy * 0.08)
    enemies.append(Boss(int(winx * 0.2) + radiuse / 2, int(winy * 0.39) - radiuse, int(winx * 0.8) - radiuse / 2,
                        int((int(winx * 0.2) + int(winx * 0.8)) / 2), int(winy * 0.28) - radiuse, radiuse,
                        int(winx * 0.008), 90))
    global platforms
    for elem in random.sample(platforms, random.randint(15, 20)):  # генератор ВРАГОВ
        if elem != (0, int(winy * 0.99), winx) and elem != (int(winx * 0.2), int(winy * 0.28), int(winx * 0.8)):
            radiuse = random.randint(int(winy * 0.03), int(winy * 0.05))
            enemies.append(
                Enemy(elem[0] + radiuse / 2, elem[1] - radiuse, elem[2] - radiuse / 2, int((elem[0] + elem[2]) / 2),
                      elem[1] - radiuse, radiuse, random.randint(int(winx * 0.003), int(winx * 0.005)),
                      random.randint(10, 20)))
        else:
            continue

    for elem in random.sample(platforms, random.randint(3, 4)):  # генератор ХИЛОК
        radiuse = random.randint(int(winy * 0.01), int(winy * 0.012))
        heal_packs.append(Heal_pack(random.randint(elem[0], elem[2]), elem[1] - radiuse, radiuse, radiuse * 1.4,
                                    random.randint(2, 10), random.randint(10, 20)))
    pygame.display.update()

death_sprite = pygame.image.load('Resources/DEATH.png')
death_sprite = pygame.transform.scale(death_sprite, (winx, winy))
win_sprite = pygame.image.load('Resources/WIN.png')
win_sprite = pygame.transform.scale(win_sprite, (winx, winy))

enemies = []
heal_packs = []

increase, decrease = False, False  # для пульсации лечилок

cool_down_count, D_press_Count, enemy_cool_down_count = 0, 0, 0  # для куллдауна атаки
D_not_pressed_timer = 100  # чтобы спрыг вниз нормально работал
win = False  # флаг убийства босса
jump_cool_down = 0
platforms = [(0, int(winy * 0.99), winx), (int(winx * 0.18), int(winy * 0.94), int(winx * 0.38)),
             (int(winx * 0.75), int(winy * 0.94), int(winx * 0.88)),
             (int(winx * 0.33), int(winy * 0.89), int(winx * 0.40)),
             (int(winx * 0.68), int(winy * 0.89), int(winx * 0.88)),
             (int(winx * 0.35), int(winy * 0.84), int(winx * 0.6)),
             (int(winx * 0.07), int(winy * 0.84), int(winx * 0.16)),
             (int(winx * 0.65), int(winy * 0.84), int(winx * 0.93)),
             (int(winx * 0.2), int(winy * 0.79), int(winx * 0.7)), (0, int(winy * 0.74), int(winx * 0.2)),
             (int(winx * 0.7), int(winy * 0.74), winx), (int(winx * 0.1), int(winy * 0.69), int(winx * 0.5)),
             (int(winx * 0.5), int(winy * 0.64), int(winx * 0.8)), (0, int(winy * 0.64), int(winx * 0.1)),
             (int(winx * 0.9), int(winy * 0.64), int(winx * 1)), (int(winx * 0.75), int(winy * 0.7), int(winx * 0.95)),
             (int(winx * 0.78), int(winy * 0.59), int(winx * 1)),
             (int(winx * 0.05), int(winy * 0.57), int(winx * 0.55)),
             (int(winx * 0.45), int(winy * 0.5), int(winx * 0.78)),
             (int(winx * 0.2), int(winy * 0.44), int(winx * 0.55)), (0, int(winy * 0.44), int(winx * 0.1)),
             (int(winx * 0.1), int(winy * 0.36), int(winx * 0.2)), (int(winx * 0.1), int(winy * 0.2), int(winx * 0.2)),
             (int(winx * 0.8), int(winy * 0.36), int(winx * 0.9)), (int(winx * 0.8), int(winy * 0.2), int(winx * 0.9)),
             (int(winx * 0.2), int(winy * 0.28), int(winx * 0.8)),
             (int(winx * 0.65), int(winy * 0.45), int(winx * 0.85))]
run = True

radiuse = int(winy * 0.08)  # описание БОССа
enemies.append(Boss(int(winx * 0.2) + radiuse / 2, int(winy * 0.39) - radiuse, int(winx * 0.8) - radiuse / 2,
                    int((int(winx * 0.2) + int(winx * 0.8)) / 2), int(winy * 0.28) - radiuse, radiuse,
                    int(winx * 0.008), 90))

for elem in random.sample(platforms, random.randint(15, 20)):  # генератор ВРАГОВ
    if elem != (0, int(winy * 0.99), winx) and elem != (int(winx * 0.2), int(winy * 0.28), int(winx * 0.8)):
        radiuse = random.randint(int(winy * 0.03), int(winy * 0.05))
        enemies.append(
            Enemy(elem[0] + radiuse / 2, elem[1] - radiuse, elem[2] - radiuse / 2, int((elem[0] + elem[2]) / 2),
                  elem[1] - radiuse, radiuse, random.randint(int(winx * 0.003), int(winx * 0.005)),
                  random.randint(10, 20)))
    else:
        continue

for elem in random.sample(platforms, random.randint(3, 4)):  # генератор ХИЛОК
    radiuse = random.randint(int(winy * 0.01), int(winy * 0.012))
    heal_packs.append(
        Heal_pack(random.randint(elem[0], elem[2]), elem[1] - radiuse, radiuse, radiuse * 1.4, random.randint(2, 10),
                  random.randint(10, 20)))

pygame.display.update()
keys = pygame.key.get_pressed()

while run:  # цикл игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False

    pygame.time.delay(frame_delay)  # задержка между кадрами

    if background_count < 8:
        background_count += 1
    else:
        background_count = 1

    if hp <= 0:  # текст смерти
        window.blit(death_sprite, (0, 0))  # рисуем текст смерти
        pygame.display.update()
        pygame.time.delay(2000)
        break
    if len(enemies) == 0 or win:  # текст победы
        window.blit(win_sprite, (0, 0))  # рисуем текст победы
        pygame.display.update()
        pygame.time.delay(2000)
        break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    if keys[pygame.K_LEFT] and x - radius > int(winx * 0.00390625):
        x -= speed
        if not in_attack:
            facing = -1
        if player_picture_number < 12:
            player_picture_number += 1
        else:
            player_picture_number = 1
    elif keys[pygame.K_RIGHT] is False:
        player_picture_number = 0
    if keys[pygame.K_RIGHT] and x < int(winx * 0.99609375) - radius:
        x += speed
        if not in_attack:
            facing = 1
        if player_picture_number < 12:
            player_picture_number += 1
        else:
            player_picture_number = 1
    elif keys[pygame.K_LEFT] is False:
        player_picture_number = 0

    if keys[pygame.K_d] and cool_down_count == 0:
        D_press_Count += 1  # счетчик нажатий клавиши D, для куллдауна
        in_attack = True
    for elem in platforms:
        if abs(y + radius - elem[1]) < int(fallspeed + winy * 0.001666667) and y + radius - elem[1] <= 0 and elem[
            0] <= x <= elem[2] and D_not_pressed_timer > 0:
            if not in_jump:
                y -= y + radius - elem[1]
            in_fall = False
            fallspeed = winy * 0.0166666667
    if keys[pygame.K_DOWN] and y != int(winy * 0.99) - radius and D_not_pressed_timer > 5 and not in_jump:
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
                        if abs(y + radius - elem[1]) < jump_speed[-jump_step + 1] and (elem[0] <= x <= elem[2]):
                            y -= y + radius - elem[1]
                            in_fall = False
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
        if fallspeed < winy * 0.025:
            fallspeed += winy * 0.00166666667
    in_fall = True
    if in_attack:  # атака
        cool_down_count = 7
        if steps_attack != 3:
            y_attack = y - int(radius * 0.4)
            x_attack = x + facing * int(radius * 1.2)
            steps_attack += 1
        else:
            steps_attack = -3
            in_attack = False
    elif D_press_Count != 0:  # для куллдауна атаки
        if cool_down_count > 0:
            cool_down_count -= 1

    if enemy_cool_down_count > 0:
        enemy_cool_down_count -= 1

    for heal_pack in heal_packs:  # пульсация бонусов
        if heal_pack.radius <= heal_pack.radius_increased / 1.4:
            increase = True
            decrease = False
            break
        if heal_pack.radius >= heal_pack.radius_increased:
            decrease = True
            increase = False
            break

    if increase is True:
        for heal_pack in heal_packs:
            heal_pack.radius += int(winy * 0.0017)
            heal_pack.y -= int(winy * 0.0017)
    if decrease is True:
        for heal_pack in heal_packs:
            heal_pack.radius -= int(winy * 0.0017)
            heal_pack.y += int(winy * 0.0017)

    for enemy in enemies:
        enemy.move()
        if (b_k((x, y, radius), (enemy.x, enemy.y + int(enemy.radius * 0.1), int(enemy.radius * 0.95))) or (
        b_k((x, y - radius, radius), (enemy.x, enemy.y,
                                      int(enemy.radius * 0.9))))) and enemy_cool_down_count == 0:  # отнимаем хп у игрока
            if enemy == enemies[0]:
                hp -= 2
            else:
                hp -= 1
            enemy_cool_down_count = 14
        if in_attack:  # отнимаем жизнь у врагов при атаке игрока
            if b_k((x_attack, y_attack, radius_attack), (enemy.x, enemy.y, int(enemy.radius * 0.95))):
                enemy.hp -= 2
                if enemy.hp <= 0:
                    if enemy == enemies[0]:
                        win = True
                    enemies.remove(enemy)  # враги умирают

    for heal_pack in heal_packs:  # прибавляем жизнь игроку при соприкосновении с лечилкой
        if b_k((x, y, radius), (heal_pack.x, heal_pack.y, heal_pack.radius)):
            if hp <= 0.6 * max_hp:
                hp += 0.4 * max_hp
            elif 0.6 * max_hp < hp < max_hp:
                hp += max_hp - hp

            elif hp == max_hp:
                continue
            heal_packs.remove(heal_pack)

    window.blit(background_sprite_list[background_count - 1], (0, 0))  # рисуем фон

    for elem in platforms:  # рисуем платформы
        window.blit(pygame.transform.scale(platform_sprite, (elem[2] - elem[0], int(winy * 0.01))), (elem[0], elem[1]))
    for heal_pack in heal_packs:  # рисуем хилки
        pygame.draw.circle(window, (0, random.randint(200, 255), 80), (heal_pack.x, heal_pack.y), heal_pack.radius)
    for enemy in enemies:  # рисуем врагов и их жизни int(winx*0.012)
        window.blit(enemy.get_pic(), (enemy.x - enemy.radius, enemy.y - int(enemy.radius * 0.948)))
        pygame.draw.line(window, (0, 128, 0),
                         (enemy.x - int(winx * 0.00625), enemy.y - enemy.radius - int(winx * 0.004)), (
                         enemy.x + int(winx * 0.00625) - (
                             int(20 * ((enemy.max_hp - enemy.hp) / enemy.max_hp))) / 1600 * winx,
                         enemy.y - enemy.radius - int(winx * 0.004)), 2)
    if hp != 0:  # рисуем полоску жизни игрока
        pygame.draw.rect(window, (255, 20, 20),
                         (int(winx * 0.02), int(winy * 0.024), int((hp * 25 / 1080) * winx), int(winy * 0.02)))

    if facing == 1 and player_picture_number == 0 and steps_attack == -3:  # рисуем спрайт игрока
        window.blit(PLAYER1, (x - 1.85 * radius, y - 2.1 * radius))
    if facing == -1 and player_picture_number == 0 and steps_attack == -3:
        window.blit(PLAYER_1, (x - 1.8 * radius, y - 2.1 * radius))

    if player_picture_number != 0 and steps_attack == -3:
        if facing == 1:
            window.blit(player_sprite_list[player_picture_number - 1], (x - walk_x_shift, y - walk_y_shift))
        else:
            window.blit(player_sprite_list[player_picture_number + 11], (x - walk_x_shift, y - walk_y_shift))
    if steps_attack != -3:
        if facing == 1:
            window.blit(player_in_attack_list[steps_attack + 2], (x - attack_right_x_shift, y - attack_right_y_shift))
        else:
            window.blit(player_in_attack_list[steps_attack + 8], (x - attack_left_x_shift, y - attack_left_y_shift))
    pygame.display.update()

pygame.quit()
sys.exit()