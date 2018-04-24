import pygame
import time

from random import *
from math import *

pygame.init()

# SIZE OF SCREEN
WIDTH = 550
HIGHT = 600

# Color all
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (200, 200, 0)
COLOR_GREEN = (34, 177, 76)
COLOR_BLUE = (0, 0, 255)
COLOR_BLUE_STRONG = (65, 58, 139)
COLOR_GREY = (91, 91, 91)
COLOR_BROWN = (147, 83, 0)
COLOR_GREEN_STRONG = (0, 137, 26)

# SETTING IMAGE
IMG_BG = pygame.image.load('img/bg.png')
IMG_NAME_GAME = pygame.image.load('img/namegame.png')
IMG_ICON = pygame.image.load('img/icon.png')

IMG_PLY = pygame.image.load('img/player_live.png')
IMG_CRASH = pygame.image.load('img/player_crash.png')
IMG_DROWNED = pygame.image.load('img/player_drowned.png')

IMG_GST = [pygame.image.load('img/ghost' + str(i+1) + '.png') for i in range(3)]
IMG_RAFT = [pygame.image.load('img/raft'+str(i+1)+'.png') for i in range(2)]
IMG_STRL = pygame.image.load('img/stroller.png')

IMG_GRAVE = pygame.image.load('img/grave.png')
IMG_COIN = pygame.image.load('img/coin.png')

IMG_SB = pygame.image.load('img/small_bound.png')
IMG_MENU = pygame.image.load('img/menu.png')

# SETTING GAME DISPLAY
SIZE_SCREEN = (WIDTH, HIGHT)
gameDisplay = pygame.display.set_mode(SIZE_SCREEN)
pygame.display.set_caption("CROSSINHG")
pygame.display.set_icon(IMG_ICON)

# SET CLOCK
clock_time = pygame.time.Clock()

# SET FPS
FPS = 2

# SET FONT
small_font = pygame.font.SysFont("consolas", 20)
med_font = pygame.font.SysFont("consolas", 50)
large_font = pygame.font.SysFont("consolas", 80)

# MAIN VALUE OF GAME
GAME_OVER = False
BAND_KEYBOUND = False
PLAY_STRL = False

best_score = -1
best_level =  0


def show_best_score(score, level):
    global best_score
    global best_level

    if score > best_score :
        best_score = score
        best_level = level

    push_img(IMG_SB, 80, 230)

    message_to_screen('YOU GOT '+str(score)+' SCORE, LEVEL : '+str(level), COLOR_BROWN, -15)
    message_to_screen('BEST SCORE is '+str(best_score)+', LEVEL : '+str(best_level), COLOR_BLUE_STRONG, 20)

    message_to_screen("Pass SPACE_BAR for revive", COLOR_GREEN_STRONG, 60)

def game_exit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()

def draw_gird():
    h = [70, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 35]
    len_h = len(h)
    for i in range(1, len_h):
        h[i] += h[i-1]

    w = [25, 46, 46, 45, 45, 45, 45, 45, 45, 45, 46, 46, 25]
    len_w = len(w)
    for i in range(1, len_w):
        w[i] += w[i-1]

    for i in range(len_h):
        pygame.draw.line(gameDisplay, COLOR_WHITE, (0, h[i]), (WIDTH, h[i]), 2);

    for i in range(len_w):
        pygame.draw.line(gameDisplay, COLOR_WHITE, (w[i], 0), (w[i], HIGHT), 2);

def grave_show(grave_list):
    n = len(grave_list)
    for i in range(n):
        x = grave_list[i][0]
        y = grave_list[i][1]
        push_img(IMG_GRAVE, x, y)
        # if i > 0: # show coin all
        #     push_img(IMG_COIN, (x + grave_list[i-1][0])//2, y)

def draw_bound(color = COLOR_WHITE, size_line = 2):
    draw_line(25, 70, 525, 70, color, size_line)
    draw_line(525, 70, 525, 565, color, size_line)
    draw_line(25, 565, 525, 565, color, size_line)
    draw_line(25, 70, 25, 565, color, size_line)

def update_screen():
    # update portion of all screen
    pygame.display.update()

def draw_line(x1, y1, x2, y2, color = COLOR_WHITE, size_line = 2):
    # Draw Line
    pygame.draw.line(gameDisplay, color, (x1, y1), (x2, y2), size_line)

def draw_rect(pos_x, pos_y, widht_rect, height_rect, color = COLOR_WHITE, stoke = 0):
    # Draw Rectangle
    pygame.draw.rect(gameDisplay, color, [pos_x, pos_y, widht_rect, height_rect], stoke)

def draw_circle(x, y, redius, color = COLOR_WHITE) :
    # draw Circle
    pygame.draw.circle(gameDisplay, color, (x, y), int(redius))

def push_img(img, x, y):
    # push image to screen in position (x, y)
    gameDisplay.blit(img, (x, y))

def fill_scr(color):
    # fill color on the screen of windows
    gameDisplay.fill(color)

def player(x, y, state = 'live'):
    global GAME_OVER
    add_img = None

    if state == 'live':
        add_img = IMG_PLY
    elif state == 'drowned':
        add_img = IMG_DROWNED
        # GAME_OVER = True
    elif state == 'crash':
        add_img = IMG_CRASH
        # GAME_OVER = True

    if add_img == None:
        draw_rect(x, y, 20, 35, COLOR_BLUE)
    else:
        push_img(add_img, x, y)

def player_die(history_ply):
    n = len(history_ply)
    for i in range(n):
        x = history_ply[i][0]
        y = history_ply[i][1]
        state = history_ply[i][2]

        add_img = None

        if state == 'live':
            add_img = IMG_PLY
        elif state == 'drowned':
            add_img = IMG_DROWNED
            # GAME_OVER = True
        elif state == 'crash':
            add_img = IMG_CRASH
            # GAME_OVER = True

        if add_img == None:
            draw_rect(x, y, 20, 35, COLOR_BLUE)
        else:
            push_img(add_img, x, y)

def traffic_LTR(ghosts) :
    # tranffic in form : Left to Right
    n = len(ghosts)
    remove_ghost = set()
    for i in range(n):
        ghost = ghosts[i]
        ghost_x = ghost[0]
        ghost_y = ghost[1]
        ghost_type = ghost[2]
        # draw_rect(ghost_x, ghost_y, 40, 20, COLOR_RED)
        
        speed_ghost = 10
        if ghost_type == 1:
            speed_ghost = randint(1, 3)
        elif ghost_type == 2:
            speed_ghost = randint(4, 6)
        elif ghost_type == 3:
            speed_ghost = randint(7, 9)

        push_img(IMG_GST[ghost_type-1], ghost_x, ghost_y)
        ghosts[i][0] += speed_ghost      # CHANGE SPEED OF ghosts[i]
        if ghost_x >= WIDTH :
            remove_ghost.add(i)
    
    ghost_live = []
    for i in range(n):
        if i not in remove_ghost:
            ghost_live.append(ghosts[i])

    ghosts.clear()
    ghosts.extend(ghost_live)

def traffic_RTL(ghosts) :
    # tranffic in form : Right to Left 
    n = len(ghosts)
    remove_ghost = set()
    for i in range(n):
        ghost = ghosts[i]
        ghost_x = ghost[0]
        ghost_y = ghost[1]
        ghost_type = ghost[2]
        # draw_rect(ghost_x, ghost_y, 40, 20, COLOR_RED)
        speed_ghost = 10
        if ghost_type == 1:
            speed_ghost = randint(1, 2)
        elif ghost_type == 2:
            speed_ghost = randint(3, 4)
        elif ghost_type == 3:
            speed_ghost = randint(5, 7)

        flip_horizon = pygame.transform.flip(IMG_GST[ghost_type-1], True, False) 
        
        push_img(flip_horizon, ghost_x, ghost_y)
        ghosts[i][0] -= speed_ghost      # CHANGE SPEED OF ghosts[i]
        if ghost_x < 0 :
            remove_ghost.add(i)
    
    ghost_live = []
    for i in range(n):
        if i not in remove_ghost:
            ghost_live.append(ghosts[i])

    ghosts.clear()
    ghosts.extend(ghost_live)

def overlab(img, x_img, y_img, obj, type_obj = 'rect') :
    img_x = x_img
    img_y = y_img
    img_width = img.get_width()
    img_hieght = img.get_height()
    obj_x = obj[0]
    obj_y = obj[1]
    if type_obj == 'rect' :    
        obj_width = obj[2]
        obj_hieght = obj[3]
        x_overlab = (img_x <= obj_x + obj_width and img_x + img_width >= obj_x)
        y_overlab = (img_y <= obj_y + obj_hieght and img_y + img_hieght >= obj_y)
        return x_overlab and y_overlab
    elif type_obj == 'circle':
        obj_r = 15
        img_x_list = [img_x]
        img_y_list = [img_y]
        for i in range(1):
            dx = img_x_list[i] - obj_x
            dy = img_y_list[i] - obj_y
            r  = obj_r + 10
            # print(sqrt(dx*dx + dy*dy), r)
            if dx*dx + dy*dy <= r*r:
                return True
        return False
    return False

def show_score(point):
    text = small_font.render("SCORE:"+str(point), True, COLOR_WHITE)
    push_img(text, 25, 52)

def show_level(level):
    text = small_font.render("LEVEL:"+str(level), True, COLOR_WHITE)
    text_width = text.get_width()
    push_img(text, WIDTH-25-text_width, 52)

def text_objects(text, color, size) :
    if size == "small":
        textSuf = small_font.render(text, True, color)
    elif size == "medium":
        textSuf = med_font.render(text, True, color)
    elif size == "large":
        textSuf = large_font.render(text, True, color)

    return textSuf, textSuf.get_rect()

def message_to_screen(msg, color, y_displace = 0, size = "small"):
    textSuf, text_rect = text_objects(msg, color, size)
    text_rect.center = (WIDTH / 2), (HIGHT / 2) + y_displace
    push_img(textSuf, text_rect.x, text_rect.y)

def create_runway(hieght_of_runway, type_of_runway = None, n_ghost = 1) :
    ghosts_runway = list()
    type_ghost = randint(1, 3)

    if type_of_runway == 'left_to_rigth':
        start_x_ghost = randint(-20, -10)    
        ghosts_runway.append([start_x_ghost, hieght_of_runway, type_ghost])

        for i in range(1, n_ghost):
            speed_ghost = randint(1, ghosts_runway[i-1][2])
            ghosts_runway.append([start_x_ghost, hieght_of_runway, type_ghost])

    elif type_of_runway == 'right_to_left':
        start_x_ghost = randint(WIDTH, WIDTH + 10)
        ghosts_runway.append([start_x_ghost, hieght_of_runway, type_ghost])

        for i in range(1, n_ghost):
            start_x_ghost = ghosts_runway[i-1][0] + 50
            ghosts_runway.append([start_x_ghost, hieght_of_runway, type_ghost])

    return ghosts_runway

def create_waterway(hieght_of_runway, type_of_runway,  type_raft, raft_current = list() ,n_raft = 1):
    raft_waterway = list()
    if type_raft == 1:
        width_raft = IMG_RAFT[0].get_width()
    else:
        width_raft = IMG_RAFT[1].get_width()

    if type_of_runway == 'left_to_rigth':
        min_x = WIDTH + 100000
        for mem in raft_current:
            min_x = min(min_x, mem[0])

        if min_x > 0:
            min_x = 0

        start_x_raft = randint(min_x-5*width_raft, min_x-width_raft)

        raft_waterway.append([start_x_raft, hieght_of_runway, type_raft])

        for i in range(1, n_raft):
            start_x_raft = raft_waterway[i-1][0] - width_raft
            raft_waterway.append([start_x_raft-5, hieght_of_runway, type_raft])

    else: #elif type_of_runway == 'right_to_left':
        max_x = -WIDTH - 100000
        for mem in raft_current:
            max_x = max(max_x, mem[0])

        if max_x <= WIDTH:
            max_x = WIDTH

        start_x_raft = randint(max_x+width_raft, max_x+5*width_raft)

        raft_waterway.append([start_x_raft, hieght_of_runway, type_raft])

        for i in range(1, n_raft):
            start_x_raft = raft_waterway[i-1][0] + width_raft
            raft_waterway.append([start_x_raft+5, hieght_of_runway, type_raft])

    return raft_waterway

def waterway_LTR(rafts):
    # waterway in form : Left to Right
    n = len(rafts)
    remove_raft = set()
    for i in range(n):
        raft = rafts[i][0]
        raft_x = rafts[i][0]
        raft_y = rafts[i][1]
        raft_type = rafts[i][2]
        # draw_rect(ghost_x, ghost_y, 40, 20, COLOR_RED)
        
        if raft_type == 1:
            speed_raft = 2
        elif raft_type == 2:
            speed_raft = 3

        push_img(IMG_RAFT[raft_type-1], raft_x, raft_y)
        rafts[i][0] += speed_raft      # CHANGE SPEED OF ghosts[i]
        if raft_x >= WIDTH :
            remove_raft.add(i)
    
    raft_live = []
    for i in range(n):
        if i not in remove_raft:
            raft_live.append(rafts[i])
    rafts.clear()
    rafts.extend(raft_live)

def waterway_RTL(rafts):
    # waterway in form : Left to Right
    n = len(rafts)
    remove_raft = set()
    for i in range(n):
        raft = rafts[i][0]
        raft_x = rafts[i][0]
        raft_y = rafts[i][1]
        raft_type = rafts[i][2]
        # draw_rect(ghost_x, ghost_y, 40, 20, COLOR_RED)
        
        if raft_type == 1:
            speed_raft = -2
        elif raft_type == 2:
            speed_raft = -3

        push_img(IMG_RAFT[raft_type-1], raft_x, raft_y)
        rafts[i][0] += speed_raft      # CHANGE SPEED OF ghosts[i]
        if raft_x <= 0:
            remove_raft.add(i)
    
    raft_live = []
    for i in range(n):
        if i not in remove_raft:
            raft_live.append(rafts[i])
    rafts.clear()
    rafts.extend(raft_live)

def coin_show(coin):
    n = len(coin)
    for i in range(n):
        x = coin[0]
        y = coin[1]
        push_img(IMG_COIN, x, y)

def how_to_play():
    
    while True:
        events = pygame.event.get()
        for ent in events:
            game_exit(ent)

            if ent.type == pygame.KEYDOWN:
                if ent.key == pygame.K_b:
                    return

                if ent.key == pygame.K_q:
                    pygame.quit()
                    quit()

        fill_scr(COLOR_BLACK)

        SHIF = 50

        message_to_screen("HOW TO PLAY", COLOR_WHITE, -200 + SHIF, 'medium')

        message_to_screen('pass a or arrow left  : move left ', COLOR_WHITE,-120+ SHIF)
        message_to_screen('pass d or arrow right : move right', COLOR_WHITE,-100+ SHIF)
        message_to_screen('pass s or arrow down  : move down ', COLOR_WHITE,-80+ SHIF)
        message_to_screen('pass w or arrow up    : move up   ', COLOR_WHITE,-60+ SHIF)

        message_to_screen('pass c : clear body', COLOR_WHITE, 0+ SHIF)
        message_to_screen('pass p : pause game', COLOR_WHITE, 20+ SHIF)
        message_to_screen('pass q : quit game ', COLOR_WHITE, 40+ SHIF)


        message_to_screen('pass b to back', COLOR_WHITE,100+ SHIF)

        message_to_screen('Don\'t be Crashed, Don\'t be drowned!!', COLOR_RED, 200)

        update_screen()
        clock_time.tick(FPS)

def ready_start():
    count_down = 3
    time_count = 0
    limit_time = FPS
    while count_down > 0:
        events = pygame.event.get()
        for ent in events:
            game_exit(ent)
            if ent.type == pygame.KEYDOWN:
                if ent.key == pygame.K_q:
                    return True       # Select Exit Game == True

        fill_scr(COLOR_BLACK)
        
        push_img(IMG_BG, 25, 70)                  # DRAW BACKGROUND STAGE
        message_to_screen(str(count_down), COLOR_WHITE, 0, 'large')

        draw_bound(COLOR_GREY, 4)                 # DRAW BOUND OF STAGE

        push_img(IMG_NAME_GAME, 175, 10)          # PUSH name of GAME to Screen

        show_score(0)                         # SHOW score ps. it is foctor of level game
        show_level(0)                         # SHOW level status

        message_to_screen("DEMO", COLOR_GREEN, 285) # tag DEMO for this game
        
        time_count += 1
        if time_count >= limit_time:
            time_count = 0
            count_down -= 1

        update_screen()
        clock_time.tick(FPS)
    return False  # Select to backing home is False

def pause_game():
    while True:
        events = pygame.event.get()
        for ent in events:
            game_exit(ent)

            if ent.type == pygame.KEYDOWN:
                if ent.key == pygame.K_SPACE:
                    return

        message_to_screen("PAUSE", COLOR_WHITE, -20, 'medium')
        message_to_screen('Pass SPACE to continue', COLOR_WHITE, 20)

        update_screen()
        clock_time.tick(FPS)

def play_sound(sound_input_for_play):
    # Play SOUND function
    pygame.mixer.Sound.play(sound_input_for_play)

def play_music(muisc_input_for_play):
    # Play background Sound
    pygame.mixer.music.play(muisc_input_for_play)

def game_loop():
    global GAME_OVER
    global BAND_KEYBOUND
    global FPS
    global PLAY_STRL


    GAME_INTRO = True
    while (GAME_INTRO) :
        events = pygame.event.get()
        for ent in events:
            game_exit(ent)

            if ent.type == pygame.KEYDOWN:
                if ent.key == pygame.K_c:
                    GAME_INTRO = False

                if ent.key == pygame.K_h:
                    how_to_play()

                if ent.key == pygame.K_q:
                    pygame.quit()
                    quit()


        fill_scr(COLOR_BLACK)
        width_img = IMG_MENU.get_width()
        gameDisplay.blit(IMG_MENU, (WIDTH//2-width_img//2, 100))

        message_to_screen("Pass C to Play the Game!", COLOR_WHITE, 50)
        message_to_screen("Pass H to See How to Play", COLOR_WHITE, 85)
        message_to_screen("Pass Q to Exit", COLOR_WHITE, 180)

        update_screen()
        clock_time.tick(FPS)

    ################################################################
    ################################################################
    ################################################################

    level = 1

    LEFT_BOUND = 30
    N_STEP_X = 15
    STEP_X = 35
    RIGHT_BOUND = LEFT_BOUND + (N_STEP_X-1) * STEP_X - 20
    cur_x = (LEFT_BOUND + RIGHT_BOUND) // 2
    
    POS_Y = [530, 482, 438, 392, 345, 298, 256, 212, 168, 123, 78]
    nY = len(POS_Y)
    y_id = 0

    # SET GROUND INFO
    GROUND_X = 25
    GROUND_Y = 295
    GROUND_WIDTH = 500
    GROUND_HIEGHT = 270
    GROUND = (GROUND_X, GROUND_Y, GROUND_WIDTH, GROUND_HIEGHT)

    ply_x = cur_x
    ply_y = POS_Y[0]

    #SET ghost INFO
    ghost_runway_LTR = create_runway(POS_Y[1], 'left_to_rigth') + create_runway(POS_Y[3], 'left_to_rigth')
    ghost_runway_RTL = create_runway(POS_Y[2], 'right_to_left') + create_runway(POS_Y[4], 'right_to_left')

    #SET STROLLER INFO
    TIME_PER_APPEAR = FPS * 10
    WIDTH_STRL = IMG_STRL.get_width() 
    HEIGHT_STRL = IMG_STRL.get_height()
    SPEED_STRL = 5
    
    time_stroller = 0
    pos_x_strl = -WIDTH_STRL
    pos_y_strl = POS_Y[5] - 10

    #SET RAFT INFO
    raft_waterway_LTR = create_waterway(POS_Y[7], 'left_to_rigth', 2) + create_waterway(POS_Y[9], 'left_to_rigth', 1)
    raft_waterway_RTL = create_waterway(POS_Y[6], 'right_to_left', 1) + create_waterway(POS_Y[8], 'right_to_left', 2)

    #SET GRAVE INFO
    WIDTH_GRAVE = IMG_GRAVE.get_width()
    HIEGHT_GRAVE = IMG_GRAVE.get_height()
    POS_GRAVE = [(i+1) * WIDTH_GRAVE + (i*60) for i in range(6)]
    N_GRAVE = len(POS_GRAVE)
    grave_list = list()
    for i in range(N_GRAVE):
        grave_list.append((POS_GRAVE[i], 80))

    TOUCH_GRAVE = False

    #SET COIN INFO
    WIDTH_COIN = IMG_COIN.get_width()
    HIEGHT_COIN = IMG_COIN.get_height()
    COIN_SHOW = False
    LIMIT_COIN = 1

    POS_COIN = list()
    set_coin = list()
    for i in range(1, 6):
        POS_COIN.append(((grave_list[i][0] + grave_list[i-1][0])//2, grave_list[i][1]))
        set_coin.append(i-1)

    select_coin = randint(0, 4)

    #SET PLAYER LIST DIE
    ply_die = list()

    #SET SCORE
    score = 0

    back_home = ready_start()
    if back_home == True:
        return True

    while not GAME_OVER:
        # =============== EVENT PROCESSING ===================== #
        events = pygame.event.get()
        for ent in events:
            game_exit(ent)

            if ent.type == pygame.KEYDOWN and not BAND_KEYBOUND:
                key = ent.key
                if key == pygame.K_LEFT or key == pygame.K_a:
                    # x_id -= 1
                    cur_x -= STEP_X

                if key == pygame.K_RIGHT or key == pygame.K_d:
                    # x_id += 1
                    cur_x += STEP_X

                if key == pygame.K_UP or key == pygame.K_w:
                    y_id += 1

                if key == pygame.K_DOWN or key == pygame.K_s:
                    y_id -= 1

                if  key == pygame.K_p:
                    pause_game()

                if ent.key == pygame.K_c:
                    ply_die.clear()

                if ent.key == pygame.K_q:
                    return True

            if BAND_KEYBOUND and ent.type == pygame.KEYDOWN and ent.key == pygame.K_SPACE:
                BAND_KEYBOUND = False
                cur_x = (LEFT_BOUND + RIGHT_BOUND) // 2
                y_id = 0
                state = 'live'
                score = 0
                level = 1
                set_coin.clear()
                for i in range(5):
                    set_coin.append(i)

                select_coin = randint(0, 4)


        # ===================== LOGIC GAME ======================= #
        if not BAND_KEYBOUND and len(ghost_runway_RTL) < randint(1, 4):
            ghost_runway_RTL.extend(create_runway(POS_Y[2*randint(1, 2)], 'right_to_left'))

        if not BAND_KEYBOUND and len(ghost_runway_LTR) < randint(1, 4):
            ghost_runway_LTR.extend(create_runway(POS_Y[2*randint(1, 2)-1], 'left_to_rigth'))

        if not BAND_KEYBOUND and len(raft_waterway_LTR) < randint(20, 50) and randint(0,1):
            chioce_rw = [(7, 2), (9, 1)]
            select = randint(0, 1)
            num_raft = randint(1, 5)
            no_rw = chioce_rw[select][0]
            type_rw = chioce_rw[select][1]
            raft_waterway_LTR.extend(create_waterway(POS_Y[no_rw], 'left_to_rigth', type_rw, raft_waterway_LTR, num_raft))

        if not BAND_KEYBOUND and len(raft_waterway_RTL) < randint(20, 50) and randint(0,1):
            chioce_rw = [(6, 1), (8, 2)]
            select = randint(0, 1)
            num_raft = randint(1, 5)
            no_rw = chioce_rw[select][0]
            type_rw = chioce_rw[select][1]
            raft_waterway_RTL.extend(create_waterway(POS_Y[no_rw], 'right_to_left', type_rw, raft_waterway_RTL, num_raft))

        TOUCH_GRAVE = False
        for i in range(N_GRAVE):
            grave_x = grave_list[i][0]
            grave_y = grave_list[i][1]
            if not BAND_KEYBOUND and overlab(IMG_PLY, ply_x, ply_y, (grave_x+15, grave_y, WIDTH_GRAVE-15, HIEGHT_GRAVE)):
                TOUCH_GRAVE = True

        if not BAND_KEYBOUND and TOUCH_GRAVE:
            y_id -= 1
            TOUCH_GRAVE = False

        cur_x = max(cur_x, LEFT_BOUND)  # LIMIT BOUND OF SIDE LEFT
        cur_x = min(cur_x, RIGHT_BOUND) # LINIT BOUND OF SIDE RIGHT
        y_id  = max(y_id, 0)            # LIMIT BOUND OF SIDE DOWN
        y_id  = min(y_id, nY-1)         # LIMIT BOUND OF SIDE UP
        
        if not BAND_KEYBOUND: ply_stete = 'live'


        in_ground = overlab(IMG_PLY, ply_x, ply_y, GROUND) # CHECK PLAYER stay in GROUND
        if not BAND_KEYBOUND and  in_ground == False:
            ply_stete = 'drowned'
            # print('test: ', ply_x, ply_y)

        n_ghosts = len(ghost_runway_LTR)
        for i in range(n_ghosts):
            type_ghost = ghost_runway_LTR[i][2]
            width_ghost = IMG_GST[type_ghost-1].get_width()
            hieght_ghost = IMG_GST[type_ghost-1].get_height()
            pos_x_ghost = ghost_runway_LTR[i][0]
            pos_y_ghost = ghost_runway_LTR[i][1]
            if not BAND_KEYBOUND and overlab(IMG_PLY, ply_x, ply_y, (pos_x_ghost, pos_y_ghost, width_ghost, hieght_ghost)):
                ply_stete = 'crash'

        n_ghosts = len(ghost_runway_RTL)
        for i in range(n_ghosts):
            type_ghost = ghost_runway_RTL[i][2]
            width_ghost = IMG_GST[type_ghost-1].get_width()
            hieght_ghost = IMG_GST[type_ghost-1].get_height()
            pos_x_ghost = ghost_runway_RTL[i][0]
            pos_y_ghost = ghost_runway_RTL[i][1]
            if not BAND_KEYBOUND and overlab(IMG_PLY, ply_x, ply_y, (pos_x_ghost, pos_y_ghost, width_ghost, hieght_ghost)):
                ply_stete = 'crash'

        n_raft = len(raft_waterway_LTR)
        for i in range(n_raft):
            type_raft = raft_waterway_LTR[i][2]
            width_raft = IMG_RAFT[type_raft-1].get_width()
            hieght_raft = IMG_RAFT[type_raft-1].get_height()
            pos_x_raft = raft_waterway_LTR[i][0]
            pos_y_raft = raft_waterway_LTR[i][1]
            if BAND_KEYBOUND : break
            if overlab(IMG_PLY, ply_x, ply_y, (pos_x_raft, pos_y_raft, width_raft, hieght_raft)):
                ply_stete = 'live'
                if type_raft == 1:
                    cur_x += 2
                elif type_raft == 2:
                    cur_x += 3

        n_raft = len(raft_waterway_RTL)
        for i in range(n_raft):
            type_raft = raft_waterway_RTL[i][2]
            width_raft = IMG_RAFT[type_raft-1].get_width()
            hieght_raft = IMG_RAFT[type_raft-1].get_height()
            pos_x_raft = raft_waterway_RTL[i][0]
            pos_y_raft = raft_waterway_RTL[i][1]
            if BAND_KEYBOUND : break
            if overlab(IMG_PLY, ply_x, ply_y, (pos_x_raft, pos_y_raft, width_raft, hieght_raft)):
                ply_stete = 'live'
                if type_raft == 1:
                    cur_x -= 2
                elif type_raft == 2:
                    cur_x -= 3

        if not BAND_KEYBOUND and overlab(IMG_PLY, ply_x, ply_y, (25, 70, 500, 45)): # CHECK OVERLAB IN EACH GROUND
            ply_stete = 'live'

        if  (PLAY_STRL == False) :
            time_stroller += 1
        
        TIME_PER_APPEAR = FPS * 10

        if not BAND_KEYBOUND and time_stroller >= TIME_PER_APPEAR:
            time_stroller = 0
            PLAY_STRL = True

        if not BAND_KEYBOUND and PLAY_STRL:
            pos_x_strl += SPEED_STRL
            if pos_x_strl >= WIDTH:
                PLAY_STRL = False
                pos_x_strl = -WIDTH_STRL

            if not BAND_KEYBOUND and overlab(IMG_PLY, ply_x, ply_y, (pos_x_strl, pos_y_strl+15, WIDTH_STRL, HEIGHT_STRL-10)):
                ply_stete = 'crash'

        pos_x_coin = POS_COIN[select_coin][0]
        pos_y_coin = POS_COIN[select_coin][1]
        if not BAND_KEYBOUND and overlab(IMG_PLY, ply_x, ply_y, (pos_x_coin, pos_y_coin, WIDTH_COIN, HIEGHT_COIN)):
            COIN_SHOW = False
            score += 200

        if not BAND_KEYBOUND and COIN_SHOW == False:
            COIN_SHOW = True
            n_remain_coin = len(set_coin)
            
            if not BAND_KEYBOUND and n_remain_coin <= 0: # WHEN KEEP COIN ALL STATE
                set_coin = [i for i in range(5)]         # foctor of LEVEL GAME IS 'score'
                n_remain_coin = 5
                cur_x = (LEFT_BOUND + RIGHT_BOUND) // 2
                y_id = 0
                level += 1                               # NOT factor, it just show

            chioce_coin = randint(0, n_remain_coin-1)
            select_coin = set_coin[chioce_coin]

            set_coin.pop(chioce_coin)

        FPS = 10*(3+(score//1000))

        if not BAND_KEYBOUND and (ply_stete == 'crash' or ply_stete == 'drowned'):
            BAND_KEYBOUND = True
            ply_die.append((ply_x, ply_y, ply_stete))
            cur_x = (LEFT_BOUND + RIGHT_BOUND)//2
            y_id = 0
            pass

        ply_x = cur_x
        ply_y = POS_Y[y_id]


        """ ============ DISPLAY OF GAME ============= """
        fill_scr(COLOR_BLACK)
        
        push_img(IMG_BG, 25, 70)                  # DRAW BACKGROUND STAGE

        player_die(ply_die)                       # SHOW HISTORY OF DEAD'PLAYER

        grave_show(grave_list)                    # DRAW GRAVE
        
        waterway_LTR(raft_waterway_LTR)           # DRAW RAFT LEFT TO RIGHT
        waterway_RTL(raft_waterway_RTL)           # DRAW RAFT RIGHT TO LEFT

        if COIN_SHOW :                            # DRAW COIN TO STAGE
            coin_show(POS_COIN[select_coin])

        if (BAND_KEYBOUND == False) :             # SHOW PLAYER LIVE
            player(ply_x, ply_y, ply_stete)           

        traffic_LTR(ghost_runway_LTR)             # DRAW TRAFFIC GHOST FROM LEFT TO RIGHT
        traffic_RTL(ghost_runway_RTL)             # DRAW TRAFFIC GHOST FROM RIGHT TO LEFT

        push_img(IMG_STRL, pos_x_strl, pos_y_strl)# DRAW STROLLER

        draw_rect(0, 70, 25, 495, COLOR_BLACK)    # DRAW BOUND LEFT
        draw_rect(525, 70, 25, 495, COLOR_BLACK)  # DRAW BOUND RIGHT
        draw_bound(COLOR_GREY, 4)                 # DRAW BOUND OF STAGE

        push_img(IMG_NAME_GAME, 175, 10)          # PUSH name of GAME to Screen

        show_score(score)                         # SHOW score ps. it is foctor of level game
        show_level(level)                         # SHOW level status

        message_to_screen("DEMO", COLOR_GREEN, 285) # tag DEMO for this game

        if BAND_KEYBOUND :                        # PROCRESS START WHEN PLAYER DIE
            show_best_score(score, level)

        # draw_gird()
        """ ========================================== """

        update_screen()
        clock_time.tick(FPS)

# START game loop

REGAME = True
while REGAME:
    REGAME = game_loop()

'''
how to play : KEY
a or arrow left : move lefr
d or arrow right : move right
s or arrow down : move down
w or arrow up : move up

space_bar : live again
c : clear body
'''