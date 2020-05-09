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
n_init=n #Initial size of population
wall_width=150; #Boundary x-position
wall_height=150; #Boundary y-position
r=5; #Size of the dots
x_vel=[0 for i in range(n)]; #x-velocity initiation
y_vel=[0 for i in range(n)]; #y-velocity initiation
cluster=[[x_center+random.randrange(-100, 100), y_center+random.randrange(-100, 100)] for i in range(n)]; #population initiation
t = 0


#Money Options
money=100; #Initial money
a=1; #If lockdown is carried out

#Calculation of Positions
x_vel=50; #x-velocity
y_vel=50; #y-velocity
dt=0.1; #Time interval

x_acc=10; #x-accleration
y_acc=10; #y-accleration

#Infection Parameters
r_infection=30; #Infection radius (proxy for R0)
p=0.85; #not getting infected (proxy for R0)
incubation=0; #Incubation period in frames
death_p=0.005; #Death Probability
death_count=0;
recover_p=0.1;
recover_time_min=50;

#Intiation of Velocity Array
vel=[[random.uniform(-x_vel, x_vel), random.uniform(-y_vel, y_vel)] for i in range(n)]; 
cluster=np.array(cluster);
vel=np.array(vel);

#Transmission Mechanism
infected=[0 for i in range(n)];
first_infection=random.randrange(0,n);
infected[first_infection]=1;
time_count=[0 for i in range(n)];
min_infection_time=5;
quarantine=[];

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

##Main loop of game
run=True;
while run:
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
                selected=np.append(selected, distance_list.index(min(distance_list))); #Select specific individuals
            
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == but_iso: #Mass Testing
                    if money > 500:
                        print('Tested!');
                        money -= 500;
                        for i in range(n):
                            pos=cluster[i];
                            if infected[i]:
                                target=cluster[i];
                                infected[i]+=incubation;
                    else:
                        print('Not enough money!!!')
        
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == but_qua: #Quarantine
                    selected=np.unique(selected);
                    selected_length=len(selected);
                    if money > selected_length*100:
                        print('Quarantined!');
                        remove_selected=1;
                        cluster=np.delete(cluster, selected, axis=0);
                        infected=np.delete(infected, selected, axis=0);
                        time_count=np.delete(time_count, selected, axis=0);
                        vel=np.delete(vel, selected, axis=0);
                        money -= 100*selected_length;
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
                        a = 0; #Lockdown: loss of income
                    else:
                        print('Not enough money!!!')
                        
    n=len(cluster);
                        
    #Basic settings
    win.fill((41,42,48));
    pygame.time.delay(int(dt*1000));
    time_delta = clock.tick(60)/1000.0;
    
    #Randomising Positions and Infection
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
                
    die=[];
    shift_arr=[0 for i in range(len(selected))];
    for i in range(n):
        if infected[i]>0:
            infected[i]+=1;
            if random.uniform(0,1)<death_p:
                die.append(i);
                death_count+=1;
                for j in range(len(selected)):
                    if selected[j]==i:
                        shift_arr[j]=-1;
                    elif selected[j]>i:
                        shift_arr[j]+=1;
            elif infected[i]>recover_time_min and random.uniform(0,1)<recover_p:
                infected[i]=0;
        if time_count_new[i]==time_count[i]:
            time_count_new[i]=0;
        elif time_count_new[i]>0:
            p_infection=1-p**(time_count_new[i]);
            if random.uniform(0,1)<p_infection:
                infected[i]=1;
                time_count_new[i]=0;
    time_count=[time for time in time_count_new];
    
    vel=np.add(vel, acc*dt);
    
    #Boundary of the Game
    for i in range(n):
        [x_pos, y_pos]=cluster[i];
        if x_pos<x_center-wall_width or x_pos>x_center+wall_width:
            vel[i,0]*=-1;
        if y_pos<y_center-wall_height or y_pos>y_center+wall_height:
            vel[i,1]*=-1;
        
    cluster=np.add(cluster, vel*dt);
    cluster_rounded=np.rint(cluster);

    #Draw
    manager.update(time_delta)
    win.blit(background, (0,0))
    
    #Additional_buttons
    element_list = []
    infected_no = len([i for i in infected if i > incubation])

    but_qua = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((440-222, 440-39), (219, 35)), text= 'Quarantined:' + str(69), manager = manager)
    element_list.append(but_qua)
    but_death = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((65, 440-39), (159, 35)), text = 'Dead:' + str(n_init-n), manager = manager)
    element_list.append(but_death)

    but_infected = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((437, 128), (62, 35)), text = '  : '+str(infected_no), manager = manager)
    element_list.append(but_infected)
    but_healthy = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((437, 168), (62, 35)), text = '  : '+str(n-infected_no), manager = manager)
    element_list.append(but_healthy)

    #Updating the money
    but_money = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 25), (80, 25)),text='$'+str(money),manager=manager);
    element_list.append(but_money)

    manager.draw_ui(win)

    #draw people
    for i in range(n):
        pos=cluster[i];
        if infected[i]>incubation:
            pygame.draw.circle(win, (246, 116, 94), (int(pos[0]), int(pos[1])), r);
        else:
            pygame.draw.circle(win, (180, 209, 164), (int(pos[0]), int(pos[1])), r);
    pygame.draw.rect(win,(200,200,200),(wall_width/2-10,wall_width/2-10,520-wall_width,520-wall_width),3);

    for i in selected:
        target=cluster[i];
        pygame.draw.rect(win, (28,196,227), (target[0] - 20/2,target[1]-20/2, 20, 20), 3)
        
    #draw textbox dot
    pygame.draw.circle(win, (246, 116, 94), (450, 146), r)
    pygame.draw.circle(win, (180, 209, 164), (450, 186), r)

    
    
    
    
    selected_new=np.array([]);
    for i in range(len(selected)):
        if shift_arr[i]!=-1:
            selected_new=np.append(selected_new, selected[i]-shift_arr[i]);
            
    selected=np.unique(selected_new);
    selected=selected.astype(int);
    
    cluster=np.delete(cluster, die, axis=0);
    vel=np.delete(vel, die, axis=0);
    time_count=np.delete(time_count, die, axis=0);
    infected=np.delete(infected, die, axis=0);
    n=len(cluster);


    
    pygame.display.update();

    #kill elements
    for i in element_list:
        i.kill()


    t = t + 1
    money += 10*a; #Income per frame
pygame.quit();
