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
COLOR_GREY = (91, 91, 91)

# SETTING IMAGE
IMG_BG = pygame.image.load('img/bg.png')
IMG_PLY = pygame.image.load('img/player_live.png')
IMG_CRASH = pygame.image.load('img/player_crash.png')
IMG_DROWNED = pygame.image.load('img/player_drowned.png')
# IMG_CAR = [pygame.image.load('img/car' + str(i+1) + '.png') for i in range(3)]

# SETTING GAME DISPLAY
SIZE_SCREEN = (WIDTH, HIGHT)
gameDisplay = pygame.display.set_mode(SIZE_SCREEN)
pygame.display.set_caption("CROSSINHG")

# SET CLOCK
clock_time = pygame.time.Clock()

# SET FPS
FPS = 30

# SET FONT
small_font = pygame.font.SysFont("comicsansms", 25)
med_font = pygame.font.SysFont("comicsansms", 50)
large_font = pygame.font.SysFont("comicsansms", 80)

def game_exit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()

def draw_gird():
    h = [70, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 35]
    len_h = len(h)
    for i in range(1, len_h):
        h[i] += h[i-1]

    w = [25, 500, 25]
    len_w = len(w)
    for i in range(1, len_w):
        w[i] += w[i-1]

    for i in range(len_h):
        pygame.draw.line(gameDisplay, COLOR_WHITE, (0, h[i]), (WIDTH, h[i]), 2);

    for i in range(len_w):
        pygame.draw.line(gameDisplay, COLOR_WHITE, (w[i], 0), (w[i], HIGHT), 2);

def draw_bound(color = COLOR_WHITE, size_line = 2):
    draw_line(25, 70, 525, 70, color, size_line)
    draw_line(525, 70, 525, 565, color, size_line)
    draw_line(25, 565, 525, 565, color, size_line)
    draw_line(25, 70, 25, 565, color, size_line)

def update_screen():
    pygame.display.update()

def draw_line(x1, y1, x2, y2, color = COLOR_WHITE, size_line = 2):
    pygame.draw.line(gameDisplay, color, (x1, y1), (x2, y2), size_line)

def draw_rect(pos_x, pos_y, widht_rect, height_rect, color = COLOR_WHITE):
    pygame.draw.rect(gameDisplay, color, [pos_x, pos_y, widht_rect, height_rect])

def draw_circle(x, y, redius, color = COLOR_WHITE) :
    pygame.draw.circle(gameDisplay, color, (x, y), int(redius))

def push_img(img, x, y): # push image to screen in position (x, y)
    gameDisplay.blit(img, (x, y))

def fill_scr(color):     # fill color on the screen of windows
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

def traffic_LTR(cars) :
    n = len(cars)
    remove_car = set()
    for i in range(n):
        car = cars[i]
        car_x = car[0]
        car_y = car[1]
        speed_car = car[2]
        draw_rect(car_x, car_y, 40, 20, COLOR_RED)
        cars[i][0] += speed_car      # CHANGE SPEED OF cars[i]
        if car_x >= WIDTH :
            remove_car.add(i)
    
    car_live = []
    for i in range(n):
        if i not in remove_car:
            car_live.append(cars[i])

    cars.clear()
    cars.extend(car_live)

def traffic_RTL(cars) :
    n = len(cars)
    remove_car = set()
    for i in range(n):
        car = cars[i]
        car_x = car[0]
        car_y = car[1]
        speed_car = car[2]
        draw_rect(car_x, car_y, 40, 20, COLOR_RED)
        cars[i][0] += speed_car      # CHANGE SPEED OF cars[i]
        if car_x < 0 :
            remove_car.add(i)
    
    car_live = []
    for i in range(n):
        if i not in remove_car:
            car_live.append(cars[i])

    cars.clear()
    cars.extend(car_live)

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

def create_runway(hieght_of_runway, type_of_runway = None, n_car = 1) :
    cars_runway = list()
    speed_car = randint(1, 5)

    if type_of_runway == 'left_to_rigth':
        start_x_car = randint(-20, -10)
        cars_runway.append([start_x_car, hieght_of_runway, speed_car])

        for i in range(1, n_car):
            speed_car = randint(1, cars_runway[i-1][2])
            start_x_car = cars_runway[i-1][0] - 50
            cars_runway.append([start_x_car, hieght_of_runway, speed_car])

    elif type_of_runway == 'right_to_left':    
        speed_car = -speed_car
        start_x_car = randint(WIDTH, WIDTH + 10)
        cars_runway.append([start_x_car, hieght_of_runway, speed_car])

        for i in range(1, n_car):
            speed_car = randint(-5, cars_runway[i-1][2])
            start_x_car = cars_runway[i-1][0] + 50
            cars_runway.append([start_x_car, hieght_of_runway, speed_car])

    return cars_runway

GAME_OVER = False

def game_loop():    
    global GAME_OVER
    global OPEN_RUNWAY1

    BAND_KEYBOUND = False 

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

    #SET CAR INFO
    car_runway_LTR = create_runway(POS_Y[1], 'left_to_rigth') + create_runway(POS_Y[3], 'left_to_rigth')
    car_runway_RTL = create_runway(POS_Y[2], 'right_to_left') + create_runway(POS_Y[4], 'right_to_left')

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
                    pass

        # ===================== LOGIC GAME ======================= #
        if len(car_runway_RTL) < 5:
            car_runway_RTL.extend(create_runway(POS_Y[2*randint(1, 2)], 'right_to_left'))

        if len(car_runway_LTR) < 1:
            car_runway_LTR.extend(create_runway(POS_Y[2*randint(1, 2)-1], 'left_to_rigth'))

        cur_x = max(cur_x, LEFT_BOUND)  # LIMIT BOUND OF SIDE LEFT
        cur_x = min(cur_x, RIGHT_BOUND) # LINIT BOUND OF SIDE RIGHT
        y_id  = max(y_id, 0)            # LIMIT BOUND OF SIDE DOWN
        y_id  = min(y_id, nY-1)         # LIMIT BOUND OF SIDE UP
        
        if not BAND_KEYBOUND: ply_stete = 'live'

        in_ground = overlab(IMG_PLY, ply_x, ply_y, GROUND) # CHECK PLAYER stay in GROUND
        if in_ground == False:
            ply_stete = 'drowned'
            # print('test: ', ply_x, ply_y)

        n_cars = len(car_runway_LTR)
        for i in range(n_cars):
            if overlab(IMG_PLY, ply_x, ply_y, (car_runway_LTR[i][0], car_runway_LTR[i][1], 40, 20)):
                ply_stete = 'crash'

        n_cars = len(car_runway_RTL)
        for i in range(n_cars):
            if overlab(IMG_PLY, ply_x, ply_y, (car_runway_RTL[i][0], car_runway_RTL[i][1], 40, 20)):
                ply_stete = 'crash'

        ply_x = cur_x
        ply_y = POS_Y[y_id]

        """ ============ DISPLAY OF GAME ============= """
        fill_scr(COLOR_BLACK)
        
        push_img(IMG_BG, 25, 70)                  # DRAW BACKGROUND STAGE
        
        # draw_gird()
        player(ply_x, ply_y, ply_stete)
        traffic_LTR(car_runway_LTR)
        traffic_RTL(car_runway_RTL)

        draw_rect(0, 70, 25, 495, COLOR_BLACK)    # DRAW BOUND LEFT
        draw_rect(525, 70, 25, 495, COLOR_BLACK)  # DRAW BOUND RIGHT
        draw_bound(COLOR_GREY, 4)                 # DRAW BOUND OF STAGE
        """ ========================================== """

        if ply_stete == 'crash' or ply_stete == 'drowned':
            # BAND_KEYBOUND = True
            pass

        update_screen()
        clock_time.tick(FPS)

def game_over():
    print('game over')
    while True:
        # =============== EVENT PROCESSING ===================== #
        events = pygame.event.get()
        for ent in events:
            game_exit(ent)

        clock_time.tick(FPS)

# START game loop
game_loop()
game_over()

'''   ========= file image ============
self.image = pygame.image.load("player1.png")
self.image2 = pygame.transform.flip(self.image, True, False)
'''