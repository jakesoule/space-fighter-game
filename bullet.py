import pygame
import constants as c

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.width = 4
        self.height = self.width
        self.size = (self.height, self.width)
        self.image = pygame.Surface(self.size)
        self.color = (255, 255, 255)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.vel_x = 0
        self.vel_y = -8

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def set_vel_y(self, y):
        self.vel_y = y
    
    def transform(self, x, y):
        self.image = pygame.transform.scale(self.image, (x, y))