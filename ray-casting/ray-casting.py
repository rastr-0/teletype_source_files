#packages
import pygame
import sys
import math

#global constants
SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2
MAP_SIZE = 8
TILE_SIZE = int((SCREEN_WIDTH / 2) / MAP_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 160
STEP_ANGLE = FOV / CASTED_RAYS
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
SCALE = (SCREEN_WIDTH / 2) / CASTED_RAYS
#global variables
player_x = (SCREEN_WIDTH / 2) / 2
player_y = (SCREEN_WIDTH / 2) / 2
player_angle = math.pi

#map
MAP = (
    '########'
    '# #    #'
    '# #  ###'
    '#      #'
    '##     #'
    '#  ### #'
    '#   #  #'
    '########'
)

#init pygame
pygame.init()

#game window
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ray-casting')

#init timer
clock = pygame.time.Clock()

def draw_map():
    #iterate over map
    for i in range(MAP_SIZE):
        for j in range(MAP_SIZE):
            #calculate square index
            square = i * MAP_SIZE + j

            #draw map
            pygame.draw.rect(
                win, (191, 191, 191) if MAP[square] == '#' else (65, 65, 65),
                (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1)
            )

    #draw player
    pygame.draw.circle(win, (162, 0, 255), (int(player_x), int(player_y)), 12)

#ray-casting algorithm
def ray_casting():
    #left angle of FOV
    start_angle = player_angle - HALF_FOV
    
    #iterate over casted rays
    for ray in range(CASTED_RAYS):
        for depth in range(MAX_DEPTH):
            #get ray target coordinates
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y +  math.cos(start_angle) * depth

            #convert target x, y coordinates to map col, row
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)  

            #calculate map square index
            square = row * MAP_SIZE + col
            
            #print(square)

            if MAP[square] == '#':
                pygame.draw.rect(win, (195, 137, 38), (col * TILE_SIZE,
                                                                        row * TILE_SIZE,
                                                                        TILE_SIZE - 1,
                                                                        TILE_SIZE - 1))
                
                #draw casted ray
                pygame.draw.line(win, (233, 166, 49), (player_x, player_y), (target_x, target_y))

                #wall shading
                color = 255 / (1 + depth * depth * 0.0001)

                #fix fish eye effect
                depth *= math.cos(player_angle - start_angle) 

                #calculate wall_height
                wall_height = 21000 / (depth)

                #fix stuck at the wall
                if wall_height > SCREEN_HEIGHT:
                    wall_height = SCREEN_HEIGHT

                #draw 3D projection
                pygame.draw.rect(win, (color, color, color), 
                                            (SCREEN_HEIGHT + ray * SCALE, 
                                            (SCREEN_HEIGHT / 2) - wall_height / 2, SCALE, wall_height))
                
                break

        #increment angle by step
        start_angle += STEP_ANGLE

#movement direction
forward = True

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    #convert player x, y coordinates to map col, row
    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)  

    #calculate map square index
    square = row * MAP_SIZE + col

    # player hits the wall (collision detection)
    if MAP[square] == '#': 
        if forward:
            player_x -= -1 * math.sin(player_angle) * 5
            player_y -= math.cos(player_angle) * 5
        else:
            player_x += -1 * math.sin(player_angle) * 5
            player_y += math.cos(player_angle) * 5
            
    
    #update 2D background
    pygame.draw.rect(win, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

    #update 3D background
    pygame.draw.rect(win, (100, 100, 100), (480, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))
    pygame.draw.rect(win, (200, 200, 200), (480, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))

    draw_map()
    ray_casting()

    #get user input
    keys = pygame.key.get_pressed()

    #handle user input
    if keys[pygame.K_LEFT]:
        #working with radians, not degrees
        player_angle -= 0.1
    elif keys[pygame.K_RIGHT]:
        player_angle += 0.1
    elif keys[pygame.K_UP]:
        forward = True
        player_x += -1 * math.sin(player_angle) * 5
        player_y += math.cos(player_angle) * 5
    elif keys[pygame.K_DOWN]:
        forward = False
        player_x -= -1 * math.sin(player_angle) * 5
        player_y -= math.cos(player_angle) * 5

    #set FPS
    clock.tick(30)

    #set FPS
    fps = str(int(clock.get_fps()))
    font = pygame.font.SysFont('Arial', 30)
    fpssurface = font.render(fps, False, (255, 255, 255))
    win.blit(fpssurface, (int(SCREEN_WIDTH / 2), 0))

    #update display
    pygame.display.flip()