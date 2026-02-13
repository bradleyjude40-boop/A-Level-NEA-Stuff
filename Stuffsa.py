import pygame
import math

pygame.init()
W_width=1920
W_height=1080
home=(75,75,75)
skin=(0,0,0)
hair=(0,0,0)
iris=(0,0,0)
cornea=(255,255,255)

PlayerPos=(960,540)

screen = pygame.display.set_mode((W_width,W_height))
pygame.display.set_caption("charTest")

velocity=5

screen.fill(home)
pygame.draw.rect(screen,skin,)