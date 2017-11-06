"""Authors: (c)copyright: """
"""Earl Martin Momongan & Peter Vu"""
"""email: techwiz@csu.fullerton.edu"""
"""email: eclipseraid@csu.fullerton.edu"""

"""This is the main script of the program. When called with
the images and sounds folders using python, it will run the
game Starfighter. Starfighter is a space shooter inspired
game, requiring the player to survive waves of enemies with
increasing difficulty until the boss arrives in which the 
player must defeat to win the game."""

import pygame
import random
import os
import sys

# Global Variables
WIDTH = 700   # Width of screen
HEIGHT = 900  # Height of screen
FPS = 60      # Game fps
PSPEED = 5    # Player speed
POWERUP_TIME = 5000

# Define colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initializes pygame and creates game window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT+3))
pygame.display.set_caption("STARFIGHTER")
clock = pygame.time.Clock()

# Set up assets folder
gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder, "images")
sndFolder = os.path.join(gameFolder, "sounds")

# Initializing font
fontName = pygame.font.match_font('arial')

# Text Draw
def draw_text(surf, text, fontSize, x, y):
    font = pygame.font.Font(fontName, fontSize)
    textSurf = font.render(text, True, WHITE)
    textRect = textSurf.get_rect()
    textRect.midtop = (x, y)
    surf.blit(textSurf, textRect)

# Creates new enemy
def new_mob(sprite,spriteGroup):
    m = sprite()
    allSprites.add(m)
    spriteGroup.add(m)
    
# Shield bar
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outlineRect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fillRect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fillRect)
    pygame.draw.rect(surf, WHITE, outlineRect, 2)

# Player lives
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        imgRect = img.get_rect()
        imgRect.x = x + 30 * i
        imgRect.y = y
        surf.blit(img, imgRect)
        
# Player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerImg        
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.75 / 2)
        self.rect.centerx = (WIDTH/2)
        self.rect.bottom = HEIGHT - 100
        self.speedx = 0
        self.speedy = 0
        self.shootDelay = 250
        self.lastShot = pygame.time.get_ticks()
        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hideTimer = pygame.time.get_ticks()
        self.power = 1
        self.powertime = pygame.time.get_ticks()
        
    def update(self):
        # powerup timeout
        if self.power >= 2 and pygame.time.get_ticks() - self.powertime > POWERUP_TIME:
            self.power = 1
            self.powertime = pygame.time.get_ticks()
            
        if self.hidden and pygame.time.get_ticks() - self.hideTimer > 2000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 100
            
        self.speedx = 0
        self.speedy = 0
        key = pygame.key.get_pressed()
        
        # Player controls/Movement
        if key[pygame.K_a]:
            self.speedx = -PSPEED
        if key[pygame.K_d]:
            self.speedx = PSPEED
        if key[pygame.K_w] and self.rect.top < HEIGHT+50:
            self.speedy = -PSPEED
        if key[pygame.K_s] and self.rect.top < HEIGHT+50:
            self.speedy = PSPEED
        if key[pygame.K_SPACE] and self.rect.top < HEIGHT + 50:
            self.shoot()           
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        # Player boundaries
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT and self.hidden != True:
            self.rect.bottom = HEIGHT
        if self.rect.top < HEIGHT - 350:
            self.rect.top = HEIGHT - 350
    
    def powerup(self):
        self.power += 1
        self.powertime = pygame.time.get_ticks()
        
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.lastShot > self.shootDelay:
            self.lastShot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top, blueBulletImg)
                allSprites.add(bullet)
                bullets.add(bullet)
                laser1.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left+2, self.rect.top+6, blueBulletImg)
                bullet2 = Bullet(self.rect.right-2, self.rect.top+6, blueBulletImg)
                allSprites.add(bullet1)
                allSprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                laser1.play()
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left+2, self.rect.top+6, blueBulletImg)
                bullet2 = Bullet(self.rect.right-2, self.rect.top+6, blueBulletImg)
                bullet3 = Bullet(self.rect.centerx, self.rect.top, blueBulletImg)
                bullet1.speedx = -3
                bullet2.speedx = 3
                allSprites.add(bullet1)
                allSprites.add(bullet2)
                allSprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                laser1.play()                
    
    # Temporarily hides player
    def hide(self):
        self.hidden = True
        self.power = 1
        self.hideTimer = pygame.time.get_ticks()
        self.rect.centerx= WIDTH/2
        self.rect.bottom = HEIGHT + 200
            
# Enemy sprites

# Asteroids
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imageOrig = random.choice(meteorImg)
        self.imageOrig.set_colorkey(BLACK)
        self.image = self.imageOrig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.x = random.randrange((WIDTH+50) - (self.rect.width-50))
        self.rect.y = random.randrange(-350,-250)
        self.speedy = random.randrange(3,5)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rotSpeed = random.randrange(-8,8)
        self.lastUpdate = pygame.time.get_ticks() 
        
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.lastUpdate > 50:
            self.lastUpdate = now
            self.rot = (self.rot + self.rotSpeed) % 360
            newImage = pygame.transform.rotate(self.imageOrig, self.rot)
            oldCenter = self.rect.center
            self.image = newImage
            self.rect = self.image.get_rect()
            self.rect.center = oldCenter
            
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -150 or self.rect.right > WIDTH + 150:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,5)
            
            
# Enemy starfighter
class EnemyFighter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(fighterImg)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 /2)
        self.rect.x = random.randrange(100,600)
        self.rect.y = random.randrange(-350,-250)
        self.speedy = random.randrange(3,7)
        self.speedx = random.randrange(-5,5)
        self.dive = random.random()
        self.lowerBound = random.randrange(300,450)
        self.upperBound = random.randrange(150,200)
        self.diveSound = False
        self.lastShot = pygame.time.get_ticks()
        self.shootDelay = random.randrange(500,1500) 
        
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.lastShot > self.shootDelay:
            self.lastShot = now
            self.shootDelay = random.randrange(500,1500)
            bullet = Bullet(self.rect.centerx, self.rect.bottom,redBulletImg)
            bullet.speedy = 6
            bullet.rect.top = self.rect.bottom
            eBullets.add(bullet)
            laser2.play()      
            
    def update(self):
        # Randomizes for dive
        if self.dive > 0.7:
            self.rect.x += 0
            self.rect.y += 15
            if self.diveSound == False:
                flyby.play()
                self.diveSound = True
        
        # Fighter movement
        elif self.dive < 0.7:
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.bottom > self.lowerBound and self.speedy >= 0:
                self.speedy = -self.speedy
                self.speedx = random.randrange(-5, 5)
                self.upperBound = random.randrange(50,200)
            if self.rect.top < self.upperBound and self.speedy <= 0:
                self.speedy = abs(self.speedy)
                self.speedx = random.randrange(-5, 5)
                self.lowerBound = random.randrange(300,450)
            self.shoot()
        
        # Fighter boundaries
        if self.rect.left <= 0:
            self.rect.left == 0
            self.speedx = abs(self.speedx)
        if self.rect.right >= WIDTH:
            self.rect.right == 0
            self.speedx = -self.speedx
        if self.rect.bottom > HEIGHT + 50:
            self.rect.x = random.randrange(100,600)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 7)
            self.speedx = random.randrange(-5, 5)
            self.dive = random.random()
            self.lowerBound = random.randrange(300,450)
            self.upperBound = random.randrange(150,200)


# Enemy Gunship
class Gunship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = gunshipImg
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 /2)
        self.rect.x = random.randrange(50,600)
        self.rect.y = -500
        self.speedy = 2
        self.speedx = 0
        self.lastShot = pygame.time.get_ticks()
        self.emptyClip = pygame.time.get_ticks()
        self.shootDelay = 400
        self.clipSize = 12
        self.clipReload = 3000
        self.health = 5
        
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.lastShot > self.shootDelay and self.rect.bottom > 20 and self.clipSize > 0:
            self.lastShot = now
            bullet1 = Bullet(self.rect.left, self.rect.bottom, greenBulletImg)
            bullet2 = Bullet(self.rect.right, self.rect.bottom, greenBulletImg)
            bullet2.speedy = 6
            bullet1.speedy = 6
            bullet1.rect.top = self.rect.bottom
            bullet2.rect.top = self.rect.bottom
            self.clipSize -= 1
            eBullets.add(bullet1)
            eBullets.add(bullet2)
            laser3.play()
        if self.clipSize == 0:
            self.emptyClip = pygame.time.get_ticks()
            self.clipSize = -1
        if now - self.emptyClip > self.clipReload and self.clipSize == -1:
            self.clipSize = 12
        
    def update(self):
        # Gunship movement
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > 100 and self.speedy == 2:
            self.speedy = 0
            self.speedx = random.choice((-3,3))
        self.shoot()
        
        # Gunship boundaries
        if self.rect.left < 0:
            self.rect.left = 0
            self.speedx = abs(self.speedx)
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speedx = -self.speedx

# Enemy UFO
class UFO(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imageOrig = ufoImg
        self.imageOrig.set_colorkey(BLACK)
        self.image = self.imageOrig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.x = random.randrange(50,600)
        self.rect.y = -300
        self.speedy = 3
        self.rot = 0
        self.rotSpeed = 10
        self.health = 4
        self.shootDelay = 1200
        self.lastUpdate = pygame.time.get_ticks()
        self.lastShot = pygame.time.get_ticks()
        
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.lastUpdate > 50:
            self.lastUpdate = now
            self.rot = (self.rot + self.rotSpeed) % 360
            newImage = pygame.transform.rotate(self.imageOrig, self.rot)
            oldCenter = self.rect.center
            self.image = newImage
            self.rect = self.image.get_rect()
            self.rect.center = oldCenter
    
    def gun(self, x, y):
        bullet = Bullet(self.rect.centerx, self.rect.centerx, greenBulletImg)
        bullet.speedx = x
        bullet.speedy = y
        bullet.rect.top = self.rect.bottom
        allSprites.add(bullet)
        eBullets.add(bullet)
        
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.lastShot > self.shootDelay and self.rect.bottom > 20:
            self.lastShot = now
            self.gun(0, 2)
            self.gun(-2, 2)
            self.gun(2, 2)
            self.gun(-1, 2)
            self.gun(1, 2)
            laser3.play()            
            
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        if self.rect.top > 300 and self.speedy >= 0:
            self.speedy = -2
        if self.rect.bottom < 200 and self.speedy <= 0:
            self.speedy = 2
        self.shoot()
        

# Enemy Boss
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imageOrig = bossImg
        self.imageOrig.set_colorkey(RED)
        self.image = self.imageOrig
        self.rect = self.image.get_rect()
        self.dam_image = bossDamagedImg
        self.dam_image.set_colorkey(RED)
        self.radius = int(self.rect.width * 0.55 / 2)
        self.rect.centerx = WIDTH / 2
        self.rect.y = -500
        self.speedy = 2
        self.speedx = 0
        self.health = 400
        self.damaged = False
        self.damTimer = pygame.time.get_ticks()
        self.alarm = 1
        
        # Side guns
        self.sideGun_lastShot = pygame.time.get_ticks()
        self.sideGun_empty = pygame.time.get_ticks()
        self.sideGun_shootDelay = 100
        self.sideGun_clipSize = 30
        self.sideGun_reload = 3000
        
        # Torpedoes
        self.torpedo_lastShot = pygame.time.get_ticks()
        self.torpedo_empty = pygame.time.get_ticks()
        self.torpedo_shootDelay = 4000
        
        # AA guns
        self.aaGun_lastShot = pygame.time.get_ticks()
        self.aaGun_empty = pygame.time.get_ticks()
        self.aaGun_shootDelay = 600
        self.aaGun_reload = random.randrange(1500,2500)
        self.aaGun_clipSize = 3
        
        # Rotary gun
        self.rotary_lastShot = pygame.time.get_ticks()
        self.rotary_empty = pygame.time.get_ticks()
        self.rotary_shootDelay = 450
        self.rotary_clipSize = 20
        self.rotary_reload = 3000
        self.x = 0
        self.y = 5
        self.gun = 1
        
    # Side Guns 
    def SideGuns(self, x):
        ray = Bullet(x, self.rect.bottom, sideBulletImg)
        ray.speedy = 10
        ray.rotSpeed = 0
        ray.rect.top = self.rect.bottom-60
        eBullets.add(ray)
    
    # Torpedoes
    def Torpedoes(self, x, y, b):
        torpedo = Bullet(b, self.rect.bottom, blueBulletOrigImg)
        torpedo.speedx = x
        torpedo.speedy = y        
        torpedo.rotSpeed = 4
        torpedo.rect.top = self.rect.bottom-200
        eBullets.add(torpedo)
        
    # AA guns
    def AAGuns(self, x, y):
        aaGun = Bullet(x, self.rect.bottom, aaBulletImg)
        aaGun.speedy = 5
        aaGun.rotSpeed = 0
        aaGun.rect.top = y
        eBullets.add(aaGun)
    
    # Rotary gun
    def RotaryGun(self, x, y, b):
        rotary = Bullet(b, self.rect.bottom, redBulletImg)
        rotary.speedx = x
        rotary.speedy = y
        rotary.rect.top = self.rect.top+150
        eBullets.add(rotary)        

    def shoot(self):
        now = pygame.time.get_ticks()
        
        # Side guns
        if now - self.sideGun_lastShot > self.sideGun_shootDelay and self.sideGun_clipSize > 0:
            self.sideGun_lastShot = now
            self.SideGuns(self.rect.left + 60)
            self.SideGuns(self.rect.right - 60)
            self.sideGun_clipSize -= 1
        if self.sideGun_clipSize == 0:
            self.sideGun_empty = pygame.time.get_ticks()
            self.sideGun_clipSize = -1
        if now - self.sideGun_empty > self.sideGun_reload and self.sideGun_clipSize == -1:
            self.sideGun_clipSize = 40
        
        # Phases
        if self.health <= 350 and self.alarm == 1:
            alarm.play()
            self.alarm = 2   
        if self.health <= 250 and self.alarm == 2:
            alarm.play()
            self.alarm = 3
        if self.health <= 150 and self.alarm == 3:
            alarm.play()
            self.alarm = 4
        if self.health <= 50 and self.alarm == 4:
            alarm.play()
            self.alarm = 5
        
        # Torpedoes
        if now - self.torpedo_lastShot > self.torpedo_shootDelay and self.health < 350:
            self.torpedo_lastShot = now
            self.Torpedoes(0, 3, self.rect.centerx)
            self.Torpedoes(-1, 3, self.rect.centerx-25)
            self.Torpedoes(1, 3, self.rect.centerx+25)
            self.Torpedoes(2, 2.8, self.rect.centerx+50)
            self.Torpedoes(-2, 2.8, self.rect.centerx-50)
            
        # AA guns
        if now - self.aaGun_lastShot > self.aaGun_shootDelay and self.aaGun_clipSize > 0:
            self.aaGun_lastShot = now
            self.aaGun_clipSize -= 1
            self.AAGuns(self.rect.centerx-95, self.rect.bottom-50)
            self.AAGuns(self.rect.centerx-130, self.rect.bottom-100)
            self.AAGuns(self.rect.centerx+95, self.rect.bottom-50)
            self.AAGuns(self.rect.centerx+130, self.rect.bottom-100)
            laser3.play()
        if self.aaGun_clipSize == 0:
            self.aaGun_empty = pygame.time.get_ticks()
            self.aaGun_clipSize = -1
        if now - self.aaGun_empty > self.aaGun_reload and self.aaGun_clipSize == -1:
            self.aaGun_clipSize = 3
            self.aaGun_reload = random.randrange(1500,2500)
         
        # Rotary Gun
        if now - self.rotary_lastShot > self.rotary_shootDelay and self.rotary_clipSize > 0 and self.health < 250:
            self.rotary_lastShot = now
            self.rotary_clipSize -= 1
            if self.y == 5 and self.x == 0 and self.gun == 1:
                self.RotaryGun(self.x, self.y, self.rect.centerx+10)
                self.RotaryGun(self.x, self.y, self.rect.centerx-10)
                self.y = 4
                self.x = 1
                self.gun = 2
            elif self.y == 4 and self.gun == 2:
                self.RotaryGun(self.x, self.y, self.rect.centerx+10)
                self.RotaryGun(self.x, self.y, self.rect.centerx-10)
                self.y = 3
                self.x = 2
                self.gun = 3
            elif self.y == 3 and self.gun == 3:
                self.RotaryGun(self.x, self.y, self.rect.centerx+10)
                self.RotaryGun(self.x, self.y, self.rect.centerx-10)
                self.y = 4
                self.x = 1
                self.gun = 4
            elif self.y == 4 and self.gun == 4:
                self.RotaryGun(self.x, self.y, self.rect.centerx+10)
                self.RotaryGun(self.x, self.y, self.rect.centerx-10)
                self.y = 5
                self.x = 0
                self.gun = 5
            elif self.y == 5 and self.gun == 5:
                self.RotaryGun(self.x, self.y, self.rect.centerx+10)
                self.RotaryGun(self.x, self.y, self.rect.centerx-10)
                self.y = 4
                self.x = -1
                self.gun = 6
            elif self.y == 4 and self.gun == 6:
                self.RotaryGun(self.x, self.y, self.rect.centerx+10)
                self.RotaryGun(self.x, self.y, self.rect.centerx-10)
                self.y = 3
                self.x = -2
                self.gun = 7
            elif self.y == 3 and self.gun == 7:
                self.RotaryGun(self.x, self.y, self.rect.centerx+10)
                self.RotaryGun(self.x, self.y, self.rect.centerx-10)
                self.y = 4
                self.x = -1
                self.gun = 8
            elif self.y == 4 and self.gun == 8:
                self.RotaryGun(self.x, self.y, self.rect.centerx+10)
                self.RotaryGun(self.x, self.y, self.rect.centerx-10)
                self.y = 5
                self.x = 0
                self.gun = 1
            laser2.play()
        if self.rotary_clipSize == 0:
            self.rotary_empty = pygame.time.get_ticks()
            self.rotary_clipSize = -1
        if now - self.rotary_empty> self.rotary_reload and self.rotary_clipSize == -1:
            self.rotary_clipSize = 20
        
    def update(self):
        # Damage animation
        if self.damaged == True:
            self.damaged = False
            self.damTimer = pygame.time.get_ticks()
            self.image = self.dam_image
        if self.damaged == False and pygame.time.get_ticks() - self.damTimer > 50:
            self.image = self.imageOrig
            
        # Boss movement
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > 25 and self.speedy == 2:
            self.speedy = 0
            self.speedx = random.choice((-1,1))
        
        # Shoot if entered stage
        if self.speedy == 0:
            self.shoot()
        
        # Boss boundaries
        if self.rect.left < 0:
            self.rect.left = 0
            self.speedx = abs(self.speedx)
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speedx = -self.speedx
        
        
# Bullets
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.imageOrig = img
        self.imageOrig.set_colorkey(BLACK)
        self.image = self.imageOrig.copy()
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 0.0
        self.speedy = -10.0
        self.radius = 10
        self.rot = 0
        self.rotSpeed = -20
        self.lastUpdate = pygame.time.get_ticks()   
        
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.lastUpdate > 50:
            self.lastUpdate = now
            self.rot = (self.rot + self.rotSpeed) % 360
            newImage = pygame.transform.rotate(self.imageOrig, self.rot)
            oldCenter = self.rect.center
            self.image = newImage
            self.rect = self.image.get_rect()
            self.rect.center = oldCenter      
            
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        
        # Deletes bullet if it leaves screen
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > HEIGHT:
            self.kill()
        if self.rect.right < 0:
            self.kill()
        if self.rect.left > WIDTH:
            self.kill()

            
# Power Ups            
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield", "gun"])
        self.image = powerUpImg[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3
        
    def update(self):
        self.rect.y += self.speedy
        
        # Deletes power up if it leaves screen
        if self.rect.top > HEIGHT:
            self.kill()
                       
            
# Explosions
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosionAnim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.lastUpdate = pygame.time.get_ticks()
        self.frameRate = 75       
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.lastUpdate > self.frameRate:
            self.lastUpdate = now
            self.frame += 1
            if self.frame == len(explosionAnim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosionAnim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
        

# Plays Game Over Screen
def show_gameover_screen():
    pygame.mixer.music.stop()
    screen.blit(background, (0,0))
    draw_text(screen, "STARFIGHTER", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "WASD keys to move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press the ESC key to begin...", 18, WIDTH /2 , HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False
        

# Load all graphics
background = pygame.image.load(os.path.join(imgFolder, "back.png")).convert()
background = pygame.transform.scale(background, (WIDTH,HEIGHT+5))
playerImg = pygame.image.load(os.path.join(imgFolder, "playerShip2_green.png")).convert()
playerImg = pygame.transform.scale(playerImg, (56, 37))
playerMiniImg = pygame.transform.scale(playerImg, (28, 19))
playerMiniImg.set_colorkey(BLACK)
blueBulletOrigImg = pygame.image.load(os.path.join(imgFolder, "laserBlue08.png")).convert()
blueBulletImg = pygame.transform.scale(blueBulletOrigImg, (20,20))
greenBulletImg = pygame.image.load(os.path.join(imgFolder, "laserGreen14.png")).convert()
greenBulletImg = pygame.transform.scale(greenBulletImg, (20,20))
redBulletImg = pygame.image.load(os.path.join(imgFolder, "laserRed08.png")).convert()
redBulletImg = pygame.transform.scale(redBulletImg, (20,20))
sideBulletImg = pygame.image.load(os.path.join(imgFolder, "laserGreen10.png")).convert()
aaBulletImg = pygame.image.load(os.path.join(imgFolder, "laserRed16.png")).convert()
ufoImg = pygame.image.load(os.path.join(imgFolder, "ufoRed.png")).convert()
ufoImg = pygame.transform.scale(ufoImg, (110,110))
gunshipImg = pygame.image.load(os.path.join(imgFolder, "enemyRed4.png")).convert()
gunshipImg = pygame.transform.scale(gunshipImg, (103,105))
bossImg = pygame.image.load(os.path.join(imgFolder, "boss.png")).convert()
bossImg = pygame.transform.scale(bossImg, (524, 408))
bossDamagedImg = pygame.image.load(os.path.join(imgFolder, "boss_damaged.png")).convert()
bossDamagedImg = pygame.transform.scale(bossDamagedImg, (524, 408))

fighterImg = []
fighterList = ["enemyBlack1.png", "enemyBlack2.png", "enemyBlack3.png"]
for img in fighterList:
    f = pygame.image.load(os.path.join(imgFolder, img)).convert()
    f = pygame.transform.scale(f, (56,37))
    fighterImg.append(f) 
    
meteorImg = []
meteorList = ["meteorBrown_big1.png", "meteorBrown_big2.png", "meteorBrown_big3.png", "meteorBrown_big4.png",
              "meteorBrown_med1.png", "meteorBrown_med2.png", "meteorBrown_small1.png",
              "meteorBrown_small2.png", "meteorBrown_tiny1.png", "meteorBrown_tiny2.png"]
for img in meteorList:
    meteorImg.append(pygame.image.load(os.path.join(imgFolder, img)).convert())
    
explosionAnim = {}
explosionAnim["lg"] = []
explosionAnim["sm"] = []
explosionAnim["nuke"] = []
for i in range(9):
    filename = "regularExplosion0{}.png".format(i)
    img = pygame.image.load(os.path.join(imgFolder, filename)).convert()
    img.set_colorkey(BLACK)
    imgLg = pygame.transform.scale(img, (75,75))
    explosionAnim["lg"].append(imgLg)
    imgSm = pygame.transform.scale(img, (32,32))
    explosionAnim["sm"].append(imgSm)
    filename = "sonicExplosion0{}.png".format(i)
    img = pygame.image.load(os.path.join(imgFolder, filename)).convert()
    img.set_colorkey(BLACK)
    explosionAnim["nuke"].append(img)

powerUpImg = {}
powerUpImg["shield"] = pygame.image.load(os.path.join(imgFolder, "shield_gold.png")).convert()
powerUpImg["gun"] = pygame.image.load(os.path.join(imgFolder, "bolt_gold.png")).convert()
    
# Load all sounds
laser1 = pygame.mixer.Sound(os.path.join(sndFolder, "Laser_Shoot.wav"))
laser1.set_volume(0.2)
laser2 = pygame.mixer.Sound(os.path.join(sndFolder, "Enemy_Shoot.wav"))
laser2.set_volume(0.2)
laser3 = pygame.mixer.Sound(os.path.join(sndFolder, "Gunship_Shoot.wav"))
laser3.set_volume(0.2)
dam = pygame.mixer.Sound(os.path.join(sndFolder, "Hit.wav"))
dam.set_volume(0.6)
boom = pygame.mixer.Sound(os.path.join(sndFolder, "rumble1.ogg"))
boom.set_volume(0.6)
laserPower = pygame.mixer.Sound(os.path.join(sndFolder, "laser_power.wav"))
laserPower.set_volume(0.6)
shieldPower = pygame.mixer.Sound(os.path.join(sndFolder, "shield_power.wav"))
shieldPower.set_volume(0.6)
explosionSnds = []
expList = ["Explosion1.wav", "Explosion2.wav", "Explosion3.wav"]
flyby = pygame.mixer.Sound(os.path.join(sndFolder, "flyby.wav"))
flyby.set_volume(0.4)
alarm = pygame.mixer.Sound(os.path.join(sndFolder, "RedAlert.wav"))
for snd in expList:
    container = pygame.mixer.Sound(os.path.join(sndFolder, snd))
    container.set_volume(0.4)
    explosionSnds.append(container)


# Game Loop
running = True    
game_over = True

while running:
    if game_over:
        show_gameover_screen()
        boss_killed = False

        # Initialize all sprite groups
        player = Player()
        mobs = pygame.sprite.Group()
        fighter = pygame.sprite.Group()
        gunship = pygame.sprite.Group()
        ufo = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        eBullets = pygame.sprite.Group()
        powerUps = pygame.sprite.Group()
        boss = pygame.sprite.Group()
        allSprites = pygame.sprite.Group()
        allSprites.add(player)
        
        # Initialize User Events
        game_start = pygame.USEREVENT + 0
        meteor_wave = pygame.USEREVENT + 1
        fighter_wave = pygame.USEREVENT + 2
        new_music = pygame.USEREVENT + 3
        ufo_wave = pygame.USEREVENT + 4
        gunship_wave = pygame.USEREVENT + 5
        alert = pygame.USEREVENT + 6
        boss_wave = pygame.USEREVENT + 7
        
        pygame.time.set_timer(game_start, 1)
        pygame.time.set_timer(meteor_wave, 4000)
        pygame.time.set_timer(fighter_wave, 22000)
        pygame.time.set_timer(new_music, 44500)
        pygame.time.set_timer(ufo_wave, 46000)
        pygame.time.set_timer(gunship_wave, 85000)
        pygame.time.set_timer(alert, 145000)
        pygame.time.set_timer(boss_wave, 151000)

        score = 0
        x = 0
        x1 = 0
        y = 0
        y1 = -HEIGHT
        support = False
        game_over = False

    clock.tick(FPS)    
    
    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and boss_killed == True:
            if event.key == pygame.K_ESCAPE:
                game_over = True           
        if event.type == game_start:
            pygame.mixer.music.load(os.path.join(sndFolder, "Battle.ogg"))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            pygame.time.set_timer(game_start, 0)
        if event.type == meteor_wave:
            for i in range(15):
                new_mob(Asteroid,mobs)
            pygame.time.set_timer(meteor_wave, 0)
        if event.type == fighter_wave:
            if support == False:
                for i in range(3):
                    new_mob(EnemyFighter,fighter)
                pygame.time.set_timer(fighter_wave, 2000)
            if support == True and len(fighter) < 3:
                for i in range(2):
                    new_mob(EnemyFighter,fighter)
                pygame.time.set_timer(fighter_wave, 5000)
        if event.type == new_music:
            pygame.mixer.music.load(os.path.join(sndFolder, "Battle dirty.ogg"))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            pygame.time.set_timer(new_music, 0)
        if event.type == ufo_wave:
            if len(ufo) < 2:
                new_mob(UFO, ufo)
            pygame.time.set_timer(ufo_wave, 6500)
            pygame.time.set_timer(fighter_wave, 3000)
        if event.type == gunship_wave: 
            if len(gunship) == 0:
                new_mob(Gunship,gunship)
            pygame.time.set_timer(fighter_wave, 4000)
            pygame.time.set_timer(ufo_wave, 4000)
            pygame.time.set_timer(gunship_wave, 8000)
        if event.type == alert:
            pygame.mixer.music.stop()
            pygame.time.set_timer(fighter_wave, 15000)
            pygame.time.set_timer(ufo_wave, 0)
            pygame.time.set_timer(gunship_wave, 0)
            pygame.time.set_timer(alert, 0)
            for enemy in fighter:
                expl = Explosion(enemy.rect.center, 'lg')
                allSprites.add(expl)
                enemy.kill()
            for enemy in gunship:
                expl = Explosion(enemy.rect.center, 'lg')
                allSprites.add(expl)
                enemy.kill()
            for enemy in ufo:
                expl = Explosion(enemy.rect.center, 'lg')
                allSprites.add(expl)
                enemy.kill()
            boom.play()
            alarm.play()
        if event.type == boss_wave:
            support = True
            pygame.time.set_timer(ufo_wave, 0)
            pygame.time.set_timer(gunship_wave, 0)
            pygame.mixer.music.load(os.path.join(sndFolder, "CPU_Showdown.mp3"))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            new_mob(Boss, boss)
            pygame.time.set_timer(boss_wave, 0)

    # Update
    allSprites.update()
    eBullets.update()

    # Check for bullet collisions
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        random.choice(explosionSnds).play()
        if hit.radius < 15 and hit.radius:
            score += 75
        elif hit.radius > 15 and hit.radius < 30:
            score += 50
        elif hit.radius > 30:
            score += 25
        expl = Explosion(hit.rect.center, 'lg')
        allSprites.add(expl)
        if random.random() > 0.90:
            pow = PowerUp(hit.rect.center)
            allSprites.add(pow)
            powerUps.add(pow)         
        new_mob(Asteroid,mobs)

    hits = pygame.sprite.groupcollide(fighter, bullets, True, True)
    for hit in hits:
        random.choice(explosionSnds).play()
        score += 150
        expl = Explosion(hit.rect.center, 'lg')
        allSprites.add(expl)

    hits = pygame.sprite.groupcollide(gunship, bullets, False, True)
    for hit in hits:
        dam.play()
        expl = Explosion(hit.rect.center, 'sm')
        allSprites.add(expl)
        hit.health -= 1
        if hit.health == 0:
            hit.kill()
            boom.play()
            score += 300
            expl = Explosion(hit.rect.center, 'lg')
            allSprites.add(expl)
    
    hits = pygame.sprite.groupcollide(ufo, bullets, False, True, pygame.sprite.collide_circle)
    for hit in hits:
        dam.play()
        hit.health -= 1
        expl = Explosion(hit.rect.center, 'sm')
        allSprites.add(expl)
        if hit.health == 0:
            hit.kill()
            boom.play()
            score += 250
            expl = Explosion(hit.rect.center, 'lg')
            allSprites.add(expl)
    
    hits = pygame.sprite.groupcollide(boss, bullets, False, True, pygame.sprite.collide_circle)
    for hit in hits:
        dam.play()
        score += 125
        expl = Explosion(hit.rect.center, 'lg')
        allSprites.add(expl)
        hit.health -= 1
        hit.damaged = True
        if hit.health == 0:
            pygame.time.set_timer(fighter_wave, 0)
            for enemy in fighter:
                expl = Explosion(enemy.rect.center, 'lg')
                allSprites.add(expl)
                enemy.kill()
            for bul in eBullets:
                expl = Explosion(bul.rect.center, 'lg')
                allSprites.add(expl)
                bul.kill()
            for meteor in mobs:
                expl = Explosion(bul.rect.center, 'lg')
                allSprites.add(expl)
                meteor.kill()
            hit.kill()
            boom.play()
            score += 5000
            expl = Explosion(hit.rect.center, 'nuke')
            allSprites.add(expl)
            boss_killed = True
            pygame.mixer.music.load(os.path.join(sndFolder, "victory.mp3"))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)

    # Check for collisions
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= (hit.radius * 2) * 1.25
        random.choice(explosionSnds).play()
        expl = Explosion(hit.rect.center, 'lg')
        allSprites.add(expl)
        new_mob(Asteroid,mobs)
        if player.shield <= 0:
            boom.play()
            deathExpl = Explosion(player.rect.center, 'nuke')
            allSprites.add(deathExpl)
            player.hide()
            player.lives -= 1
            player.shield = 100    

    hits = pygame.sprite.spritecollide(player, fighter, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 100
        random.choice(explosionSnds).play()
        expl = Explosion(hit.rect.center, 'lg')
        allSprites.add(expl)
        new_mob(EnemyFighter,fighter)
        if player.shield <= 0:
            boom.play()
            deathExpl = Explosion(player.rect.center, 'nuke')
            allSprites.add(deathExpl)
            player.hide()
            player.lives -= 1
            player.shield = 100    

    hits = pygame.sprite.spritecollide(player, eBullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 15
        dam.play()
        expl = Explosion(hit.rect.center, 'sm')
        allSprites.add(expl)
        if player.shield <= 0:
            boom.play()
            deathExpl = Explosion(player.rect.center, 'nuke')
            allSprites.add(deathExpl)
            player.hide()
            player.lives -= 1
            player.shield = 100                

    hits = pygame.sprite.spritecollide(player, powerUps, True)
    for hit in hits:
        if hit.type == "shield":
            shieldPower.play()
            player.shield += 20
            score += 500
            if player.shield >= 100:
                player.shield = 100
        if hit.type == "gun":
            laserPower.play()
            score += 500
            player.powerup()              

    # Waits for death animation to finish
    if player.lives == 0 and not deathExpl.alive():
        pygame.mixer.music.stop()
        game_over = True

    # Draw / render
    y1 += 1
    y += 1

    screen.fill(BLACK)
    screen.blit(background, (x,y))
    screen.blit(background, (x1,y1))
    if y > HEIGHT:
        y = -HEIGHT
    if y1 > HEIGHT:
        y1 = -HEIGHT
    allSprites.draw(screen)
    eBullets.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, playerMiniImg)

    # Display images
    if boss_killed == True:
        draw_text(screen, "YOU WON!!!", 64, WIDTH / 2, HEIGHT / 4)
        draw_text(screen, "Final Score: " + str(score), 22, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, "Press ESC to quit...", 22, WIDTH / 2, HEIGHT * 0.75)
    pygame.display.flip()

pygame.quit()
