import random, math, sys, pygame

width=1920
height=1080
w=480
h=270
ran=50
stdheight=100
count=0
grid= [[100 for i in range(h)] for j in range(w)]


def heights(ran, stdheight,count):
    x1=random.randint(-ran,ran)
    x2=random.randint(-ran,ran)
    x=x1+x2
    height=stdheight+x
    count+=4
    return height



def gen(h,w,ran,stdheight,count):
    for j in range(0,h):
        for i in range(0,w):
            tempx=100
            tempy=100
            if i>=1:
                tempx=grid[i-1][j]
                count+=1
            
            if j>=1:
                tempy=grid[i][j-1]
                count+=1

            if abs(tempx-tempy)>ran:
                height=(tempx+tempy)/5
                grid[i][j]=math.ceil(height,count)
                continue

            height=heights(ran,stdheight,count)
            while abs(tempx-height)>ran/9 or abs(tempy-height)>ran/9:
                height=heights(ran,stdheight,count)
                count+=2
            grid[i][j]=height
            count+=3
    print(count)
    return grid

run=True
grid=gen(h,w,ran,stdheight,count)
#for i in grid:
#    print("".join(str(i)))


Clock=pygame.time.Clock()
FPS=60
screen=pygame.display.set_mode((width,height),pygame.RESIZABLE)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
        pygame.quit()
        sys.exit()
    for i in range(0,w):
        for j in range(0,h):
            c=grid[i][j]
            pygame.draw.rect(screen,(40,c,0),pygame.Rect(i*4,j*4,4,4))
    Clock.tick(FPS) 
    pygame.display.update() 
pygame.quit()