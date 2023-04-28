import pygame, sys
from utils.button import Button
import sente 
from sente import stone
from agents import RandomAgent

pygame.init()

SCREEN = pygame.display.set_mode((660, 450))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
def Bo_Luot(game): 
    game.pss()
    print('Bo Luoted')

def Bo_Cuoc(game): 
    game.resign()
    print('Bo Cuoc')

def game_mode():
    pygame.display.set_caption("Go-Game")
    while True:
        SCREEN.fill((255,255,255))
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        PEOPLE = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(330, 100), 
                            text_input="PEOPLE", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        AGENT_0 = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(330, 220), 
                            text_input="AGENT_FIRST", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        AGENT_1 = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(330, 340), 
                            text_input="AGENT_SECOND", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        PEOPLE.update(SCREEN)
        AGENT_0.update(SCREEN)
        AGENT_1.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PEOPLE.checkForInput(MENU_MOUSE_POS):
                    play()
                if AGENT_0.checkForInput(MENU_MOUSE_POS):
                    play(stone.BLACK)
                if AGENT_1.checkForInput(MENU_MOUSE_POS):
                    play(stone.WHITE)
        pygame.display.update()


def play(may = None):
    pygame.display.set_caption("Go-Game")
    
    image = pygame.image.load("assets/go_game_9x9.png")
    black_image_chessman = pygame.image.load("assets/black.png")
    white_image_chessman = pygame.image.load("assets/white.png")
    color = (255,255,255)
    position = (0,0)

    n = 9
    game = sente.Game(n)
    #Bot 
    if(may != None):
        agent = RandomAgent(game,may)
    
    exit = False
    while not exit:
        if (game.is_over() == True) :
            print(game.score())
            print(game.get_result())
            print(game.get_winner())
            break  
        #Luot cua Bot  
        if(may != None and game.get_active_player() == may):
            game.play(agent.next_move())

        SCREEN.fill(color)
        SCREEN.blit(image,dest = position)
        # Hien thi con chuot la quan co khi di chuyen
        mx,my=pygame.mouse.get_pos()
        if(game.get_active_player() == stone.BLACK) :
            image_virtual = black_image_chessman
        elif (game.get_active_player() == stone.WHITE) :
            image_virtual = white_image_chessman
        SCREEN.blit(image_virtual,(mx-16,my-16))

        # Hien thi cac nut Button
        PLAY_BACK = Button(image=None, pos=(550, 430), 
                            text_input="BACK", font=get_font(20), base_color="Black", hovering_color="Green")
        BO_LUOT = Button(image=None, pos=(550, 30), 
                            text_input="Bo Luot", font=get_font(20), base_color="Black", hovering_color="Green")
        BO_CUOC = Button(image=None, pos=(550, 130), 
                            text_input="Bo cuoc", font=get_font(20), base_color="Black", hovering_color="Green")
        PLAY_BACK.update(SCREEN)
        BO_LUOT.update(SCREEN)
        BO_CUOC.update(SCREEN)

        #hien thi diem
        # Diem = "W" + str(game.score()[stone.WHITE]) + ":" + "B" + str(game.score()[stone.BLACK])
        Diem = get_font(20).render('Diem', False, (0, 0, 0))
        SCREEN.blit(Diem,(500,240))
        for i in range(n):
            for j in range(n):
                if(game.get_board().get_stone(i+1,j+1) == sente.stone.BLACK):
                    SCREEN.blit(black_image_chessman,((i)*49+15,(j)*49+15))
                elif(game.get_board().get_stone(i+1,j+1) == sente.stone.WHITE):
                    SCREEN.blit(white_image_chessman,((i)*49+15,(j)*49+15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP :
                exit = False
            elif event.type == pygame.MOUSEBUTTONDOWN :
                place_x = mx - 16
                place_y = my - 16
                # print(place_x,place_y)
                if place_x%49 >=1 and place_x%49 <= 29  and place_y %49 >= 1 and place_y%49 <=29:
                    if(game.is_legal(int(place_x/49)+1,int(place_y/49)+1)):					
                        game.play(int(place_x/49)+1,int(place_y/49)+1)
                if BO_LUOT.checkForInput((mx,my)):
                    Bo_Luot(game)
                if PLAY_BACK.checkForInput((mx,my)):
                    main_menu()  
                if BO_CUOC.checkForInput((mx,my)):
                    Bo_Cuoc(game)  

        pygame.display.update()

    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(25).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(330, 50))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(330, 150), 
                            text_input="PLAY", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(330, 270), 
                            text_input="OPTIONS", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(330, 390), 
                            text_input="QUIT", font=get_font(20), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    game_mode()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()