import random;
import numpy as np;
cluster=[];
x_center=250;
y_center=250;
n=100;
width=50;
height=50;
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

vel=[[random.uniform(-x_vel, x_vel), random.uniform(-y_vel, y_vel)] for i in range(n)];
cluster=np.array(cluster);
vel=np.array(vel);

import pygame
pygame.init()

win = pygame.display.set_mode((500,500));

run=True;
while run:
    win.fill((0,0,0));
    pygame.time.delay(int(dt*1000));
    
    acc=[[random.uniform(-x_acc, x_acc), random.uniform(-y_acc, y_acc)] for i in range(n)];
    acc=np.array(acc);
    
    
    vel=np.add(vel, acc*dt);
    
    for i in range(n):
        [x_pos, y_pos]=cluster[i];
        if x_pos<0 or x_pos>500:
            vel[i,0]*=-1;
        if y_pos<0 or y_pos>500:
            vel[i,1]*=-1;
        
        
    
    cluster=np.add(cluster, vel*dt);
    cluster_rounded=np.rint(cluster);
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False;
    
    for pos in cluster_rounded:
        pygame.draw.circle(win, (255, 255, 255), (int(pos[0]), int(pos[1])), r)
    
    pygame.display.update();
    
pygame.quit();
