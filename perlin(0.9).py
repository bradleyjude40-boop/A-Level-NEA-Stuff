import random, math, sys, pygame

width=500
height=500
gridh=10
gridw=10
Clock=pygame.time.Clock()
StandardHeight=100
FPS=60
grid = [[100 for i in range(gridw)] for j in range(gridh)]
screen=pygame.display.set_mode((width,height),pygame.RESIZABLE)

def Height(StandardHeight):
    x1=random.randint(-15,15)
    x2=random.randint(-15,15)
    x=x1+x2
    height=StandardHeight+x
    return height

def worldgen(gridw,gridh,StandardHeight):
    out = False
    for i in range(0,gridw):
        for j in range(0,gridh):
            #making distance from standard
            height = Height(StandardHeight)
            if i>=1: #ensuring no range error
                temp1=int(grid[i-1][j])
                while height < temp1+5 or height < temp1-5:
                    height=Height(StandardHeight)               # preventing too large of a gap in height by comparing with the space behind
                if j>=1:                                        #ensuring no range error
                    temp2=int(grid[i][j-1])
                    #checking difference between position above and left, if they are greater than the maximum difference allowed sets new height to the average of them
                    if abs(temp1-temp2)>10: 
                        height=(temp1+temp2)/2
                        out=True
                    while height > temp2+5 or height < temp2-5:
                        if out==True:
                            out=False
                            break
                        height=Height(StandardHeight)
            elif j>=1:
                temp1=temp2=grid[i][j-1]
            grid[i][j]=math.ceil(height)
    print(grid)
    for i in grid:
        print(" ".join(str(i)))
    return grid

run=True
grid=worldgen(gridw,gridh,StandardHeight)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
        pygame.quit()
        sys.exit()

    Clock.tick(FPS) 
    pygame.display.update() 
pygame.quit()