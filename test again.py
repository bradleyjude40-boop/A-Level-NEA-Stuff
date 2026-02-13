import pygame, random, sys, math

w=20
h=20
ran=10
stdheight=100
grid= [[10 for i in range(w)] for j in range(h)]


def heights(ran, stdheight):
    x1=random.randint(-ran,ran)
    x2=random.randint(-ran,ran)
    x=x1+x2
    height=stdheight+x
    return height



def gen(w,h,ran,stdheight):
    for j in range(0,h):
        for i in range(0,w):
            tempx=100
            tempy=100
            if i>=1:
                tempx=grid[i-1][j]
            
            if j>=1:
                tempy=grid[i][j-1]

            if abs(tempx-tempy)>10:
                height=(tempx+tempy)/2
                grid[i][j]=math.ceil(height)
                continue

            height=heights(ran,stdheight)
            while abs(tempx-height)>5 or abs(tempy-height)>5:
                height=heights(ran,stdheight)
            grid[i][j]=math.ceil(height)
    return grid

grid = gen(w,h,ran,stdheight)

for i in grid:
    print("".join(str(i)))