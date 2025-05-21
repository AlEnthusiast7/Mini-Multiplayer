import pygame
from settings import*

class player(pygame.sprite.Sprite):
    def __init__(self,x ,y, width, height, color):
        super().__init__()
        self.x = x
        self.y = y

        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.vel = 3


    def draw(self, win,color):
        pygame.draw.rect(win,color,self.rect)

    def move(self,k):


        if k["left"]:
            self.rect.x -= self.vel
        if k["right"]:
            self.rect.x += self.vel
        if k["down"]:
            self.rect.y += self.vel
        if k["up"]:
            self.rect.y -= self.vel
        #self.update()

        if self.rect.left > WINDOW_WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WINDOW_WIDTH
        if self.rect.top >= WINDOW_HEIGHT:
            self.rect.bottom = 0



    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
