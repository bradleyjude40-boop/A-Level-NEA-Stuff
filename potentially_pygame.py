import pygame, sys, math, random
num=6
width=318*num
height=159*num
BGr,BGg,BGb=175,175,175
screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
pygame.display.set_caption("GameyThing")
Clock = pygame.time.Clock()
run = True
shape=pygame.Rect(10,10,10,10)
ishigami=pygame.image.load("resources\images.png")
while run and 1==1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
        pygame.quit()
        sys.exit()
    screen.fill((BGr, BGg, BGb)) 
    pygame.draw.circle(screen,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(width/2,height/2), math.sqrt(width*height/100))
    for i in range(0,num):
        for j in range(0,num):
            #screen.blit(ishigami,(i*318,j*159))
            x=1+1
    Clock.tick(60) 
    pygame.display.update() 
pygame.quit()