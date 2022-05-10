import pygame
import random
from all_needed_things import Enemy, Boss, Heal_pack, balls_collide as b_k


pygame.init()
MAX_FRAME_ITERATION = 2000

class PlatformerForAi:
    def __init__(self):
        # self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # - для полноэкранного
        # self.window = pygame.display.set_mode((1280, 720), display=1)  # - для второго монитора
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        displ = pygame.display.Info()
        self.winx, self.winy = displ.current_w, displ.current_h
        pygame.display.set_caption('PlatformeR')
        self.frame_delay = 0  # регулирует скорость игры 15 для адекватной скорости
        self.score = 0
        # for music
        self.music_volume = 0.2  # 0.2 is default
        self.file = 'Resources/OST.mp3'
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load(self.file)
        pygame.mixer.music.play(loops = -1)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.event.wait()
        # описание параметров игрока
        self.x, self.y, self.radius, self.speed, self.jump_step, self.in_jump, self.in_fall, self.facing, self.hp, self.max_hp, self.in_attack, self.radius_attack, self.steps_attack, self.fallspeed = int(
            self.winx * 0.08), int(self.winy * 0.99) - int(self.winy * 0.02), int(self.winy * 0.02), int(
            self.winx * 0.00875), 5, False, True, 1, 25, 25, False, int(self.winy * 0.03), -3, self.winy * 0.016666667
        self.jump_speed = [0, int(self.winy * 0.001666667), int(self.winy * 0.006666667), int(self.winy * 0.015),
                           int(self.winy * 0.026666666),
                           int(self.winy * 0.041666666)]
        self.y_attack = self.y - int(self.radius * 0.4)
        self.x_attack = self.x + self.facing * int(self.radius * 1.2)
        self.frame_iteration = 0
        self.player_picture_number = 1
        self.attack_x_scale = int(4.45 * self.radius)
        self.attack_y_scale = int(3.51 * self.radius)
        # ДЛЯ СПРАЙТОВ
        self.player_in_attack1 = pygame.image.load('Resources/PLAYER_IN_ATTACK1.png')
        self.player_in_attack1 = pygame.transform.scale(self.player_in_attack1, (self.attack_x_scale, self.attack_y_scale))
        self.player_in_attack2 = pygame.image.load('Resources/PLAYER_IN_ATTACK2.png')
        self.player_in_attack2 = pygame.transform.scale(self.player_in_attack2, (self.attack_x_scale, self.attack_y_scale))
        self.player_in_attack3 = pygame.image.load('Resources/PLAYER_IN_ATTACK3.png')
        self.player_in_attack3 = pygame.transform.scale(self.player_in_attack3, (self.attack_x_scale, self.attack_y_scale))
        self.player_in_attack4 = pygame.image.load('Resources/PLAYER_IN_ATTACK4.png')
        self.player_in_attack4 = pygame.transform.scale(self.player_in_attack4, (self.attack_x_scale, self.attack_y_scale))
        self.player_in_attack5 = pygame.image.load('Resources/PLAYER_IN_ATTACK5.png')
        self.player_in_attack5 = pygame.transform.scale(self.player_in_attack5, (self.attack_x_scale, self.attack_y_scale))
        self.player_in_attack6 = pygame.image.load('Resources/PLAYER_IN_ATTACK6.png')
        self.player_in_attack6 = pygame.transform.scale(self.player_in_attack6, (self.attack_x_scale, self.attack_y_scale))
        self.player_in_attack_1 = pygame.image.load('Resources/PLAYER_IN_ATTACK-1.png')
        self.player_in_attack_1 = pygame.transform.scale(self.player_in_attack_1, (self.attack_x_scale, self.attack_y_scale))
        self.player_in_attack_2 = pygame.image.load('Resources/PLAYER_IN_ATTACK-2.png')
        self.player_in_attack_2 = pygame.transform.scale(self.player_in_attack_2, (self.attack_x_scale, self.attack_y_scale))
        self.player_in_attack_3 = pygame.image.load('Resources/PLAYER_IN_ATTACK-3.png')
        self.player_in_attack_3 = pygame.transform.scale(self.player_in_attack_3, (self.attack_x_scale, self.attack_y_scale))
        self.player_in_attack_4 = pygame.image.load('Resources/PLAYER_IN_ATTACK-4.png')
        self.player_in_attack_4 = pygame.transform.scale(self.player_in_attack_4, (self.attack_x_scale, self.attack_y_scale))
        self.player_in_attack_5 = pygame.image.load('Resources/PLAYER_IN_ATTACK-5.png')
        self.player_in_attack_5 = pygame.transform.scale(self.player_in_attack_5, (self.attack_x_scale, self.attack_y_scale))
        self.player_in_attack_6 = pygame.image.load('Resources/PLAYER_IN_ATTACK-6.png')
        self.player_in_attack_6 = pygame.transform.scale(self.player_in_attack_6, (self.attack_x_scale, self.attack_y_scale))
        self.player_in_attack_list = [self.player_in_attack1, self.player_in_attack2, self.player_in_attack3, self.player_in_attack4,
                                 self.player_in_attack5,
                                 self.player_in_attack6, self.player_in_attack_1, self.player_in_attack_2, self.player_in_attack_3,
                                 self.player_in_attack_4, self.player_in_attack_5, self.player_in_attack_6]
        self.background_count = 1
        self.background_sprite1 = pygame.image.load('Resources/BACKGROUND1.png')
        self.background_sprite1 = pygame.transform.scale(self.background_sprite1, (self.winx, self.winy))
        self.background_sprite2 = pygame.image.load('Resources/BACKGROUND2.png')
        self.background_sprite2 = pygame.transform.scale(self.background_sprite2, (self.winx, self.winy))
        self.background_sprite3 = pygame.image.load('Resources/BACKGROUND3.png')
        self.background_sprite3 = pygame.transform.scale(self.background_sprite3, (self.winx, self.winy))
        self.background_sprite4 = pygame.image.load('Resources/BACKGROUND4.png')
        self.background_sprite4 = pygame.transform.scale(self.background_sprite4, (self.winx, self.winy))
        self.background_sprite5 = pygame.image.load('Resources/BACKGROUND5.png')
        self.background_sprite5 = pygame.transform.scale(self.background_sprite5, (self.winx, self.winy))
        self.background_sprite6 = pygame.image.load('Resources/BACKGROUND6.png')
        self.background_sprite6 = pygame.transform.scale(self.background_sprite6, (self.winx, self.winy))
        self.background_sprite7 = pygame.image.load('Resources/BACKGROUND7.png')
        self.background_sprite7 = pygame.transform.scale(self.background_sprite7, (self.winx, self.winy))
        self.background_sprite8 = pygame.image.load('Resources/BACKGROUND8.png')
        self.background_sprite8 = pygame.transform.scale(self.background_sprite8, (self.winx, self.winy))
        self.background_sprite_list = [self.background_sprite1, self.background_sprite2, self.background_sprite3, self.background_sprite4,
                                  self.background_sprite5, self.background_sprite6, self.background_sprite7, self.background_sprite8]
        self.platform_sprite = pygame.image.load('Resources/PLATFORM_SPRITE.png')

        self.walk_skale = int(self.radius * 3.5)
        self.walk_x_shift = self.radius * 1.82  # сдвиг спрайта над хитбоксом, используется при отрисовке
        self.walk_y_shift = self.radius * 2.1

        self.attack_right_x_shift = self.radius * 1.801  # больше - левее
        self.attack_right_y_shift = self.radius * 2.09
        self.attack_left_x_shift = self.radius * 2.6579
        self.attack_left_y_shift = self.radius * 2.09

        self.PLAYER1 = pygame.image.load('Resources/PLAYER1.png')
        self.PLAYER1 = pygame.transform.scale(self.PLAYER1, (self.walk_skale, self.walk_skale))
        self.PLAYER2 = pygame.image.load('Resources/PLAYER2.png')
        self.PLAYER2 = pygame.transform.scale(self.PLAYER2, (self.walk_skale, self.walk_skale))
        self.PLAYER3 = pygame.image.load('Resources/PLAYER3.png')
        self.PLAYER3 = pygame.transform.scale(self.PLAYER3, (self.walk_skale, self.walk_skale))
        self.PLAYER4 = pygame.image.load('Resources/PLAYER4.png')
        self.PLAYER4 = pygame.transform.scale(self.PLAYER4, (self.walk_skale, self.walk_skale))
        self.PLAYER5 = pygame.image.load('Resources/PLAYER5.png')
        self.PLAYER5 = pygame.transform.scale(self.PLAYER5, (self.walk_skale, self.walk_skale))
        self.PLAYER6 = pygame.image.load('Resources/PLAYER6.png')
        self.PLAYER6 = pygame.transform.scale(self.PLAYER6, (self.walk_skale, self.walk_skale))
        self.PLAYER7 = pygame.image.load('Resources/PLAYER7.png')
        self.PLAYER7 = pygame.transform.scale(self.PLAYER7, (self.walk_skale, self.walk_skale))
        self.PLAYER8 = pygame.image.load('Resources/PLAYER8.png')
        self.PLAYER8 = pygame.transform.scale(self.PLAYER8, (self.walk_skale, self.walk_skale))
        self.PLAYER9 = pygame.image.load('Resources/PLAYER9.png')
        self.PLAYER9 = pygame.transform.scale(self.PLAYER9, (self.walk_skale, self.walk_skale))
        self.PLAYER10 = pygame.image.load('Resources/PLAYER10.png')
        self.PLAYER10 = pygame.transform.scale(self.PLAYER10, (self.walk_skale, self.walk_skale))
        self.PLAYER11 = pygame.image.load('Resources/PLAYER11.png')
        self.PLAYER11 = pygame.transform.scale(self.PLAYER11, (self.walk_skale, self.walk_skale))
        self.PLAYER12 = pygame.image.load('Resources/PLAYER12.png')
        self.PLAYER12 = pygame.transform.scale(self.PLAYER12, (self.walk_skale, self.walk_skale))
        self.PLAYER_1 = pygame.image.load('Resources/PLAYER-1.png')
        self.PLAYER_1 = pygame.transform.scale(self.PLAYER_1, (self.walk_skale, self.walk_skale))
        self.PLAYER_2 = pygame.image.load('Resources/PLAYER-2.png')
        self.PLAYER_2 = pygame.transform.scale(self.PLAYER_2, (self.walk_skale, self.walk_skale))
        self.PLAYER_3 = pygame.image.load('Resources/PLAYER-3.png')
        self.PLAYER_3 = pygame.transform.scale(self.PLAYER_3, (self.walk_skale, self.walk_skale))
        self.PLAYER_4 = pygame.image.load('Resources/PLAYER-4.png')
        self.PLAYER_4 = pygame.transform.scale(self.PLAYER_4, (self.walk_skale, self.walk_skale))
        self.PLAYER_5 = pygame.image.load('Resources/PLAYER-5.png')
        self.PLAYER_5 = pygame.transform.scale(self.PLAYER_5, (self.walk_skale, self.walk_skale))
        self.PLAYER_6 = pygame.image.load('Resources/PLAYER-6.png')
        self.PLAYER_6 = pygame.transform.scale(self.PLAYER_6, (self.walk_skale, self.walk_skale))
        self.PLAYER_7 = pygame.image.load('Resources/PLAYER-7.png')
        self.PLAYER_7 = pygame.transform.scale(self.PLAYER_7, (self.walk_skale, self.walk_skale))
        self.PLAYER_8 = pygame.image.load('Resources/PLAYER-8.png')
        self.PLAYER_8 = pygame.transform.scale(self.PLAYER_8, (self.walk_skale, self.walk_skale))
        self.PLAYER_9 = pygame.image.load('Resources/PLAYER-9.png')
        self.PLAYER_9 = pygame.transform.scale(self.PLAYER_9, (self.walk_skale, self.walk_skale))
        self.PLAYER_10 = pygame.image.load('Resources/PLAYER-10.png')
        self.PLAYER_10 = pygame.transform.scale(self.PLAYER_10, (self.walk_skale, self.walk_skale))
        self.PLAYER_11 = pygame.image.load('Resources/PLAYER-11.png')
        self.PLAYER_11 = pygame.transform.scale(self.PLAYER_11, (self.walk_skale, self.walk_skale))
        self.PLAYER_12 = pygame.image.load('Resources/PLAYER-12.png')
        self.PLAYER_12 = pygame.transform.scale(self.PLAYER_12, (self.walk_skale, self.walk_skale))
        self.player_sprite_list = [self.PLAYER1, self.PLAYER2, self.PLAYER3, self.PLAYER4, self.PLAYER5, self.PLAYER6, self.PLAYER7, self.PLAYER8, self.PLAYER9, self.PLAYER10,
                              self.PLAYER11, self.PLAYER12, self.PLAYER_1, self.PLAYER_2, self.PLAYER_3, self.PLAYER_4, self.PLAYER_5, self.PLAYER_6, self.PLAYER_7,
                              self.PLAYER_8, self.PLAYER_9, self.PLAYER_10, self.PLAYER_11, self.PLAYER_12]
        self.death_sprite = pygame.image.load('Resources/DEATH.png')
        self.death_sprite = pygame.transform.scale(self.death_sprite, (self.winx, self.winy))
        self.time_is_up_sprite = pygame.image.load('Resources/TIME_IS_UP.png')
        self.time_is_up_sprite = pygame.transform.scale(self.time_is_up_sprite, (self.winx, self.winy))
        self.win_sprite = pygame.image.load('Resources/WIN.png')
        self.win_sprite = pygame.transform.scale(self.win_sprite, (self.winx, self.winy))

        self.enemies = []
        self.heal_packs = []
        self.increase, self.decrease = False, False  # для пульсации лечилок

        self.cool_down_count, self.D_press_Count, self.enemy_cool_down_count = 0, 0, 0  # для куллдауна атаки
        self.D_not_pressed_timer = 100  # чтобы спрыг вниз нормально работал
        self.win = False  # флаг убийства босса
        self.jump_cool_down = 0
        self.platforms = [(0, int(self.winy * 0.99), self.winx), (0, int(self.winy * 0.95), self.winx),
                     (0, int(self.winy * 0.90), self.winx),
                     (0, int(self.winy * 0.85), self.winx),
                     (0, int(self.winy * 0.80), self.winx),
                     (0, int(self.winy * 0.75), self.winx),
                     (0, int(self.winy * 0.70), self.winx),
                     (0, int(self.winy * 0.65), self.winx),
                     (0, int(self.winy * 0.60), self.winx),
                     (0, int(self.winy * 0.55), self.winx),
                     (0, int(self.winy * 0.50), self.winx),
                     (0, int(self.winy * 0.45), self.winx),
                     (0, int(self.winy * 0.28), self.winx),
                     (0, int(self.winy * 0.39), self.winx),
                     (0, int(self.winy * 0.33), self.winx),
                     (0, int(self.winy * 0.28), self.winx)]
        self.platform_visited_flag_list = [False] * len(self.platforms)
        self.run = True

        self.radiuse = int(self.winy * 0.08)  # описание БОССа
        self.enemies.append(Boss(int(self.winx * 0.2) + self.radiuse / 2, int(self.winy * 0.39) - self.radiuse, int(self.winx * 0.8) - self.radiuse / 2,
                            int((int(self.winx * 0.2) + int(self.winx * 0.8)) / 2), int(self.winy * 0.28) - self.radiuse, self.radiuse,
                            int(self.winx * 0.008), 90))

        for elem in random.sample(self.platforms, 12):  # генератор ВРАГОВ
            if elem != (0, int(self.winy * 0.99), self.winx) and elem != (int(self.winx * 0.2), int(self.winy * 0.28), int(self.winx * 0.8)):
                self.radiuse = random.randint(int(self.winy * 0.03), int(self.winy * 0.05))
                self.enemies.append(
                    Enemy(elem[0] + self.radiuse / 2, elem[1] - self.radiuse, elem[2] - self.radiuse / 2, int((elem[0] + elem[2]) / 2),
                          elem[1] - self.radiuse, self.radiuse, random.randint(int(self.winx * 0.003), int(self.winx * 0.005)),
                          random.randint(10, 20)))
            else:
                continue

        for elem in random.sample(self.platforms, 10):  # генератор ХИЛОК
            self.radiuse = random.randint(int(self.winy * 0.01), int(self.winy * 0.012))
            self.heal_packs.append(
                Heal_pack(random.randint(elem[0], elem[2]), elem[1] - self.radiuse, self.radiuse, self.radiuse * 1.4,
                          random.randint(2, 10),
                          random.randint(10, 20)))

        pygame.display.update()
        pygame.event.pump()
        self.keys = pygame.key.get_pressed()
        #self.reset_game()


    def reset_game(self):
        self.frame_iteration = 0
        self.score = 0
        window = pygame.display.Info()
        self.winx, self.winy = window.current_w, window.current_h
        self.x, self.y, self.in_jump, self.in_fall, self.facing, self.hp, self.in_attack, self.steps_attack = int(self.winx * 0.08), int(self.winy * 0.99) - int(
            self.winy * 0.02), False, True, 1, 25, False, -3
        self.player_picture_number, self.background_count = 1, 1
        self.enemies, self.heal_packs = [], []
        self.increase, self.decrease = False, False  # для пульсации лечилок
        self.cool_down_count, self.D_press_Count, self.enemy_cool_down_count = 0, 0, 0  # для куллдауна атаки
        self.D_not_pressed_timer = 100  # чтобы спрыг вниз нормально работал
        self.win = False  # флаг убийства босса
        self.jump_cool_down = 0
        self.run = True
        self.radiuse = int(self.winy * 0.08)
        self.enemies.append(
            Boss(int(self.winx * 0.2) + self.radiuse / 2, int(self.winy * 0.39) - self.radiuse, int(self.winx * 0.8) - self.radiuse / 2,
                 int((int(self.winx * 0.2) + int(self.winx * 0.8)) / 2), int(self.winy * 0.28) - self.radiuse, self.radiuse,
                 int(self.winx * 0.008), 90))
        for elem in random.sample(self.platforms, 12):  # генератор ВРАГОВ
            if elem != (0, int(self.winy * 0.99), self.winx) and elem != (int(self.winx * 0.2), int(self.winy * 0.28), int(self.winx * 0.8)):
                self.radiuse = random.randint(int(self.winy * 0.03), int(self.winy * 0.05))
                self.enemies.append(
                    Enemy(elem[0] + self.radiuse / 2, elem[1] - self.radiuse, elem[2] - self.radiuse / 2,
                          int((elem[0] + elem[2]) / 2),
                          elem[1] - self.radiuse, self.radiuse, random.randint(int(self.winx * 0.003), int(self.winx * 0.005)),
                          random.randint(10, 20)))
            else:
                continue
        self.platform_visited_flag_list = [False] * len(self.platforms)

        for elem in random.sample(self.platforms, 10):  # генератор ХИЛОК
            self.radiuse = random.randint(int(self.winy * 0.01), int(self.winy * 0.012))
            self.heal_packs.append(Heal_pack(random.randint(elem[0], elem[2]), elem[1] - self.radiuse, self.radiuse, self.radiuse * 1.4,
                                        random.randint(2, 10), random.randint(10, 20)))
        pygame.display.update()
        pygame.event.pump()


    def frame_step(self, action):
        self.frame_iteration += 1
        reward = 0
        game_over = False
        pygame.time.delay(self.frame_delay)  # задержка между кадрами

        if (0 > self.x) or (self.x > self.winx) or (0 > self.y) or (self.y > self.winy): # если упал за карту
            self.x, self.y =  (self.winx * 0.08), int(self.winy * 0.99) - int(self.winy * 0.02)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            raise SystemExit

        if self.background_count < 8:
            self.background_count += 1
        else:
            self.background_count = 1

        if self.hp <= 0:  # текст смерти, если хп = 0
            self.window.blit(self.death_sprite, (0, 0))  # рисуем текст смерти
            pygame.display.update()
            pygame.time.delay(1000)
            reward -= 50 # за смерть
            game_over = True
            return reward, game_over, self.score
        if self.frame_iteration > MAX_FRAME_ITERATION: # текст о проигрыше, время вышло
            self.window.blit(self.time_is_up_sprite, (0, 0))  # рисуем текст смерти
            pygame.display.update()
            pygame.time.delay(1000)
            reward -= 50  # за смерть
            game_over = True
            return reward, game_over, self.score
        if len(self.enemies) == 0 or self.win:  # текст победы
            self.window.blit(self.win_sprite, (0, 0))  # рисуем текст победы
            pygame.display.update()
            pygame.time.delay(2000)
            return reward, game_over, self.score


        for i in range(len(self.platforms)):
            elem = self.platforms[i]
            if abs(self.y + self.radius - elem[1]) < int(self.fallspeed + self.winy * 0.001666667) and self.y + self.radius - elem[1] <= 0 and elem[
                0] <= self.x <= elem[2] and self.D_not_pressed_timer > 0:
                if not self.in_jump:
                    self.y -= self.y + self.radius - elem[1]
                self.in_fall = False
                if not self.platform_visited_flag_list[i]:
                    reward += 0 # за то что побывал на новой платформе
                    self.platform_visited_flag_list[i] = True
                self.fallspeed = self.winy * 0.0166666667


        self.move_player(action)
        #if (not bool(action[0])) and (not bool(action[1])):  # and (not bool(action[2])) and (not bool(action[3])):
        #    reward -= 1 # за бездействие на месте


        if self.D_not_pressed_timer <= 5:
            self.D_not_pressed_timer += 1

        if self.in_jump:
            if self.jump_step >= -5:
                if self.jump_step >= 0:
                    self.y -= self.jump_speed[self.jump_step]
                elif self.in_fall:
                    self.y += self.jump_speed[-self.jump_step]
                    if self.jump_step != -5:
                        for elem in self.platforms:
                            if abs(self.y + self.radius - elem[1]) < self.jump_speed[-self.jump_step + 1] and (elem[0] <= self.x <= elem[2]):
                                self.y -= self.y + self.radius - elem[1]
                                self.in_fall = False
                else:
                    self.in_jump = False
                    self.jump_step = 6
                    self.jump_cool_down = 2
                self.jump_step -= 1
            else:
                self.in_jump = False
                self.jump_step = 5
                self.jump_cool_down = 2
        elif self.jump_cool_down > 0:
            self.jump_cool_down -= 1
        if self.in_fall and not self.in_jump:
            self.y += int(self.fallspeed)
            if self.fallspeed < self.winy * 0.025:
                self.fallspeed += self.winy * 0.00166666667
        self.in_fall = True
        if self.in_attack:  # атака
            self.cool_down_count = 7
            if self.steps_attack != 3:
                self.y_attack = self.y - int(self.radius * 0.4)
                self.x_attack = self.x + self.facing * int(self.radius * 1.2)
                self.steps_attack += 1
            else:
                self.steps_attack = -3
                self.in_attack = False
        elif self.D_press_Count != 0:  # для куллдауна атаки
            if self.cool_down_count > 0:
                self.cool_down_count -= 1

        if self.enemy_cool_down_count > 0:
            self.enemy_cool_down_count -= 1

        for heal_pack in self.heal_packs:  # пульсация бонусов
            if heal_pack.radius <= heal_pack.radius_increased / 1.4:
                self.increase = True
                self.decrease = False
                break
            if heal_pack.radius >= heal_pack.radius_increased:
                self.decrease = True
                self.increase = False
                break

        if self.increase is True:
            for heal_pack in self.heal_packs:
                heal_pack.radius += int(self.winy * 0.0017)
                heal_pack.y -= int(self.winy * 0.0017)
        if self.decrease is True:
            for heal_pack in self.heal_packs:
                heal_pack.radius -= int(self.winy * 0.0017)
                heal_pack.y += int(self.winy * 0.0017)

        for enemy in self.enemies:
            enemy.move()
            if (b_k((self.x, self.y, self.radius), (enemy.x, enemy.y + int(enemy.radius * 0.1), int(enemy.radius * 0.95))) or (
                    b_k((self.x, self.y - self.radius, self.radius), (enemy.x, enemy.y,
                                                  int(enemy.radius * 0.9))))) and self.enemy_cool_down_count == 0:  # отнимаем хп у игрока
                reward -= 1 # за получение урона
                if enemy == self.enemies[0]:
                    self.hp -= 2
                else:
                    self.hp -= 1
                self.enemy_cool_down_count = 14
            if self.in_attack:  # отнимаем жизнь у врагов при атаке игрока
                if b_k((self.x_attack, self.y_attack, self.radius_attack), (enemy.x, enemy.y, int(enemy.radius * 0.95))):
                    enemy.hp -= 2
                    if enemy == self.enemies[0]:
                        reward += 30  # за то, что бьет босса
                        self.score += 2
                    else:
                        reward += 15  # за то, что бьет врага
                        self.score += 1
                    if enemy.hp <= 0:
                        self.enemies.remove(enemy)  # враги умирают
                        if enemy == self.enemies[0]:
                            reward += 400  # за победу над боссом
                            self.score += 300
                        else:
                            reward += 50  # за победу над врагом
                            self.score += 50
                        if enemy == self.enemies[0]:
                            self.win = True

        for heal_pack in self.heal_packs:  # прибавляем жизнь игроку при соприкосновении с лечилкой
            if b_k((self.x, self.y, self.radius), (heal_pack.x, heal_pack.y, heal_pack.radius)):
                if self.hp < self.max_hp:
                    self.hp = self.max_hp
                elif self.hp == self.max_hp:
                    continue
                self.heal_packs.remove(heal_pack)
                reward += 50  # за использование лечилки для восстановления здоровья

        self.window.blit(self.background_sprite_list[self.background_count - 1], (0, 0))  # рисуем фон

        for elem in self.platforms:  # рисуем платформы
            self.window.blit(pygame.transform.scale(self.platform_sprite, (elem[2] - elem[0], int(self.winy * 0.01))),
                        (elem[0], elem[1]))
        for heal_pack in self.heal_packs:  # рисуем хилки
            pygame.draw.circle(self.window, (0, random.randint(200, 255), 80), (heal_pack.x, heal_pack.y), heal_pack.radius)
        for enemy in self.enemies:  # рисуем врагов и их жизни int(winx*0.012)
            self.window.blit(enemy.get_pic(), (enemy.x - enemy.radius, enemy.y - int(enemy.radius * 0.948)))
            pygame.draw.line(self.window, (0, 128, 0),
                             (enemy.x - int(self.winx * 0.00625), enemy.y - enemy.radius - int(self.winx * 0.004)), (
                                 enemy.x + int(self.winx * 0.00625) - (
                                     int(20 * ((enemy.max_hp - enemy.hp) / enemy.max_hp))) / 1600 * self.winx,
                                 enemy.y - enemy.radius - int(self.winx * 0.004)), 2)
        if self.hp != 0:  # рисуем полоску жизни игрока
            pygame.draw.rect(self.window, (90, 15, 15),
                             (int(self.winx * 0.02), int(self.winy * 0.024),
                              int(0.35 * self.winx), int(self.winy * 0.02)))
            pygame.draw.rect(self.window, (255, 20, 20),
                             (int(self.winx * 0.02), int(self.winy * 0.024),
                              int((self.hp / self.max_hp * 0.35) * self.winx), int(self.winy * 0.02)))

        if self.facing == 1 and self.player_picture_number == 0 and self.steps_attack == -3:  # рисуем спрайт игрока
            self.window.blit(self.PLAYER1, (self.x - 1.85 * self.radius, self.y - 2.1 * self.radius))
        if self.facing == -1 and self.player_picture_number == 0 and self.steps_attack == -3:
            self.window.blit(self.PLAYER_1, (self.x - 1.8 * self.radius, self.y - 2.1 * self.radius))

        if self.player_picture_number != 0 and self.steps_attack == -3:
            if self.facing == 1:
                self.window.blit(self.player_sprite_list[self.player_picture_number - 1], (self.x - self.walk_x_shift, self.y - self.walk_y_shift))
            else:
                self.window.blit(self.player_sprite_list[self.player_picture_number + 11], (self.x - self.walk_x_shift, self.y - self.walk_y_shift))
        if self.steps_attack != -3:
            if self.facing == 1:
                self.window.blit(self.player_in_attack_list[self.steps_attack + 2],
                            (self.x - self.attack_right_x_shift, self.y - self.attack_right_y_shift))
            else:
                self.window.blit(self.player_in_attack_list[self.steps_attack + 8], (self.x - self.attack_left_x_shift, self.y - self.attack_left_y_shift))
        pygame.display.update()
        pygame.event.pump()
        return reward, game_over, self.score

    def move_player(self, action):
        if bool(action[1]) and self.x - self.radius > int(self.winx * 0.00390625):
            self.x -= self.speed
            if not self.in_attack:
                self.facing = -1
            if self.player_picture_number < 12:
                self.player_picture_number += 1
            else:
                self.player_picture_number = 1
        elif not bool(action[0]):
            self.player_picture_number = 0
        if bool(action[0]) and self.x < int(self.winx * 0.99609375) - self.radius:
            self.x += self.speed
            if not self.in_attack:
                self.facing = 1
            if self.player_picture_number < 12:
                self.player_picture_number += 1
            else:
                self.player_picture_number = 1
        elif bool(action[0]):
            self.player_picture_number = 0

        if bool(action[4]) and self.cool_down_count == 0:
            self.D_press_Count += 1  # счетчик нажатий клавиши D, для куллдауна
            self.in_attack = True
        if bool(action[3]) and self.y != int(self.winy * 0.99) - self.radius and self.D_not_pressed_timer > 5 and not self.in_jump: #action == Action.go_down and self.y != int(self.winy * 0.99) - self.radius and self.D_not_pressed_timer > 5 and not self.in_jump:
            self.D_not_pressed_timer = 0
            self.in_fall = True
        if not self.in_jump and not self.in_fall:
            if bool(action[2]) and self.jump_cool_down == 0:
                self.in_jump = True
                self.in_fall = True

        pygame.event.pump()
