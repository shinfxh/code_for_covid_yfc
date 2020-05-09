def distance(pos_1, pos_2):
    return sqrt(sum((pos_1-pos_2)**2));
    
import random;
import numpy as np;
from math import *;
cluster=[];
x_center=250;
y_center=250;
n=100;
wall_width=150;
wall_height=150;
r=5;
x_vel=[0 for i in range(n)];
y_vel=[0 for i in range(n)];
cluster=[[x_center+random.randrange(-100, 100), y_center+random.randrange(-100, 100)] for i in range(n)];


x_vel=50;
y_vel=50;
dt=0.1;

x_acc=10;
y_acc=10;

x_bias=10;
y_bias=10;

r_infection=10;

vel=[[random.uniform(-x_vel, x_vel), random.uniform(-y_vel, y_vel)] for i in range(n)];
cluster=np.array(cluster);
vel=np.array(vel);

import pygame
pygame.init()

win = pygame.display.set_mode((500,500));

background = pygame.Surface((500, 500))
background.fill(pygame.Color('#292a30'))


infected=[0 for i in range(n)];
first_infection=random.randrange(0,n);
infected[first_infection]=1;

infected_track=[[0 for i in range(n)] for i in range(n)];
infected_track=np.array(infected_track);
min_infection_time=5;

run=True;
while run:
    win.fill((41,42,48));
    pygame.time.delay(int(dt*1000));
    
    
    acc=[[random.uniform(-x_acc, x_acc), random.uniform(-y_acc, y_acc)] for i in range(n)];
    acc=np.array(acc);
    
    new_infected=[];
    
    for i in range(n):
        if infected[i]:
            for j in range(n):
                if i!=j:
                    if distance(cluster[i], cluster[j])<r_infection:
                        infected_track[i][j]+=1;
                        if infected_track[i][j]>=min_infection_time:
                            infected[j]=1;
                    elif infected_track[i][j]!=0:
                        infected_track[i][j]=0;
                
    
    vel=np.add(vel, acc*dt);
    
    for i in range(n):
        [x_pos, y_pos]=cluster[i];
        if x_pos<x_center-wall_width or x_pos>x_center+wall_width:
            vel[i,0]*=-1;
        if y_pos<y_center-wall_height or y_pos>y_center+wall_height:
            vel[i,1]*=-1;
        
        
    
    cluster=np.add(cluster, vel*dt);
    cluster_rounded=np.rint(cluster);
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False;
    
    for i in range(n):
        pos=cluster[i];
        if infected[i]:
            pygame.draw.circle(win, (246, 116, 94), (int(pos[0]), int(pos[1])), r);
        else:
            pygame.draw.circle(win, (180, 209, 164), (int(pos[0]), int(pos[1])), r);
    pygame.draw.rect(win,(200,200,200),(wall_width/2-10,wall_width/2-10,520-wall_width,520-wall_width),3);

    pygame.display.update();
    
pygame.quit();
