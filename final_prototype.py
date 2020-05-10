#Calculation of Distance
def distance(pos_1, pos_2):
    return sqrt(sum((pos_1-pos_2)**2));

#Declaration of Basic Parameters
import random;
import numpy as np;
from math import *;
cluster=[]; #population
x_center=250; #Centre x-position
y_center=250; #Centre y-position
n=100; #Size of population
wall_width=150; #Boundary x-position
wall_height=150; #Boundary y-position
r=5; #Size of the characters(in pixels)
cluster=[[x_center+random.randrange(-100, 100), y_center+random.randrange(-100, 100)] for i in range(n)]; #population initiation

#Money Options
money=100; #Initial money
lockdown=0; #If lockdown is carried out

#Calculation of Positions
x_vel=50; #x-velocity
y_vel=50; #y-velocity
dt=1/20; #Time interval

x_acc=10; #x-accleration
y_acc=10; #y-accleration

#Infection Parameters
r_infection=23; #Infection radius (proxy for R0)
infection_p=0.1; #getting infected (proxy for R0)
incubation=30; #Incubation period in frames
death_p=0.001; #Death Probability
death_count=0;
recover_p=0.1;
recover_time_min=1000;

#Intiation of Velocity and position Array
vel=[[random.uniform(-x_vel, x_vel), random.uniform(-y_vel, y_vel)] for i in range(n)]; 
cluster=np.array(cluster);
vel=np.array(vel);

#Transmission Mechanism
infected=[0 for i in range(n)];
first_infection=random.randrange(0,n);
infected[first_infection]=1;
quarantine=[0 for i in range(n)];
quarantine_duration=5; #quarantine for AT LEAST this duration, released only after recovery
active=[1 for i in range(n)];
dead=[0 for i in range(n)];
infected_known_count=0;
infected_total=1;
death_count=0;
quarantine_count=0;

#PyGame Initiation
import pygame
import pygame_gui
pygame.init()

win = pygame.display.set_mode((500,500)); #Background surface size
clock = pygame.time.Clock();
manager = pygame_gui.UIManager((500,500));

background = pygame.Surface((500, 500));
background.fill(pygame.Color('#292a30')); #Colour of background

#Buttons
but_iso = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 450), (100, 25)),text='Testing',manager=manager); #Testing

but_qua = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 450), (100, 25)),text='Quarantine',manager=manager); #Quarantine

but_cb = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((360, 450), (100, 25)),text='Lockdown',manager=manager); #Lockdown

but_title = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((75, 25), (250, 25)),text='COVID-19 Response Simulation',manager=manager); #Title

#clicked
selected=np.array([]);
selected=selected.astype(int);
remove_selected=0;

run=True;

while run:
    #Basic settings
    win.fill((41,42,48));
    pygame.time.delay(int(dt*1000));
    time_delta = clock.tick(1/dt)/1000.0;
    
    #Updating active/dead/selected/quarantine etc. statuses of characters
    for i in range(n):
        if quarantine[i]>0:
            quarantine[i]+=1;
        if infected[i]>0:
            infected[i]+=1;
            if random.uniform(0,1)<death_p:
                active[i]=0;
                dead[i]=1;
                infected[i]=0;
                selected=selected[selected!=i];
                death_count+=1;
                infected[i]=0;
                if quarantine[i]:
                    quarantine[i]=0;
                    quarantine_count-=1;
            elif infected[i]>recover_time_min and random.uniform(0,1)<recover_p:
                infected[i]=0;
        elif quarantine[i]>quarantine_duration:
            active[i]=1;
            quarantine[i]=0;
            quarantine_count-=1;
            cluster[i]=[x_center, y_center];
    
    #Buttons Actions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False;

        manager.process_events(event)
        
        #Get mouse position
        click = pygame.mouse.get_pressed()
        if click[2]:
            print(pygame.mouse.get_pos())

        if click[0]:
            click_pos = pygame.mouse.get_pos();
            if 65<=click_pos[0]<=430 and 65<=click_pos[1]<=430:
                distance_list = [distance(i, click_pos) for i in cluster];
                ind=distance_list.index(min(distance_list));
                if ind in selected:
                    selected=selected[selected!=ind];
                else:
                    selected=np.append(selected, ind); #Select specific individuals
                    selected=np.unique(selected);
            
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == but_iso: #Mass Testing
                    if money > 500:
                        print('Tested!');
                        money -= 500;
                        for i in range(n):
                            pos=cluster[i];
                            if infected[i]:
                                infected[i]+=incubation;
                                pygame.draw.circle(win, (246, 116, 94), (int(pos[0]), int(pos[1])), 10,2);
                    else:
                        print('Not enough money!!!')
        
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == but_qua: #Quarantine
                    selected_length=len(selected);
                    if money > selected_length*100:
                        print('Quarantined!');
                        for i in selected:
                            active[i]=0;
                            quarantine[i]+=1;
                            quarantine_count+=1;
                        selected=np.array([]);
                        selected=selected.astype(int);
                    else:
                        print('Not enough money!!!')
        
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == but_cb: #Lockdown
                    if money >= 5000:
                        print('Lockdown Started!');
                        money -= 5000;
                        vel=[[0,0] for i in range(n)];
                        lockdown = 1; #Lockdown: loss of income
                    else:
                        print('Not enough money!!!')
                        
    
    
    [x_pos, y_pos]=np.transpose(cluster);
    sorted_x_indices=np.argsort(x_pos);
    x_sorted=x_pos[sorted_x_indices];
    indices_reference=np.array([0 for i in range(n)]);
    for i in range(n):
        index=sorted_x_indices[i];
        indices_reference[index]=i;
        
    new_infected=infected[:];
    for i in range(n):
        if infected[i] and active[i]:
            index=indices_reference[i];
            index_right=index+1;
            index_left=index-1;
            while index_right<n and abs(x_sorted[index_right]-x_sorted[i])<r_infection:
                j=sorted_x_indices[index_right];
                if distance(cluster[i], cluster[j])<r_infection and infected[j]==0 and active[j]:
                    if random.uniform(0,1)<infection_p:
                        new_infected[j]=1;
                        infected_total+=1;
                index_right+=1;
            while index_left>=0 and abs(x_sorted[index_left]-x_sorted[i])<r_infection:
                j=sorted_x_indices[index_left];
                if distance(cluster[i], cluster[j])<r_infection and infected[j]==0 and active[j]:
                    if random.uniform(0,1)<infection_p:
                        new_infected[j]=1;
                        infected_total+=1;
                index_left-=1;
    infected=new_infected[:];
    
    #Draw cluster    
    for i in range(n):
        pos=cluster[i];
        if active[i]:
            if infected[i]>incubation:
                pygame.draw.circle(win, (246, 116, 94), (int(pos[0]), int(pos[1])), r);
            else:
                pygame.draw.circle(win, (180, 209, 164), (int(pos[0]), int(pos[1])), r);
    
    for i in selected:
        target=cluster[i];
        pygame.draw.rect(win, (28,196,227), (target[0] - 20/2,target[1]-20/2, 20, 20), 3);
        
    pygame.draw.rect(win,(200,200,200),(wall_width/2-10,wall_width/2-10,520-wall_width,520-wall_width),3);
    
    
    #Draw additional buttons
    element_list = [];
    infected_known_count=len([i for i in infected if i>incubation])
    but_qua_text = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((440-222, 440-39), (219, 35)), text= 'Quarantined:' +str(quarantine_count), manager = manager);
    element_list.append(but_qua_text);
    but_death_text = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((65, 440-39), (159, 35)), text = 'Dead:' + str(death_count), manager = manager);
    element_list.append(but_death_text);
    but_infected = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((437, 128), (62, 35)), text = '  : '+str(infected_known_count), manager = manager);
    element_list.append(but_infected);
    but_money = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 25), (80, 25)),text='$'+str(money),manager=manager);
    element_list.append(but_money);
    
    manager.update(time_delta);
    manager.draw_ui(win);

    pygame.draw.circle(win, (246, 116, 94), (450, 146), r);

    #Update window
    pygame.display.update();
    
    #Kill buttons
    for i in element_list:
        i.kill();
    
    #Updating the money
    money += 5*int(not(lockdown)); #Income per frame
    
    #Random Motion of Characters
    acc=[[random.uniform(-x_acc, x_acc), random.uniform(-y_acc, y_acc)] for i in range(n)];
    acc=np.array(acc);
    vel=np.add(vel, acc*dt);
    cluster=np.add(cluster, vel*dt);
    for i in range(n):
        [x_pos, y_pos]=cluster[i];
        if active[i]==0:
            cluster[i]=[0, 0];
        elif x_pos<x_center-wall_width or x_pos>x_center+wall_width:
            vel[i,0]*=-1;
        elif y_pos<y_center-wall_height or y_pos>y_center+wall_height:
            vel[i,1]*=-1; 
    cluster_rounded=np.rint(cluster);

pygame.quit()
