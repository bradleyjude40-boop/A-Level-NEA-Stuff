import random, math, sys, pygame, time

width=1920
height=1080
w=320
h=180
ran=30
stdheight=100
grid = [[100 for i in range(h+1)] for j in range(w+1)]
obsgrid = [[0 for i in range(h+1)] for j in range(w+1)]
gridhealth=[[0 for i in range(h+1)] for j in range(w+1)]
inventory = [["null" for i in range (3)] for j in range(12)]
inventory[0][0], inventory[1][0] = 0,0
location=[100,100]
ui="Home"
uichange=False
TREE=-1
hand = inventory[0][0]
facing="left"

obsdict={
    "tree":{"health":12,
            "tool":"axe",
            "toughness":0,
            "drop":("wood","sapling","fibre")
            },
    "rock":{"health":20,
            "tool":"pickaxe",
            "toughness":1,
            "drop":("stone")
    }
}



def heights(ran, stdheight):
    x1=random.randint(-ran,ran)
    x2=random.randint(-ran,ran)
    x=x1+x2
    height=stdheight+x
    return height
    
# i = current x position, j = current y position, stdheight = height before change, comp = 
def make(i,j,ran,stdheight,comp): 
    tempx=100
    tempy=100
    out=False

    if j>=1:
            tempy=grid[i][j-1] #if the grid position is against the top then it will use 100 as the tempy value, if not it will use the position above it

    if comp:    #if generating from the second direction
        if i<w:
            tempx=grid[i+1][j]  #position to the right
        if abs(tempx-tempy)>ran/1.5:    # checks difference between positions of right and above, if difference is more than 10 then it takes the average
            height=(tempx+tempy)/2
            grid[i][j]=math.ceil(height)
            out=True
    else:   #if generating from the first direction
        if i>=1: 
            tempx=grid[i-1][j]  #position to the left
        if abs(tempx-tempy)>ran/3:  # checks difference between positions of left and above, if difference is more than 5 then it takes the average
            height=(tempx+tempy)/2
            grid[i][j]=math.ceil(height)
            out=True

    height=heights(ran,stdheight)
    if comp:    
        while abs(tempx-height)>ran/4 or abs(tempy-height)>ran/4:   #repeats if too far away from either right or above
           height=heights(ran,stdheight)
    else:
        while abs(tempx-height)>ran/6 or abs(tempy-height)>ran/6:   #repeats if too far away from either left or above
               height=heights(ran,stdheight)
    grid[i][j]=height
    return out

def gen(h,w,ran,stdheight, grid):   #generates comparing to left and above
    for j in range(0,h):
        for i in range(0,w):
            out=make(i,j,ran,stdheight, False)
            c=grid[i][j]
            pygame.draw.rect(screen,(0,c,0),pygame.Rect(i*4,j*4,4,4))
            if out==True:
                out=False
                continue
        pygame.display.update()
    gen2(h,w,ran, grid, obsgrid)
    return grid

def gen2(h,w,ran, grid,obsgrid):        #generates comparing to right and above after the first gen function
    for j in range(0,h):
        for i in range(0,w):
            i=w-i
            height=grid[i][j]
            out=make(i,j,ran,height, True)  
            c=grid[i][j]
            pygame.draw.rect(screen,(0,c,0),pygame.Rect(i*4,j*4,4,4))
            
            if out == True:
                out=False
                continue
        pygame.display.update()
    for i in grid:
        print
    obsgrid = obstructions(h,w,obsgrid)
    return grid

def obstructions(h,w,obsgrid):  # introduces obstacles, currently only trees
    for i in range(0,int(math.ceil(math.sqrt(w*h)))):   # a number of trees 
        a=random.randint(1,w-1)
        b=random.randint(1,h-1)
        obsgrid[a][b]=TREE
        gridhealth[a][b]=obsdict['tree']['health']

def movement(location, keys,facing):    # movement in 4 directions
    a=location[0]
    b=location[1]
    if (keys[pygame.K_w] or keys[pygame.K_UP]) and gridhealth[(a)//3+1][(b-1)//3]<=0 and gridhealth[(a+2)//3+1][(b-1)//3]<=0: #checking for collisions with each movement
        location[1]-=1
        facing="up"
    if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and gridhealth[(a)//3+1][(b)//3+1]<=0 and gridhealth[(a+2)//3+1][(b)//3+1]<=0:
        location[1]+=1
        facing="down"
    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and gridhealth[(a+2)//3][(b+2)//3]<=0 and gridhealth[(a+2)//3][(b)//3]<=0:
        location[0]-=1
        facing="left"
    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and gridhealth[(a)//3+2][(b+2)//3]<=0 and gridhealth[(a)//3+2][(b)//3]<=0:
        location[0]+=1
        facing="right"
        
    if location[0]<0:   #edge checking
        location[0]=0
    elif location[0]>w*3-4*size+25:
        location[0]=w*3-4*size+25
    if location[1]<0:
        location[1]=0
    elif location[1]>h*3-2*size+10:
        location[1]=h*3-2*size+10
    return facing

def showworld(grid):    #displaying the world in all 9 zones
    if 93<location[0]<=w*3-192 and 48<location[1]<=h*3-108: #centre
        for i in range(0,65):
            for j in range(0,37):
                a=location[0]//3+i-30
                b=location[1]//3+j-16
                c=obsgrid[a][b]
                d=grid[a][b]
                match c:
                    case -1:
                        pygame.draw.rect(screen,(130,75,0),pygame.Rect(i*size-location[0]%3*10,j*size-location[1]%3*10,size,size))
                    case _:
                        pygame.draw.rect(screen,(0,d,0),pygame.Rect(i*size-location[0]%3*10,j*size-location[1]%3*10,size,size))
        pygame.draw.rect(screen,(0,0,0), pygame.Rect((31*size),(16*size),size,size))
    
    elif location[0]<=93:   #left collumn
            
        if location[1]<48:  # top left
            for i in range(0,65):
                for j in range(0,37):
                    a=90//3+i-30
                    b=48//3+j-16
                    c=obsgrid[a][b]
                    d=grid[a][b]
                    match c:
                        case -1:
                            pygame.draw.rect(screen,(130,75,0),pygame.Rect(i*size-90%3*10-30,j*size-48%3*10,size,size))
                        case _:
                            pygame.draw.rect(screen,(0,d,0),pygame.Rect(i*size-90%3*10-30,j*size-48%3*10,size,size))
            pygame.draw.rect(screen,(0,0,0), pygame.Rect((location[0]*size/3), (location[1]*size/3), size, size))

        elif location[1]>=h*3-108:  # bottom left
            for i in range(0,65):
                for j in range(0,37):
                    a=90//3+i-30
                    b=h+j-52
                    c=obsgrid[a][b]
                    d=grid[a][b]
                    match c:
                        case -1:
                            pygame.draw.rect(screen,(130,75,0),pygame.Rect(i*size-90%3*10-30,j*size-48%3*10-10,size,size))
                        case _:
                            pygame.draw.rect(screen,(0,d,0),pygame.Rect(i*size-90%3*10-30,j*size-48%3*10-10,size,size))
            pygame.draw.rect(screen,(0,0,0), pygame.Rect((location[0]*size/3), (location[1]*size/3-3850), size, size))

        else:   # middle left
            for i in range(0,65):
                for j in range(0,37):
                    a=90//3+i-30
                    b=location[1]//3+j-16
                    c=obsgrid[a][b]
                    d=grid[a][b]
                    match c:
                        case -1:
                            pygame.draw.rect(screen,(130,75,0),pygame.Rect(i*size-90%3*10-30,j*size-location[1]%3*10,size,size))
                        case _:
                            pygame.draw.rect(screen,(0,d,0),pygame.Rect(i*size-90%3*10-30,j*size-location[1]%3*10,size,size))
            pygame.draw.rect(screen,(0,0,0), pygame.Rect((location[0]*size/3), (16*size), size, size))

            
    elif location[0]>w*3-192: # right collumn

        if location[1]<48: #top right
            for i in range(0,65):
                for j in range(0,37):
                    a=(w*3-192)//3+i-30
                    b=48//3+j-16
                    c=obsgrid[a][b]
                    d=grid[a][b]
                    match c:
                        case -1:
                            pygame.draw.rect(screen,(130,75,0),pygame.Rect(i*size-90%3*10-10,j*size-48%3*10,size,size))
                        case _:
                            pygame.draw.rect(screen,(0,d,0),pygame.Rect(i*size-90%3*10-10,j*size-48%3*10,size,size))
            pygame.draw.rect(screen,(0,0,0), pygame.Rect((location[0]*size/3-6760), (location[1]*size/3), size, size))

        elif location[1]>h*3-108:   # bottom right
            for i in range(0,65):
                for j in range(0,37):
                    a=(w*3-192)//3+i-30
                    b=(h*3)//3+j-52
                    c=obsgrid[a][b]
                    d=grid[a][b]
                    match c:
                        case -1:
                            pygame.draw.rect(screen,(130,75,0),pygame.Rect(i*size-90%3*10-10,j*size-48%3*10-10,size,size))
                        case _:
                            pygame.draw.rect(screen,(0,d,0),pygame.Rect(i*size-90%3*10-10,j*size-48%3*10-10,size,size))
            pygame.draw.rect(screen,(0,0,0), pygame.Rect((location[0]*size/3-6760), (location[1]*size/3-3850), size, size))

        else:   # middle right
            for i in range(0,65):
                for j in range(0,37):
                    a=(w*3-192)//3+i-30
                    b=location[1]//3+j-16
                    c=obsgrid[a][b]
                    d=grid[a][b]
                    match c:
                        case -1:
                            pygame.draw.rect(screen,(130,75,0),pygame.Rect(i*size-93%3*10-10,j*size-location[1]%3*10,size,size))
                        case _:
                            pygame.draw.rect(screen,(0,d,0),pygame.Rect(i*size-93%3*10-10,j*size-location[1]%3*10,size,size))
            pygame.draw.rect(screen,(0,0,0), pygame.Rect((location[0]*10-6760), (16*size), size, size))

    elif location[1]<=48:   #top middle
        for i in range(0,65):
            for j in range(0,37):
                a=location[0]//3+i-30
                b=48//3+j-16
                c=obsgrid[a][b]
                d=grid[a][b]
                match c:
                    case -1:
                        pygame.draw.rect(screen,(130,75,0),pygame.Rect(i*size-location[0]%3*10,j*size-48%3*10,size,size))
                    case _:
                        pygame.draw.rect(screen,(0,d,0),pygame.Rect(i*size-location[0]%3*10,j*size-48%3*10,size,size))
        pygame.draw.rect(screen,(0,0,0), pygame.Rect((31*size), (location[1]*size/3), size, size))
        
    elif location[1]>h*3-108:   # bottom middle
        for i in range(0,65):
            for j in range(0,37):
                a=location[0]//3+i-30
                b=(h*3)//3+j-52
                c=obsgrid[a][b]
                d=grid[a][b]
                match c:
                    case -1:
                        pygame.draw.rect(screen,(130,75,0),pygame.Rect(i*size-location[0]%3*10,j*size-48%3*10-10,size,size))
                    case _:
                        pygame.draw.rect(screen,(0,d,0),pygame.Rect(i*size-location[0]%3*10,j*size-48%3*10-10,size,size))
        pygame.draw.rect(screen,(0,0,0), pygame.Rect((31*size), (location[1]*size/3-3850), size, size))

def interact(obsgrid, gridhealth, location, hand):  #allows player to break and interact with obstacles
    if obsgrid[location[0]//3+2][location[1]//3]<0 and facing=="right":
        currentobstaclelocation=(location[0]//3+2,location[1]//3)
    elif obsgrid[location[0]//3][location[1]//3]<0 and facing=="left":
        currentobstaclelocation=(location[0]//3,location[1]//3)
    elif obsgrid[location[0]//3+1][location[1]//3+1]<0 and facing=="down":
        currentobstaclelocation=(location[0]//3+1,location[1]//3+1)
    elif obsgrid[location[0]//3+1][location[1]//3-1]<0 and facing=="up":
        currentobstaclelocation=(location[0]//3+1,location[1]//3-1)
    else:
        currentobstaclelocation=(-1,-1)
    
    if pygame.mouse.get_pressed()[0]:
        gridhealth[currentobstaclelocation[0]][currentobstaclelocation[1]]-=1
        if gridhealth[currentobstaclelocation[0]][currentobstaclelocation[1]]<=0:


            gridhealth[currentobstaclelocation[0]][currentobstaclelocation[1]]=0
            obsgrid[currentobstaclelocation[0]][currentobstaclelocation[1]]=0
 
def drops(obsgrid, obsdict):    #will be where obstacles are broken and dropped on the floor
    1+1==2

run=True

Clock=pygame.time.Clock()
FPS=60
screen=pygame.display.set_mode((width,height),pygame.RESIZABLE)
pygame.display.set_caption("display screen idk why w bosons have charge and z bosons don't")
temp=0
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

            if keys[pygame.K_ESCAPE] and uichange!=True:
                ui="Home"
                uichange=True
                temp=30
            elif keys[pygame.K_e]:
                ui="inv"
            elif keys[pygame.K_1]:
                hand=inventory[0][0]
            elif keys[pygame.K_2]:
                hand=inventory[1][0] 
            facing=movement(location,keys,facing)
            
            interact(obsgrid, gridhealth, location, hand)
            
            showworld(grid)
            if uichange:
                temp-=1
                if temp<=0:
                    uichange=False
            
        
        case "inv":
            keys = pygame.key.get_pressed()
            (x,y)=pygame.mouse.get_pos()
            for i in range(0,12):
                for j in range(0,3):
                    pygame.draw.rect(screen,(150,150,150), pygame.Rect(420+i*90,480+j*90,90,90))
                    if inventory[i][j]=="null":
                        pygame.draw.rect(screen,(00,00,00), pygame.Rect(425+i*90,485+j*90,80,80))
                    else:
                        if 425+i*90<x<505+i*90 and 485+j*90<y<565+j*90:
                            pygame.draw.rect(screen,(90,90,90), pygame.Rect(425+i*90,485+j*90,80,80))
                        else:
                            pygame.draw.rect(screen,(100,100,100), pygame.Rect(425+i*90,485+j*90,80,80))
            if keys[pygame.K_ESCAPE]:
                ui="World"
                uichange=True
                temp=30
        
    Clock.tick(FPS) 
    pygame.display.update() 
pygame.quit()
sys.exit()
