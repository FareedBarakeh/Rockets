import pygame
from Packages.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE
from Packages.game import Game
from pygame import mixer

#Frame Per Second
FPS = 60


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Rockets')

def get_row_col_from_mouse(pos): 
    x, y = pos 
    row = y // SQUARE_SIZE 
    col = x // SQUARE_SIZE 
    return row, col

mixer.init()

x = 1
boom = mixer.Sound(r'S:\Projects\Programing Projects\-\Projects\Rockets\assets\boom.ogg')
hoom = mixer.Sound(r'S:\Projects\Programing Projects\-\Projects\Rockets\assets\hoom.ogg')
soundtrack = mixer.music.load(r'S:\Projects\Programing Projects\-\Projects\Rockets\assets\Deep-Blue-Day-_Remastered-2019_-_128-kbps__1.ogg')
#mixer.music.play(-1)

def main(): 
    run = True 
    clock = pygame.time.Clock() 
    game = Game(WIN)

    #while is game is running 
    while run:

        clock.tick(FPS) 

        if game.winner() != None: 
            print(game.winner()) 
            run = False 

        for event in pygame.event.get():

            #if we hit quit(red button) 
            if event.type == pygame.QUIT:
                run = False                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and game.selected:
                    game.change_dir(-1)
                if event.key == pygame.K_RIGHT and game.selected:
                    game.change_dir(1)
                if event.key==pygame.K_SPACE:  
                    game.change_turn()       
                        
            if event.type == pygame.MOUSEBUTTONDOWN:
                #hoom.play()
                #position we hit with mouse 
                pos = pygame.mouse.get_pos()
                #if event.button == 3:
                    #boom.play()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col, event.button)            
        game.update()
    pygame.quit()
main()