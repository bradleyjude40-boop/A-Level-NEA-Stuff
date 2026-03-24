import random, math, sys, pygame, time

width=1920
height=1080
w=320
h=180
ran=30
stdheight=100
grid= [[100 for i in range(h+1)] for j in range(w+1)]
location=[300,300]
ui="Home"
uichange=False
TREE=-1


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

def gen(h,w,ran,stdheight, grid):
    for j in range(0,h):
        for i in range(0,w):
            out=make(i,j,ran,stdheight, False)
            #c=grid[i][j]
            #pygame.draw.rect(screen,(0,c,0),pygame.Rect(i*4,j*4,4,4))
            #pygame.display.update() 
            if out==True:
                out=False
                continue
    gen2(h,w,ran, grid)
    return grid

def gen2(h,w,ran, grid):
    for j in range(0,h):
        for i in range(0,w):
            i=w-i
            height=grid[i][j]
            out=make(i,j,ran,height, True)  
            #c=grid[i][j]
            #pygame.draw.rect(screen,(0,c,0),pygame.Rect(i*4,j*4,4,4))
            #pygame.display.update()       
            if out == True:
                out=False
                continue
    grid = obstructions(h,w,grid)
    return grid

def obstructions(h,w,grid):
    for i in range(0,int(math.ceil(math.sqrt(w*h)))):
        grid[random.randint(0,w)][random.randint(0,h)]=TREE
    return grid

def movement(location, keys):

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        location[1]-=1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        location[1]+=1

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        location[0]-=1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        location[0]+=1
        
    if location[0]<0:
        location[0]=0
    elif location[0]>w*3-2*size:
        location[0]=(w*3-2*size)
    if location[1]<0:
        location[1]=0
    elif location[1]>h*3-2*size:
        location[1]=(h*3-2*size)

def showworld(grid):
    if 93<=location[0]<=w*3-192 and 51<=location[1]<=h*3-108:
        for i in range(0,65):
            for j in range(0,37):
                a=location[0]//3+i-30
                b=location[1]//3+j-16
                c=grid[a][b]
                match c:
                    case -1:
                        pygame.draw.rect(screen,(130,75,0),pygame.Rect(i*size-location[0]%3*10,j*size-location[1]%3*10,size,size))
                    case _:
                        pygame.draw.rect(screen,(0,c,0),pygame.Rect(i*size-location[0]%3*10,j*size-location[1]%3*10,size,size))
        pygame.draw.rect(screen,(0,0,0), pygame.Rect((31*size),(17*size),2*size,2*size))
    
    elif location[0]<93:
            
        if location[1]<51:
            for i in range(0,65):
                for j in range(0,37):
                    a=90//3+i-30
                    b=48//3+j-16
                    c=grid[a][b]
                    match c:
                        case -1:
                            pygame.draw.rect(screen,(130,75,0),pygame.Rect(i*size-90%3*10,j*size-48%3*10,size,size))
                        case _:
                            pygame.draw.rect(screen,(0,c,0),pygame.Rect(i*size-90%3*10,j*size-48%3*10,size,size))
            pygame.draw.rect(screen,(0,0,0), pygame.Rect((location[0]*size/3), (location[1]*size/3), 2*size, 2*size))

        elif location[1]>=h*3-108:
            for i in range(0,65):
                for j in range(0,37):
                    a=90//3+i-30
                    b=h+j-52
                    c=grid[a][b]
                    match c:
                        case -1:
                            pygame.draw.rect(screen,(130,75,0),pygame.Rect(i*size-90%3*10,j*size-48%3*10,size,size))
                        case _:
                            pygame.draw.rect(screen,(0,c,0),pygame.Rect(i*size-90%3*10,j*size-48%3*10,size,size))
            pygame.draw.rect(screen,(0,0,0), pygame.Rect((location[0]*size/3), (location[1]*size/3-3800), 2*size, 2*size))

        else:
            for i in range(0,65):
                for j in range(0,37):
                    a=90//3+i-30
                    b=location[1]//3+j-16
                    c=grid[a][b]
                    match c:
                        case -1:
                            pygame.draw.rect(screen,(130,75,0),pygame.Rect(i*size-90%3*10,j*size-location[1]%3*10,size,size))
                        case _:
                            pygame.draw.rect(screen,(0,c,0),pygame.Rect(i*size-90%3*10,j*size-location[1]%3*10,size,size))
            pygame.draw.rect(screen,(0,0,0), pygame.Rect((location[0]*size/3), (17*size), 2*size, 2*size))

            
    elif location[0]>w*3-192:
        if location[1]<51:
            for i in range(0,65):
                for j in range(0,37):
                    a=(w*3-192)//3+i-30
                    b=48//3+j-16
                    c=grid[a][b]
                    match c:
                        case -1:
                            pygame.draw.rect(screen,(130,75,0),pygame.Rect(i*size-90%3*10,j*size-48%3*10,size,size))
                        case _:
                            pygame.draw.rect(screen,(0,c,0),pygame.Rect(i*size-90%3*10,j*size-48%3*10,size,size))
            pygame.draw.rect(screen,(0,0,0), pygame.Rect((location[0]*size/3-6756), (location[1]*size/3), 2*size, 2*size))

        elif location[1]>=h*3-108:
            for i in range(0,65):
                for j in range(0,37):
                    a=(w*3-192)//3+i-30
                    b=(h*3)//3+j-52
                    c=grid[a][b]
                    match c:
                        case -1:
                            pygame.draw.rect(screen,(130,75,0),pygame.Rect(i*size-90%3*10,j*size-48%3*10,size,size))
                        case _:
                            pygame.draw.rect(screen,(0,c,0),pygame.Rect(i*size-90%3*10,j*size-48%3*10,size,size))
            pygame.draw.rect(screen,(0,0,0), pygame.Rect((location[0]*size/3-6756), (location[1]*size/3-3800), 2*size, 2*size))

        else:
            for i in range(0,65):
                for j in range(0,37):
                    a=(w*3-192)//3+i-30
                    b=location[1]//3+j-16
                    c=grid[a][b]
                    match c:
                        case -1:
                            pygame.draw.rect(screen,(130,75,0),pygame.Rect(i*size-93%3*10,j*size-location[1]%3*10,size,size))
                        case _:
                            pygame.draw.rect(screen,(0,c,0),pygame.Rect(i*size-93%3*10,j*size-location[1]%3*10,size,size))
            pygame.draw.rect(screen,(0,0,0), pygame.Rect((location[0]*size/3-6756), (17*size), 2*size, 2*size))

run=True

Clock=pygame.time.Clock()
FPS=60
screen=pygame.display.set_mode((width,height),pygame.RESIZABLE)
pygame.display.set_caption("display screen idk why w bosons have charge and z bosons don't")
temp=30
size=30

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False


    match ui:
        case "Home":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] and uichange==False:
                break
            (x,y)=pygame.mouse.get_pos()
            screen.fill((255,255,255))
            pygame.draw.rect(screen,(0,0,0),pygame.Rect(width/2-50,height/2-25,100, 50))
            pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                if 910<x<1010 and 515<y<565:
                    print("making")
                    ui="World"
                    grid = gen(h,w,ran,stdheight, grid)
                    print("made")
            elif keys[pygame.K_SPACE]:
                print("making")
                ui="World"
                grid = gen(h,w,ran,stdheight, grid)
                print("made")
            
            if uichange:
                temp-=1
                if temp<=0:
                    uichange=False

        case "World":
            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                ui="Home"
                uichange=True
            elif keys[pygame.K_e]:
                ui="inv"

            movement(location,keys)

            showworld(grid)
            
        
        case "inv":
            keys = pygame.key.get_pressed()
            for i in range(0,12):
                for j in range(0,3):
                    pygame.draw.rect(screen,(150,150,150), pygame.Rect(420+i*90,480+j*90,90,90))
                    pygame.draw.rect(screen,(100,100,100), pygame.Rect(425+i*90,485+j*90,80,80))
            if keys[pygame.K_ESCAPE]:
                ui="World"
                uichange=True
        
    Clock.tick(FPS) 
    pygame.display.update() 
pygame.quit()
sys.exit()