import random, pygame



class Enemy:
    def __init__(self, x0, y0, xk, x, y, radius, speed, hp):
        self.x0 = x0
        self.y0 = y0
        self.xk = xk
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.hp = hp
        self.max_hp = hp
        self.max_n = 8
        self.picture_number = 1
        PIGEON1 = pygame.image.load('PIGEON1.png')
        PIGEON1 = pygame.transform.smoothscale(PIGEON1, (2*radius, 2*radius))
        PIGEON2 = pygame.image.load('PIGEON2.png')
        PIGEON2 = pygame.transform.smoothscale(PIGEON2, (2*radius, 2*radius))
        PIGEON3 = pygame.image.load('PIGEON3.png')
        PIGEON3 = pygame.transform.smoothscale(PIGEON3, (2*radius, 2*radius))
        PIGEON4 = pygame.image.load('PIGEON4.png')
        PIGEON4 = pygame.transform.smoothscale(PIGEON4, (2*radius, 2*radius))
        PIGEON5 = pygame.image.load('PIGEON5.png')
        PIGEON5 = pygame.transform.smoothscale(PIGEON5, (2*radius, 2*radius))
        PIGEON6 = pygame.image.load('PIGEON6.png')
        PIGEON6 = pygame.transform.smoothscale(PIGEON6, (2*radius, 2*radius))
        PIGEON7 = pygame.image.load('PIGEON7.png')
        PIGEON7 = pygame.transform.smoothscale(PIGEON7, (2*radius, 2*radius))
        PIGEON8 = pygame.image.load('PIGEON8.png')
        PIGEON8 = pygame.transform.smoothscale(PIGEON8, (2*radius, 2*radius))
        PIGEON_1 = pygame.image.load('PIGEON-1.png')
        PIGEON_1 = pygame.transform.smoothscale(PIGEON_1, (2*radius, 2*radius))
        PIGEON_2 = pygame.image.load('PIGEON-2.png')
        PIGEON_2 = pygame.transform.smoothscale(PIGEON_2, (2*radius, 2*radius))
        PIGEON_3 = pygame.image.load('PIGEON-3.png')
        PIGEON_3 = pygame.transform.smoothscale(PIGEON_3, (2*radius, 2*radius))
        PIGEON_4 = pygame.image.load('PIGEON-4.png')
        PIGEON_4 = pygame.transform.smoothscale(PIGEON_4, (2*radius, 2*radius))
        PIGEON_5 = pygame.image.load('PIGEON-5.png')
        PIGEON_5 = pygame.transform.smoothscale(PIGEON_5, (2*radius, 2*radius))
        PIGEON_6 = pygame.image.load('PIGEON-6.png')
        PIGEON_6 = pygame.transform.smoothscale(PIGEON_6, (2*radius, 2*radius))
        PIGEON_7 = pygame.image.load('PIGEON-7.png')
        PIGEON_7 = pygame.transform.smoothscale(PIGEON_7, (2*radius, 2*radius))
        PIGEON_8 = pygame.image.load('PIGEON-8.png')
        PIGEON_8 = pygame.transform.smoothscale(PIGEON_8, (2*radius, 2*radius))
        self.picture = [PIGEON1,PIGEON2,PIGEON3,PIGEON4,PIGEON5,PIGEON6,PIGEON7,PIGEON8,PIGEON_1,PIGEON_2,PIGEON_3,PIGEON_4,PIGEON_5,PIGEON_6,PIGEON_7,PIGEON_8]
        
    def move(self): #эт чтобы они бродили по платформе
        if self.x + self.speed >= self.xk or self.x0 >= self.x + self.speed:
            self.speed = -self.speed
            self.max_n *= -1
            self.picture_number *= -1
        self.x += self.speed
        self.picture_number = self.picture_number % self.max_n + int(self.max_n / 8)
    def get_pic(self):
        if self.picture_number < 0:
            return self.picture[-self.picture_number + 7]
        else:
            return self.picture[self.picture_number - 1]
        
class Boss(Enemy):
    def __init__(self, x0, y0, xk, x, y, radius, speed, hp):
        Enemy.__init__(self, x0, y0, xk, x, y, radius, speed, hp)
        BOSS1 = pygame.image.load('BOSS1.png')
        BOSS1 = pygame.transform.smoothscale(BOSS1, (2*radius, 2*radius))
        BOSS2 = pygame.image.load('BOSS2.png')
        BOSS2 = pygame.transform.smoothscale(BOSS2, (2*radius, 2*radius))
        BOSS3 = pygame.image.load('BOSS3.png')
        BOSS3 = pygame.transform.smoothscale(BOSS3, (2*radius, 2*radius))
        BOSS4 = pygame.image.load('BOSS4.png')
        BOSS4 = pygame.transform.smoothscale(BOSS4, (2*radius, 2*radius))
        BOSS5 = pygame.image.load('BOSS5.png')
        BOSS5 = pygame.transform.smoothscale(BOSS5, (2*radius, 2*radius))
        BOSS6 = pygame.image.load('BOSS6.png')
        BOSS6 = pygame.transform.smoothscale(BOSS6, (2*radius, 2*radius))
        BOSS7 = pygame.image.load('BOSS7.png')
        BOSS7 = pygame.transform.smoothscale(BOSS7, (2*radius, 2*radius))
        BOSS8 = pygame.image.load('BOSS8.png')
        BOSS8 = pygame.transform.smoothscale(BOSS8, (2*radius, 2*radius))
        BOSS_1 = pygame.image.load('BOSS-1.png')
        BOSS_1 = pygame.transform.smoothscale(BOSS_1, (2*radius, 2*radius))
        BOSS_2 = pygame.image.load('BOSS-2.png')
        BOSS_2 = pygame.transform.smoothscale(BOSS_2, (2*radius, 2*radius))
        BOSS_3 = pygame.image.load('BOSS-3.png')
        BOSS_3 = pygame.transform.smoothscale(BOSS_3, (2*radius, 2*radius))
        BOSS_4 = pygame.image.load('BOSS-4.png')
        BOSS_4 = pygame.transform.smoothscale(BOSS_4, (2*radius, 2*radius))
        BOSS_5 = pygame.image.load('BOSS-5.png')
        BOSS_5 = pygame.transform.smoothscale(BOSS_5, (2*radius, 2*radius))
        BOSS_6 = pygame.image.load('BOSS-6.png')
        BOSS_6 = pygame.transform.smoothscale(BOSS_6, (2*radius, 2*radius))
        BOSS_7 = pygame.image.load('BOSS-7.png')
        BOSS_7 = pygame.transform.smoothscale(BOSS_7, (2*radius, 2*radius))
        BOSS_8 = pygame.image.load('BOSS-8.png')
        BOSS_8 = pygame.transform.smoothscale(BOSS_8, (2*radius, 2*radius))
        self.picture = [BOSS1,BOSS2,BOSS3,BOSS4,BOSS5,BOSS6,BOSS7,BOSS8,BOSS_1,BOSS_2,BOSS_3,BOSS_4,BOSS_5,BOSS_6,BOSS_7,BOSS_8]

        


class Heal_pack:
    def __init__(self, x, y, radius, radius_increased, speed, hp):
        self.x = x
        self.y = y
        self.radius = radius
        self.radius_increased = radius_increased
        self.speed = speed
        self.hp = hp
        self.picture = 'name.png'


def balls_collide(ball1, ball2):
    if ((ball1[0]-ball2[0])**2 + (ball1[1]-ball2[1])**2)**0.5 <= ball1[2]+ball2[2]:
        return True
    else:
        return False
