import pygame
import constants as c
from bullet import Bullet
from hud import HUD

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super(Ship, self).__init__()
        self.image = pygame.image.load('spaceships\\ships\\brown.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
        self.rect = self.image.get_rect()
        self.rect.x = c.DISPLAY_WIDTH // 2
        self.rect.y = c.DISPLAY_HEIGHT - self.rect.height * 2 - 5
        self.snd_hit = pygame.mixer.Sound('.\\sound_fx\\sounds\\Hit-1.ogg')
        self.bullets = pygame.sprite.Group()
        self.snd_shoot = pygame.mixer.Sound('.\\sound_fx\\sounds\\Fire 1.ogg')
        self.max_hp = 3
        self.hp = self.max_hp
        self.lives = 3
        self.hud = HUD(self.hp, self.lives)
        self.hud_group = pygame.sprite.Group()
        self.hud_group.add(self.hud)
        self.is_invincible = False
        self.max_invincibility_timer = 60
        self.invincibility_timer = 0
        self.is_alive = True

        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.reload = 0
    
    def update(self):
        self.reload += 1
        self.hud_group.update()
        self.bullets.update()
        for bullet in self.bullets:
            if bullet.rect.y <= 0:
                self.bullets.remove(bullet)
        self.rect.x += self.vel_x
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= c.DISPLAY_WIDTH - self.rect.width:
            self.rect.x = c.DISPLAY_WIDTH - self.rect.width
        self.rect.y += self.vel_y

        #check for invincibility
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1
        else:
            self.is_invincible = False

    def shoot(self):
        if self.is_alive:
            if self.reload >= 0:
                self.snd_shoot.play()
                new_bullet = Bullet()
                new_bullet.rect.x = self.rect.x + 22
                new_bullet.rect.y = self.rect.y
                self.bullets.add(new_bullet)
                self.reload = 0
        
    def get_hit(self):
        if self.is_alive:
            self.hp -= 1
            self.snd_hit.play()
            self.hud.health_bar.decrease_hp_value()
            if self.hp <= 0:
                self.hp = 0
                self.death()

    def death(self):
        self.lives -= 1
        if self.lives <= 0:
            self.lives = 0
            self.is_alive = False
            self.image = pygame.Surface((0,0))
        self.hp = self.max_hp
        self.hud.health_bar.reset_health_to_max()
        self.hud.lives.decrement_life()
        self.rect.x = c.DISPLAY_WIDTH // 2
        self.is_invincible = True
        self.invincibility_timer = self.max_invincibility_timer