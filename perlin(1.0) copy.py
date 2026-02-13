import random, math, sys, pygame

width=400
height=400
w=200
h=200
ran=30
stdheight=100
grid= [[100 for i in range(h+1)] for j in range(w+1)]
World=False

def heights(ran, stdheight):
    x1=random.randint(-ran,ran)
    x2=random.randint(-ran,ran)
    x=x1+x2
    height=stdheight+x
    return height
    
def make(i,j,ran,stdheight,comp):
    tempx=100
    tempy=100
    out=False

    if j>=1:
            tempy=grid[i][j-1]

    if comp:
        if i<w:
            tempx=grid[i+1][j]
        if abs(tempx-tempy)>ran/1.5:
            height=(tempx+tempy)/2
            grid[i][j]=math.ceil(height)
            out=True
    else:
        if i>=1:
            tempx=grid[i-1][j]
        if abs(tempx-tempy)>ran/3:
            height=(tempx+tempy)/2
            grid[i][j]=math.ceil(height)
            out=True

    height=heights(ran,stdheight)
    if comp:
        while abs(tempx-height)>ran/3 or abs(tempy-height)>ran/3:
           height=heights(ran,stdheight)
    else:
        while abs(tempx-height)>ran/6 or abs(tempy-height)>ran/6:
               height=heights(ran,stdheight)
    grid[i][j]=height
    return out

def gen(h,w,ran,stdheight):
    for j in range(0,h):
        for i in range(0,w):
            out=make(i,j,ran,stdheight, False)
            c=grid[i][j]
            pygame.draw.rect(screen,(0,c,0),pygame.Rect(i*size,j*size,size,size))
            pygame.display.update() 
            if out==True:
                out=False
                continue
    gen2(h,w,ran)
    return grid

def gen2(h,w,ran):
    for j in range(0,h):
        for i in range(0,w):
            i=w-i
            height=grid[i][j]
            out=make(i,j,ran,height, True)  
            c=grid[i][j]
            pygame.draw.rect(screen,(0,c,0),pygame.Rect(i*size,j*size,size,size))
            pygame.display.update()       
            if out == True:
                out=False
                continue

run=True

Clock=pygame.time.Clock()
FPS=60
screen=pygame.display.set_mode((width,height),pygame.RESIZABLE)
pygame.display.set_caption("perlin or something, idk")

size=2

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        break
    (x,y)=pygame.mouse.get_pos()
    screen.fill((255,255,255))
    if pygame.mouse.get_pressed()[0]:
        if 910<x<1010 and 515<y<565:
            print("making")
            grid = gen(h,w,ran,stdheight)
            World=True
            print("made")
    elif keys[pygame.K_SPACE]:
        print("making")
        grid = gen(h,w,ran,stdheight)
        World=True
        print("made")

    if World:
        for i in range(0,w):
            for j in range(0,h):
                c=grid[i][j]
                pygame.draw.rect(screen,(0,c,0),pygame.Rect(i*size,j*size,size,size))

    pygame.draw.rect(screen,(0,0,0),pygame.Rect(width/2-50,height/2-25,100, 50))
    Clock.tick(FPS) 
    pygame.display.update() 
pygame.quit()
sys.exit()