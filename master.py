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

money=10000;
a=1;

x_vel=50;
y_vel=50;
dt=0.1;

x_acc=10;
y_acc=10;

x_bias=10;
y_bias=10;

r_infection=10;

incubation=70;

vel=[[random.uniform(-x_vel, x_vel), random.uniform(-y_vel, y_vel)] for i in range(n)];
cluster=np.array(cluster);
vel=np.array(vel);

infected=[0 for i in range(n)];
first_infection=random.randrange(0,n);
infected[first_infection]=1;

time_count=[0 for i in range(n)];
min_infection_time=5;
p=0.8;#not getting infected

import pygame
import pygame_gui
pygame.init()

win = pygame.display.set_mode((500,500));
clock = pygame.time.Clock();
manager = pygame_gui.UIManager((500,500));

background = pygame.Surface((500, 500));
background.fill(pygame.Color('#292a30'));


#BUTTONS
but_iso = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 450), (100, 25)),text='Testing',manager=manager);

but_qua = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 450), (100, 25)),text='Quarantine',manager=manager);

but_cb = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((360, 450), (100, 25)),text='Lockdown',manager=manager);

but_title = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((75, 25), (250, 25)),text='COVID-19 Response Simulation',manager=manager);

#clicked
clicked = -1
#RUN GAME
run=True;
while run:
    win.fill((41,42,48));
    pygame.time.delay(int(dt*1000));
    time_delta = clock.tick(60)/1000.0;
    
    acc=[[random.uniform(-x_acc, x_acc), random.uniform(-y_acc, y_acc)] for i in range(n)];
    acc=np.array(acc);
    
    
    [x_pos, y_pos]=np.transpose(cluster);
    sorted_x_indices=np.argsort(x_pos);
    x_sorted=x_pos[sorted_x_indices];
    indices_reference=np.array([0 for i in range(n)]);
    for i in range(n):
        index=sorted_x_indices[i];
        indices_reference[index]=i;
    
    time_count_new=[time for time in time_count];
    for i in range(n):
        if infected[i]:
            index=indices_reference[i];
            index_right=index+1;
            index_left=index-1;
            while index_right<n and abs(x_sorted[index_right]-x_sorted[i])<r_infection:
                j=sorted_x_indices[index_right];
                if distance(cluster[i], cluster[j])<r_infection and infected[j]==0:
                    time_count_new[j]+=1;
                index_right+=1;
            while index_left>=0 and abs(x_sorted[index_left]-x_sorted[i])<r_infection:
                j=sorted_x_indices[index_left];
                if distance(cluster[i], cluster[j])<r_infection and infected[j]==0:
                    time_count_new[j]+=1;
                index_left-=1;
                
    for i in range(n):
        if infected[i]>0:
            infected[i]+=1;
        if time_count_new[i]==time_count[i]:
            time_count_new[i]=0;
        elif time_count_new[i]>0:
            p_infection=1-p**(time_count_new[i]);
            if random.uniform(0,1)<p_infection:
                infected[i]=1;
                time_count_new[i]=0;
    time_count=[time for time in time_count_new];
    
                
    
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

        manager.process_events(event)

        click = pygame.mouse.get_pressed()
        if click[2]== 1:
            print(pygame.mouse.get_pos())

        if click[0]== 1:
            click_pos = pygame.mouse.get_pos()
            distance_list = [distance(i, click_pos) for i in cluster]
            if min(distance_list) < 30:
                clicked = distance_list.index(min(distance_list))
            
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == but_iso:
                    print('Tested!');
                    money -= 10;
                    for i in range(n):
                           pos=cluster[i];
                           if infected[i]:
                               pygame.draw.circle(win, (246, 116, 94), (int(pos[0]), int(pos[1])), 10,3);
                               infected[i]+=incubation;
        
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == but_qua:
                    print('Quarantined!');
                    money -= 100;
        
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == but_cb:
                    if money >= 5000:
                        print('Lockdown Started!');
                        money -= 5000;
                        vel=[[0,0] for i in range(n)];
                        a = 0;
                    else:
                        print('Not enough money!!!')


    manager.update(time_delta)
    manager.draw_ui(win)

    for i in range(n):
        pos=cluster[i];
        if infected[i]>incubation:
            pygame.draw.circle(win, (246, 116, 94), (int(pos[0]), int(pos[1])), r);
        else:
            pygame.draw.circle(win, (180, 209, 164), (int(pos[0]), int(pos[1])), r);
    pygame.draw.rect(win,(200,200,200),(wall_width/2-10,wall_width/2-10,520-wall_width,520-wall_width),3);

    if clicked >= 0:
        clicked_target = cluster[clicked]
        pygame.draw.rect(win, (217,237,255), (clicked_target[0] - 20/2,clicked_target[1]-20/2, 20, 20), 2)

    but_money = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 25), (80, 25)),text='$'+str(money),manager=manager);
    
    pygame.display.update();
    money += 2*a;
pygame.quit();

