import pygame;
import pygame_gui;

pygame.init();

res = (500,500);
pygame.display.set_caption('GUI Test');
win = pygame.display.set_mode(res);
manager = pygame_gui.UIManager((500,500))

#background
background = pygame.Surface((500, 500))
background.fill(pygame.Color('#292a30'))

#Start screen
centralised_anchor = {'left': 'left','right': 'right','top': 'top','bottom': 'bottom'}
start_button_layout = pygame.Rect(200, 225, 100, 50)    
start_button = pygame_gui.elements.UIButton(relative_rect = start_button_layout,
                                            text = 'Start Game', manager = manager,
                                            anchors = centralised_anchor)


#buttons
'''test_subject = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((131, 144), (20, 20)),
                                            text = '',
                                            manager=manager)

test_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((421, 77),(120,40)),
                                            text = 'Test',
                                            manager=manager)
'''

clock = pygame.time.Clock()
run = True;

while run:
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    print('Started')
        manager.process_events(event)

        right_click = pygame.mouse.get_pressed()[2]
        if right_click == 1:
            print(pygame.mouse.get_pos())

    manager.update(time_delta)


    win.blit(background, (0,0))
    manager.draw_ui(win)

    #pygame.draw.rect(win, (255,255,255), ((52,39), (300,300)), 2)
    
    


    pygame.display.update()