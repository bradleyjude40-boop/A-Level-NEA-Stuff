import random, math, sys, pygame, pygame.freetype, pathlib, os

width=1920
height=1080
w=320
h=180
ran=30
stdheight=100
grid = [[100 for i in range(h+1)] for j in range(w+1)]
obsgrid = [["null" for i in range(h+1)] for j in range(w+1)]
gridhealth=[[0 for i in range(h+1)] for j in range(w+1)]
dropgrid = [[0 for i in range((h+1))] for j in range((w+1))]
location=[100,100]
ui="Home"
uichange=False
TREE=-1
hand =[0,0]


dropgrid[100//3][105//3]="pickaxe"

def image_finding(name):
    global images
    for path in pathlib.Path(".").rglob(name):
        return path.resolve()

obsdict={
    "Tree":{"health":12,
            "tool":"axe",
            "toughness":0,
            "drops":("sapling","log"),
            "colour":(130,75,0)
            },
    "Rock":{"health":20,
            "tool":"pickaxe",
            "toughness":1,
            "drops":(0,"stone"),
            "colour":(175,175,175)
            }
}

itemdict={
    "null": {"sprite":pygame.image.load(os.path.join('sprites', 'null.png')),
            },
             
    "axe":  {"health":100,
            "class":"axe",
            "toughness":1,
            "sprite":pygame.image.load(os.path.join('sprites', 'axe.png')),
            },
    "pickaxe":{"health":100,
            "class":"pickaxe",
            "toughness":1,
            "sprite":pygame.image.load(os.path.join('sprites', 'pickaxe.png')),
            },
    "stone":{"health":0,
            "class":"none",
            "toughness":1,
            "sprite":pygame.image.load(os.path.join('sprites', 'stone.png')),
            "placeable":True
            },
    "log":{"health":0,
            "class":"none",
            "toughness":0,
            "sprite":pygame.image.load(os.path.join('sprites', 'log.png')),
            "placeable":True
            },
    "sapling":{"health":0,
            "class":"none",
            "toughness":0,
            "sprite":pygame.image.load(os.path.join('sprites', 'sapling.png')),
            "placeable":True
            }
}




def heights(ran, stdheight):
    x1=random.randint(-ran,ran)
    x2=random.randint(-ran,ran)
    x=x1+x2
    height=stdheight+x
    return height
    
# i = current x position, j = current y position, stdheight = height before change
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
        while abs(tempx-height)>ran/6 or abs(tempy-height)>ran/6:   #repeats if too far away from either right or above
           height=heights(ran,stdheight)
    else:
        while abs(tempx-height)>ran/4 or abs(tempy-height)>ran/4:   #repeats if too far away from either left or above
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
        GAME_FONT.render_to(screen, (40, 350), "making!", (255,255,255))
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
        GAME_FONT.render_to(screen, (40, 350), "making!", (255,255,255))
        pygame.display.update()
    for i in grid:
        print
    obsgrid = obstructions(h,w,obsgrid)
    return grid

def obstructions(h,w,obsgrid):  # introduces obstacles, currently only trees
    for i in range(0,int(math.ceil(math.sqrt(w*h)))):   # a number of trees 
        a=random.randint(1,w-1)
        b=random.randint(1,h-1)
        obsgrid[a][b]="Tree"
        gridhealth[a][b]=obsdict["Tree"]['health']

    for i in range(0,int(math.ceil(math.sqrt(w*h)/2))):   # a number of rocks 
        a=random.randint(1,w-1)
        b=random.randint(1,h-1)
        obsgrid[a][b]="Rock"
        gridhealth[a][b]=obsdict["Rock"]['health']

def toolcheck(obstacle):
    if obstacle=="null":
        return False
    elif inhand == "null" or inhand == 0:
        GAME_FONT.render_to(screen, (700, 500), "You need a different tool", (255,255,255))
        return False
    elif obsdict[obstacle]['tool']==itemdict[inhand]['class'] and obsdict[obstacle]['toughness']<=itemdict[inhand]['toughness']:
        return True
    else:
        GAME_FONT.render_to(screen, (700, 500), "You need a different tool", (255,255,255))
        pygame.display.update()
        return False

class Player:

    def __init__(self,vel,posx,posy,facing,inventory):
        self.vel=vel
        self.posx=posx
        self.posy=posy
        self.facing=facing
        self.inventory=inventory
        self.image=pygame.Surface((30,30))
        self.image.fill((150,75,0))
        self.rect=self.image.get_rect()

    def movement(self):
        keys=pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]):
            self.facing = "up"
            if gridhealth[(self.posx)//3+1][(self.posy-1)//3]<=0 and gridhealth[(self.posx+2)//3+1][(self.posy-1)//3]<=0:
                self.posy-=self.vel
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]):
            self.facing = "down"
            if gridhealth[(self.posx)//3+1][(self.posy)//3+1]<=0 and gridhealth[(self.posx+2)//3+1][(self.posy)//3+1]<=0:
                self.posy+=self.vel
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.facing = "left"
            if gridhealth[(self.posx+2)//3][(self.posy+2)//3]<=0 and gridhealth[(self.posx+2)//3][(self.posy)//3]<=0:
                self.posx-=self.vel
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.facing = "right"
            if gridhealth[(self.posx)//3+2][(self.posy+2)//3]<=0 and gridhealth[(self.posx)//3+2][(self.posy)//3]<=0:
                self.posx+=self.vel
        
        if self.posx<0:
            self.posx=0
        elif self.posx>865:
            self.posx=865
        if self.posy<0:
            self.posy=0
        elif self.posy>490:
            self.posy=490
        picked = False
        
        for q in range(0,2):
            for r in range(0,2):
                checkposx=(self.posx+q)//3+1
                checkposy=(self.posy+r)//3
                if dropgrid[(checkposx)][(checkposy)]!=0:
                    for i in range(0,12):   
                        for j in range(0,3):
                            if person.inventory[i][j] == 0:
                                person.inventory[i][j]=dropgrid[checkposx][checkposy]
                                dropgrid[checkposx][checkposy]=0
                                picked=True
                            if picked==True:    
                                break
                    if picked==True:
                            break
                if picked==True:
                        break
        self.rect.center=self.posx,self.posy
        return self.facing
    
    def interact(self):
        if obsgrid[self.posx//3+2][self.posy//3]!=0 and self.facing=="right":
            currentobstaclelocation=(self.posx//3+2,self.posy//3)
        elif obsgrid[self.posx//3][self.posy//3]!=0 and self.facing=="left":
            currentobstaclelocation=(self.posx//3,self.posy//3)
        elif obsgrid[self.posx//3+1][self.posy//3+1]!=0 and self.facing=="down":
            currentobstaclelocation=(self.posx//3+1,self.posy//3+1)
        elif obsgrid[self.posx//3+1][self.posy//3-1]!=0 and self.facing=="up":
            currentobstaclelocation=(self.posx//3+1,self.posy//3-1)
        else:
            currentobstaclelocation=(-1,-1)
        if currentobstaclelocation!=(-1,-1):
            if pygame.mouse.get_pressed()[0] and toolcheck(obsgrid[currentobstaclelocation[0]][currentobstaclelocation[1]]):
                gridhealth[currentobstaclelocation[0]][currentobstaclelocation[1]]-=1
                if gridhealth[currentobstaclelocation[0]][currentobstaclelocation[1]]<=0:
                    gridhealth[currentobstaclelocation[0]][currentobstaclelocation[1]]=0
                    drops(currentobstaclelocation, obsgrid, obsdict,dropgrid)
                    obsgrid[currentobstaclelocation[0]][currentobstaclelocation[1]]="null"
    

person=Player(1, location[0],location[1],"right",[["null" for i in range (3)] for j in range(12)])

for i in range(0,12):
    person.inventory[i][0]=0
person.inventory[0][0]="axe"
person.inventory[1][0]="pickaxe"


def showworld(grid):    #displaying the world in all 9 zones
    if 93<person.posx<=w*3-192 and 48<person.posy<=h*3-108: #centre
        for i in range(0,65):
            for j in range(0,37):
                a=person.posx//3+i-30
                b=person.posy//3+j-16
                maplocation=[i*size-person.posx%3*10,j*size-person.posy%3*10]
                personlocation=((31*size),(16*size))
                display(a,b,maplocation)
        
    
    elif person.posx<=93:   #left collumn
        
        if person.posy<48:  # top left
            for i in range(0,65):
                for j in range(0,37):
                    a=90//3+i-30
                    b=48//3+j-16
                    maplocation=[i*size-90%3*10-30,j*size-48%3*10]
                    personlocation=(person.posx*size/3), (person.posy*size/3)
                    display(a,b,maplocation)   


        elif person.posy>=h*3-108:  # bottom left
            for i in range(0,65):
                for j in range(0,37):
                    a=90//3+i-30
                    b=h+j-52
                    maplocation=[i*size-90%3*10-30,j*size-48%3*10-10]
                    personlocation=(person.posx*size/3),(person.posy*size/3-3850)
                    display(a,b,maplocation)   

        else:   # middle left
            for i in range(0,65):
                for j in range(0,37):
                    a=90//3+i-30
                    b=person.posy//3+j-16
                    maplocation=[i*size-90%3*10-30,j*size-person.posy%3*10]
                    personlocation=(person.posx*size/3), (16*size)
                    display(a,b,maplocation)   

            
    elif person.posx>w*3-192: # right collumn

        if person.posy<48: #top right
            for i in range(0,65):
                for j in range(0,37):
                    a=(w*3-192)//3+i-30
                    b=48//3+j-16
                    maplocation=[i*size-90%3*10-10,j*size-48%3*10]
                    personlocation=(person.posx*size/3-6760), (person.posy*size/3)
                    display(a,b,maplocation)   

        elif person.posy>h*3-108:   # bottom right
            for i in range(0,65):
                for j in range(0,37):
                    a=(w*3-192)//3+i-30
                    b=(h*3)//3+j-52
                    maplocation=[i*size-90%3*10-10,j*size-48%3*10-10]
                    personlocation=(person.posx*size/3-6760), (person.posy*size/3-3850)
                    display(a,b,maplocation)   

        else:   # middle right
            for i in range(0,65):
                for j in range(0,37):
                    a=(w*3-192)//3+i-30
                    b=person.posy//3+j-16
                    maplocation=[i*size-93%3*10-10,j*size-person.posy%3*10]
                    personlocation=(person.posx*10-6760), (16*size)
                    display(a,b,maplocation)   

    elif person.posy<=48:   #top middle
        for i in range(0,65):
            for j in range(0,37):
                a=person.posx//3+i-30
                b=48//3+j-16
                maplocation=[i*size-person.posx%3*10,j*size-48%3*10]
                personlocation=(31*size), (person.posy*size/3)
                display(a,b,maplocation)   
        
    elif person.posy>h*3-108:   # bottom middle
        for i in range(0,65):
            for j in range(0,37):
                a=person.posx//3+i-30
                b=(h*3)//3+j-52
                maplocation=[i*size-person.posx%3*10,j*size-48%3*10-10]
                personlocation=(31*size), (person.posy*size/3-3850)
                display(a,b,maplocation)   
                

    pygame.draw.rect(screen,(0,0,0), pygame.Rect(personlocation[0],personlocation[1],size,size))
    
def display(a,b,maplocation):
    c=obsgrid[a][b]
    d=grid[a][b]
    match c:
        case "null":
            pygame.draw.rect(screen,(0,d,0),pygame.Rect(maplocation[0],maplocation[1],size,size))
        case _:
            pygame.draw.rect(screen,obsdict[c]["colour"],pygame.Rect(maplocation[0],maplocation[1],size,size))
    if dropgrid[a][b]!=0:
                            screen.blit(itemdict[dropgrid[a][b]]["sprite"],(maplocation[0],maplocation[1],20,20))
        
def drops(currentobstaclelocation, obsgrid, obsdict,dropgrid):    #where obstacles are broken and dropped on the floor
    for z in range (0, len(obsdict[obsgrid[currentobstaclelocation[0]][currentobstaclelocation[1]]]["drops"])):
        if dropgrid[currentobstaclelocation[0]][currentobstaclelocation[1]]==0:
            a, b = -1, -1
            dropgrid[currentobstaclelocation[0]][currentobstaclelocation[1]] = obsdict[obsgrid[currentobstaclelocation[0]][currentobstaclelocation[1]]]["drops"][z]
        else:
            while dropgrid[currentobstaclelocation[0]+a][currentobstaclelocation[1]+b]!=0:
                b+=1
                if b==2:
                    b=-1
                    a+=1
                if a==2:
                    break
            dropgrid[currentobstaclelocation[0]+a][currentobstaclelocation[1]+b] = obsdict[obsgrid[currentobstaclelocation[0]][currentobstaclelocation[1]]]["drops"][z]

run=True

Clock=pygame.time.Clock()
FPS=120
screen=pygame.display.set_mode((width,height),pygame.RESIZABLE)
pygame.display.set_caption("wild")
temp=0
size=30
inhand = person.inventory[0][0]
pygame.init()
GAME_FONT = pygame.freetype.Font("Roboto-Italic-VariableFont_wdth,wght.ttf", 20)

textlist=("return to game","save","quit to menu")

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
            GAME_FONT.render_to(screen, (width/2-47,height/2-15), "New Game", (255, 255, 255))
            pygame.display.update()
            if pygame.mouse.get_pressed()[0] and 910<x<1010 and 515<y<565 or keys[pygame.K_SPACE]:
                pygame.draw.rect(screen,(0,0,0),pygame.Rect(0,0,width,height))
                ui="World"
                grid = gen(h,w,ran,stdheight, grid)

            if uichange:
                temp-=1
                if temp<=0:
                    uichange=False


        case "World":
            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE] and uichange!=True:
                ui="esc"
                uichange=True
                temp=30
            elif keys[pygame.K_e]:
                ui="inv"
            elif keys[pygame.K_i]:
                ui="craft"
            elif keys[pygame.K_1]:
                inhand=person.inventory[0][0]
                hand=[0,0]
            elif keys[pygame.K_2]:
                inhand=person.inventory[1][0]
                hand=[1,0] 
            elif keys[pygame.K_3]:
                inhand=person.inventory[2][0]
                hand=[2,0] 
            elif keys[pygame.K_4]:
                inhand=person.inventory[3][0]
                hand=[3,0] 
            elif keys[pygame.K_5]:
                inhand=person.inventory[4][0]
                hand=[4,0] 
            elif keys[pygame.K_6]:
                inhand=person.inventory[5][0]
                hand=[5,0] 
            elif keys[pygame.K_7]:
                inhand=person.inventory[6][0]
                hand=[6,0] 
            elif keys[pygame.K_8]:
                inhand=person.inventory[7][0]
                hand=[7,0] 
            elif keys[pygame.K_9]:
                inhand=person.inventory[8][0]
                hand=[8,0] 
            elif keys[pygame.K_0]:
                inhand=person.inventory[9][0]
                hand=[9,0] 
            elif keys[pygame.K_MINUS]:
                inhand=person.inventory[10][0]
                hand=[10,0] 
            elif keys[pygame.K_EQUALS]:
                inhand=person.inventory[11][0]
                hand=[11,0] 
            
            person.movement()

            person.interact()
            
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
                    if hand[0]!=i or hand[1]!=j:    
                        pygame.draw.rect(screen,(150,150,150), pygame.Rect(420+i*90,480+j*90,90,90))
                    else:
                        pygame.draw.rect(screen,(200,200,200), pygame.Rect(420+i*90,480+j*90,90,90))
                    if person.inventory[i][j]=="null":
                        pygame.draw.rect(screen,(00,00,00), pygame.Rect(425+i*90,485+j*90,80,80))
                    else:
                        if 425+i*90<x<505+i*90 and 485+j*90<y<565+j*90:
                            pygame.draw.rect(screen,(90,90,90), pygame.Rect(425+i*90,485+j*90,80,80))
                        else:
                            pygame.draw.rect(screen,(100,100,100), pygame.Rect(425+i*90,485+j*90,80,80))
                    if person.inventory[i][j]in itemdict:
                        screen.blit(pygame.transform.scale((itemdict[person.inventory[i][j]]["sprite"]),(80,80)),(425+i*90,485+j*90,80,80))

            for i in range(0,3):
                for j in range(0,3):
                    pygame.draw.rect(screen,(150,150,150), pygame.Rect(825+i*90,210+j*90,90,90))
                    pygame.draw.rect(screen,(100,100,100), pygame.Rect(830+i*90,215+j*90,80,80))
            if keys[pygame.K_ESCAPE]:
                ui="World"
                uichange=True
                temp=30

        
        case "esc":
            (x,y)=pygame.mouse.get_pos()
            for i in range(0,3):
                pygame.draw.rect(screen,(150,150,150), pygame.Rect(width/2-300,height/2-400+250*i,600,150))
                GAME_FONT.render_to(screen, (width/2-300,height/2-400+250*i), textlist[i], (255,255,255))
            if pygame.mouse.get_pressed()[0] and width/2-300<x<width/2+300 and height/2-400<y<height/2-250:
                ui="World"
            if pygame.mouse.get_pressed()[0] and width/2-300<x<width/2+300 and height/2-150<y<height/2:
                with open("saves.txt","w") as textfile:
                    for line in obsgrid:
                        textfile.write(f"{line}&")
                        textfile.write("\n")
                    textfile.write("\n")
                    textfile.write("\n")
                    for line in dropgrid:
                        textfile.write(f"{line}&")
                        textfile.write("\n")
                    textfile.write("\n")
                    textfile.write("\n")
                    for line in grid:
                        textfile.write(f"{line}&")
                        textfile.write("\n")
                    textfile.write("\n")
                    textfile.write("\n")
                    textfile.write(f"{person.vel}")
                    textfile.write(f"{person.posx}")
                    textfile.write(f"{person.posy}")
                    textfile.write(f"{person.facing}")
                    textfile.write("\n")
                    textfile.write("\n")
                    for line in person.inventory:
                        textfile.write(f"{line}&")
                        textfile.write("\n")
            if pygame.mouse.get_pressed()[0] and width/2-300<x<width/2+300 and height/2+100<y<height/2+250:#
                ui="Home"
                uichange=True
                temp=30
    Clock.tick(FPS) 
    pygame.display.update() 
pygame.quit()
sys.exit()
