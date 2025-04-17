import numpy as np
import pygame

# CONSTANTS
CELL_SIZE = 5
LINE_WIDTH = 2
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
GRID_SIZE = 100           # For a GRID_SIZE x GRID_SIZE grid

def numNeighbours(board, x,y):
    total = 0
    if x-1 >= 0:
        if board[x-1,y] == 1: # Check top neighbour
            total += 1
        if y-1 >= 0:
            if board[x-1,y-1] == 1: # Check top left neighbour
                total += 1
        if y+1 < GRID_SIZE:
            if board[x-1,y+1] == 1: # Check top right neighbour
                total += 1
    if y-1 >= 0:
        if board[x,y-1] == 1: # Check left neighbour
            total += 1
        if x+1 < GRID_SIZE:
            if board[x+1, y-1] == 1: # Check bottom left neighbour
                total += 1
    if y+1 < GRID_SIZE:
        if board[x, y+1] == 1: # Check right neighbour
            total += 1
        if x+1 < GRID_SIZE:
            if board[x+1, y+1] == 1: # Check bottom right neighbour
                total += 1
    if x+1 < GRID_SIZE and board[x+1, y] == 1: # Check bottom neighbour
        total += 1

    return total

def resetBoard():
    for i, cell in enumerate(rectangle_ref):
        conwayBoard1[int(i/GRID_SIZE), i%GRID_SIZE] = 0
        conwayBoard2[int(i/GRID_SIZE), i%GRID_SIZE] = 0
        pygame.draw.rect(screen, (0, 0, 0), cell)

def generateContainer(x,y):
    # Draw Border
    full_length = GRID_SIZE*CELL_SIZE
    pygame.draw.line(screen, "black", (x, y-LINE_WIDTH), (x+full_length, y-LINE_WIDTH), width=LINE_WIDTH)   # TOP
    pygame.draw.line(screen, "black", (x-LINE_WIDTH, y), (x-LINE_WIDTH, y+full_length), width=LINE_WIDTH)   # LEFT
    pygame.draw.line(screen, "black", (x, y+full_length), (x+full_length, y+full_length), width=LINE_WIDTH)   # BOTTOM
    pygame.draw.line(screen, "black", (x+full_length, y), (x+full_length, y+full_length), width=LINE_WIDTH)   # RIGHT

    # Create tile references
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rectangle_ref.append(pygame.Rect(x+(j*CELL_SIZE), y+(i*CELL_SIZE), CELL_SIZE, CELL_SIZE))

rectangle_ref = []
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
deltaTime = 0
timer = 0

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 14)

pygame.display.set_caption("Conway's game of life")
# Background colour (255, 226, 99)
screen.fill((73, 92, 91))

x_start = SCREEN_WIDTH/2 - (GRID_SIZE/2) * CELL_SIZE
y_start = SCREEN_HEIGHT/2 - (GRID_SIZE/2) * CELL_SIZE

# Generate Board
generateContainer(x_start, y_start)
startToggleRef = pygame.Rect(x_start, y_start+(GRID_SIZE*CELL_SIZE) + CELL_SIZE*2, GRID_SIZE*CELL_SIZE, CELL_SIZE*5)

toggleText = font.render('Toggle', True, (255, 255, 255), (73, 92, 91))
screen.blit(toggleText, startToggleRef)
resetButtonRef = pygame.Rect(x_start+(GRID_SIZE*CELL_SIZE) + CELL_SIZE*2, y_start, CELL_SIZE*5, GRID_SIZE*CELL_SIZE)

resetText = font.render('Reset', True, (255, 255, 255), (73, 92, 91))
screen.blit(resetText, resetButtonRef)
numIterRef = pygame.Rect(x_start, y_start - 25, CELL_SIZE, CELL_SIZE)
conwayBoard1 = np.zeros((GRID_SIZE,GRID_SIZE))
conwayBoard2 = np.zeros((GRID_SIZE,GRID_SIZE))
mouseButtonFlag = False
gameToggle = False
numIterations = 0
resetBoard() # Initialize background to black

while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            mouseButtonFlag = False

        elif event.type == pygame.MOUSEBUTTONDOWN or mouseButtonFlag:
            mouseButtonFlag = True
            x, y = event.pos
            # Check if start/stop button is being pressed
            if event.type == pygame.MOUSEBUTTONDOWN and startToggleRef.collidepoint(x,y):
                gameToggle = not gameToggle
            # Check if reset button is being pressed
            if event.type == pygame.MOUSEBUTTONDOWN and resetButtonRef.collidepoint(x,y):
                resetBoard()
                numIterations = 0
                iterText = font.render('Number of Iterations:         ', True, (255, 255, 255), (73, 92, 91))
                screen.blit(iterText, numIterRef)
            for i, cell in enumerate(rectangle_ref):
                if cell.collidepoint(x,y):
                    if pygame.mouse.get_pressed()[2] == True:
                        pygame.draw.rect(screen, (0, 0, 0), cell)
                        conwayBoard1[int(i/GRID_SIZE), i%GRID_SIZE] = 0
                    else:
                        pygame.draw.rect(screen, (255, 255, 255), cell)
                        conwayBoard1[int(i/GRID_SIZE), i%GRID_SIZE] = 1
                        
            
        elif event.type == pygame.QUIT:
            running = False
        
    if gameToggle:
        timer -= deltaTime
        if timer <= 0: 
            for i in range(GRID_SIZE):          # rows
                for j in range(GRID_SIZE):      # columns
                    match numIterations%2:
                        case 0:
                            # update each of the items of the first board and place them on the second board
                            num_neighbours1 = numNeighbours(conwayBoard1, i,j)
                                
                            # Any live cell with two or three live neighbours lives on to the next generation
                            if conwayBoard1[i,j] == 1 and (num_neighbours1 == 2 or num_neighbours1 == 3):
                                conwayBoard2[i,j] = 1
                                pygame.draw.rect(screen, (255, 255, 255), rectangle_ref[j+(i*GRID_SIZE)])
                            # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction
                            elif conwayBoard1[i,j] == 0 and num_neighbours1 == 3:
                                conwayBoard2[i,j] = 1
                                pygame.draw.rect(screen, (255, 255, 255), rectangle_ref[j+(i*GRID_SIZE)])
                            else:
                                conwayBoard2[i,j] = 0
                                pygame.draw.rect(screen, (0, 0, 0), rectangle_ref[j+(i*GRID_SIZE)])
                                
                        case 1:
                            # update each of the items of the second board and place them on the first board
                            num_neighbours2 = numNeighbours(conwayBoard2, i,j) 
                                
                            # Any live cell with two or three live neighbours lives on to the next generation
                            if conwayBoard2[i,j] == 1 and (num_neighbours2 == 2 or num_neighbours2 == 3):
                                conwayBoard1[i,j] = 1
                                pygame.draw.rect(screen, (255, 255, 255), rectangle_ref[j+(i*GRID_SIZE)])
                            # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction
                            elif conwayBoard2[i,j] == 0 and num_neighbours2 == 3:
                                conwayBoard1[i,j] = 1
                                pygame.draw.rect(screen, (255, 255, 255), rectangle_ref[j+(i*GRID_SIZE)])
                            else:
                                conwayBoard1[i,j] = 0
                                pygame.draw.rect(screen, (0, 0, 0), rectangle_ref[j+(i*GRID_SIZE)])

            timer = 0.05
            numIterations += 1
            iterText = font.render('Number of Iterations: ' + str(numIterations), True, (255, 255, 255), (73, 92, 91))
            screen.blit(iterText, numIterRef)

    # flip the display to update screen
    pygame.display.flip()

    deltaTime = clock.tick(60) / 1000 # convert to seconds

pygame.quit()