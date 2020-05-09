import random;
import numpy as np;
cluster=[];
x_center=250;
y_center=250;
n=100;
width=50;
height=50;
r=5;
xrange=100;
yrange=100;
x_vel=[0 for i in range(n)];
y_vel=[0 for i in range(n)];
cluster=[[x_center+random.randrange(-xrange, xrange), y_center+random.randrange(-yrange, yrange)] for i in range(n)];


x_vel=50;
y_vel=50;
dt=0.1;

x_acc=10;
y_acc=10;



import pygame
pygame.init()

win = pygame.display.set_mode((500,500));

run=True;
while run:
    vel=[[random.uniform(-x_vel, x_vel), random.uniform(-y_vel, y_vel)] for i in range(n)];
    cluster=np.array(cluster);
    vel=np.array(vel);
    
    win.fill((0,0,0));
    pygame.time.delay(int(dt*1000));
    
    
    cluster1=np.add(cluster, vel*dt);
    cluster2=np.add(cluster,-vel*dt);
    cluster=np.where(cluster<500,cluster1,cluster2);
    cluster=np.where(cluster>0,cluster,cluster2);
    cluster_rounded=np.rint(cluster);
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False;
    
    for pos in cluster_rounded:
        pygame.draw.circle(win, (255, 255, 255), (int(pos[0]), int(pos[1])), r)
    
    pygame.display.update();
    
pygame.quit();
