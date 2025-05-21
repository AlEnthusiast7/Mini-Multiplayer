import pygame
import math
from settings import*


class laser(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height,target):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.target = target

        self.dx = self.target[0] - self.x
        self.dy = self.target[1] - self.y
        self.angle = (-math.degrees(math.atan2(self.dy, self.dx))-90) %360


        self.direction = pygame.math.Vector2(self.target[0]-self.x,self.target[1]-self.y).normalize()
        self.vel = 3

    def update(self):
        if pygame.math.Vector2(self.x,self.y).distance_to(self.target) < 5:
            return False
        self.x += (self.direction*self.vel)[0]
        self.y += (self.direction*self.vel)[1]
        #self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return True

    def draw(self,win,image):
        image = pygame.transform.rotate(image, self.angle)
        self.rect = image.get_rect(center =(self.x, self.y))
        win.blit(image, self.rect)
        # pygame.draw.rect(win,self.color,self.rect)

