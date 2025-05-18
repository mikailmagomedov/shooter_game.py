from pygame import *
from random import randint

bullets = sprite.Group()
lost = 0
lost1 = 0

font.init()
font1 = font.SysFont('Segoe Script', 36)
font2 = font.SysFont('Segoe Script', 36)
font3 = font.SysFont('Segoe Script', 36)
font4 = font.SysFont('Segoe Script', 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (50,50))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
    def move(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_a]:
            self.rect.x -= 2
        if key_pressed[K_d]:
            self.rect.x += 2
    def fire(self):
        global bullets
        if len(bullets) < 10:
            bullet = Bullet('bullet.png', self.rect.x, self.rect.y, 1)
            bullets.add(bullet)

class Monster(GameSprite):
    def update(self):
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(1, 650)
            global lost
            global lost1
            lost = lost + 1
            lost1 = lost1 - 5
        elif self.rect.y <= 500:
            self.rect.y += self.speed

class Bullet(GameSprite):
    def update(self):
        if self.rect.y >= 0:
            self.rect.y -= self.speed
        elif self.rect.y <= 0:
            self.kill()

win = display.set_mode((700,500))
display.set_caption('Тест: Какая ты табуретка? СУПЕР ХАРДКОР МОД')
bg = transform.scale(image.load('galaxy.jpg'), (700,500))
clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
clock.tick(FPS)
monsters = sprite.Group()
fire = mixer.Sound('fire.ogg')

rocket = Player('rocket.png', 300, 430, 1)

for i in range(3):
    monster = Monster('ufo.png', randint(1, 650), 0, 1)
    monsters.add(monster)

game = True
finish = False
while game:
    win.blit(bg,(0,0))
    rocket.move()
    monsters.update()
    monsters.draw(win)
    text_lose = font1.render("Пропущено:"+str(lost), 1, (255, 255, 255))
    text_damage = font2.render("Счёт:"+str(lost1), 1, (255, 255, 255))
    defeat_text = font3.render('Красава, ты проиграл!', 1, (255,0,0))
    win_text = font3.render('Красава, ты победил!', 1, (0,255,0))
    win.blit(text_lose,(10,50))
    win.blit(text_damage,(10,20))
    k = key.get_pressed()
    bullets.update()
    bullets.draw(win)
    if k[K_UP]:
        rocket.fire()

    for e in event.get():
        if e.type == QUIT:
            game = False

    if sprite.groupcollide(bullets, monsters, True, True):
        monster = Monster('ufo.png', randint(1, 650), 0, 1)
        lost1 = lost1 + 1
        monsters.add(monster)
        fire.play()
        
    if sprite.spritecollide(rocket, monsters, False) or lost >= 3:
        win.blit(defeat_text,(100,250))
        finish = True

    if lost1 >= 30:
        win.blit(win_text,(100,250))
        finish = True

    rocket.reset()
    display.update()