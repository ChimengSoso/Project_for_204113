import pygame
import time

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

# SETTING GAME DISPLAY
gameDisplay = pygame.display.set_mode([WIDTH, HIGHT])
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
        pygame.draw.line(gameDisplay, WHITE, (0, h[i]), (WIDTH, h[i]), 2);

    for i in range(len_w):
        pygame.draw.line(gameDisplay, WHITE, (w[i], 0), (w[i], HIGHT), 2);

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

def push_img(img, x, y): # push image to screen in position (x, y)
    gameDisplay.blit(img, (x, y))

def fill_scr(color):     # fill color on the screen of windows
    gameDisplay.fill(color)

def player(x, y):
    # draw_rect(x, y, 20, 35, COLOR_BLUE)
    push_img(IMG_PLY, x, y)

def overlab(img, x_img, y_img, obj) :
    img_x = x_img
    img_y = y_img
    img_width = img.get_width()
    img_hieght = img.get_height()
    obj_x = obj[0]
    obj_y = obj[1]
    obj_width = obj[2]
    obj_hieght = obj[3]
    x_overlab = (img_x <= obj_x + obj_width and img_x + img_width >= obj_x)
    y_overlab = (img_y <= obj_y + obj_hieght and img_y + img_hieght >= obj_y)
    return x_overlab and y_overlab;

def game_loop():
    GAME_OVER = False
    
    ply_x = 0
    ply_y = 0

    LEFT_BOUND = 30
    N_STEP_X = 15
    STEP_X = 35
    RIGHT_BOUND = LEFT_BOUND + (N_STEP_X-1) * STEP_X - 20
    CUR_X = (LEFT_BOUND + RIGHT_BOUND) // 2
    
    POS_Y = [530, 482, 438, 392, 345, 296, 250, 205, 165, 120, 75]
    nY = len(POS_Y)
    y_id = 0


    GROUND_X = 25
    GROUND_Y = 295
    GROUND_WIDTH = 500
    GROUND_HIEGHT = 270
    GROUND = (GROUND_X, GROUND_Y, GROUND_WIDTH, GROUND_HIEGHT)

    while not GAME_OVER:
        events = pygame.event.get()
        for ent in events:
            game_exit(ent)

            if ent.type == pygame.KEYDOWN:
                key = ent.key
                if key == pygame.K_LEFT or key == pygame.K_a:
                    # x_id -= 1
                    CUR_X -= STEP_X

                if key == pygame.K_RIGHT or key == pygame.K_d:
                    # x_id += 1
                    CUR_X += STEP_X

                if key == pygame.K_UP or key == pygame.K_w:
                    y_id += 1

                if key == pygame.K_DOWN or key == pygame.K_s:
                    y_id -= 1

                if  key == pygame.K_p:
                    pass



        CUR_X = max(CUR_X, LEFT_BOUND)  # LIMIT BOUND OF SIDE LEFT
        CUR_X = min(CUR_X, RIGHT_BOUND) # LINIT BOUND OF SIDE RIGHT
        y_id  = max(y_id, 0)            # LIMIT BOUND OF SIDE DOWN
        y_id  = min(y_id, nY-1)         # LIMIT BOUND OF SIDE UP
        
        ply_x = CUR_X
        ply_y = POS_Y[y_id]

        # if ply_x 

        """ ============ DISPLAY OF GAME ============= """
        fill_scr(COLOR_BLACK)
        # draw_gird()
        push_img(IMG_BG, 25, 70)                  # DRAW BACKGROUND STAGE
        draw_rect(0, 70, 25, 495, COLOR_BLACK)    # DRAW BOUND LEFT
        draw_rect(525, 70, 25, 495, COLOR_BLACK)  # DRAW BOUND RIGHT
        draw_bound(COLOR_GREY, 4)                 # DRAW BOUND OF STAGE

        player(ply_x, ply_y)
        if overlab(IMG_PLY, ply_x, ply_y, GROUND): # CHECK PLAYER stay in GROUND
            print("Stay in Ground")
        else:
            print("Stay in Water")

        """ ========================================== """
        update_screen()
        clock_time.tick(FPS)

# START game loop
game_loop()