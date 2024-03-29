import pygame
import sys
from utils.button import Button
import sente
from sente import stone
from MyGame import MyGame as Game
from agents import RandomAgent, AlphaBetaPruningAgent, DropAgent

pygame.init()

SCREEN = pygame.display.set_mode((660, 450))
pygame.display.set_caption("Menu")
BOT = 4
TIME = 0
BG = pygame.image.load("assets/Background.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def Bo_Luot(game):
    game.pss()
    print('Bo Luoted')


def Bo_Cuoc(game):
    # game.resign()
    print('Bo Cuoc')


def end_game(game, screen):
    while True:
        screen.fill((255, 255, 255))
        if (game.get_winner() == stone.BLACK):
            win = "Black thang"
        elif (game.get_winner() == stone.WHITE):
            win = "WHITE thang"
        Winner = get_font(20).render(win, False, (0, 0, 0))
        screen.blit(Winner, (230, 100))

        score = 'BLACK ' + \
            str(game.score()[stone.BLACK]) + " --- " + \
            str(game.score()[stone.WHITE]) + ' WHITE'
        Score = get_font(20).render(score, False, (0, 0, 0))
        screen.blit(Score, (100, 200))
        # print(game.get_result())
        # Hien thi cac nut Button
        PLAY_BACK = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(330, 320),
                           text_input="BACK", font=get_font(20), base_color="#d7fcd4", hovering_color="Green")
        PLAY_BACK.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(pygame.mouse.get_pos()):
                    main_menu()
        pygame.display.update()


def surrender(screen, loser):
    while True:
        screen.fill((255, 255, 255))
        if (loser == stone.WHITE):
            win = "Black thang"
        elif (loser == stone.BLACK):
            win = "WHITE thang"
        Winner = get_font(20).render(win, False, (0, 0, 0))
        screen.blit(Winner, (230, 200))
        # print(game.get_result())
        # Hien thi cac nut Button
        PLAY_BACK = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(330, 320),
                           text_input="BACK", font=get_font(20), base_color="#d7fcd4", hovering_color="Green")
        PLAY_BACK.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(pygame.mouse.get_pos()):
                    main_menu()
        pygame.display.update()


def game_mode():
    pygame.display.set_caption("Go-Game")
    while True:
        SCREEN.fill((255, 255, 255))
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


def play(may=None):
    pygame.display.set_caption("Go-Game")

    image = pygame.image.load("assets/go_game_9x9.png")
    black_image_chessman = pygame.image.load("assets/black.png")
    white_image_chessman = pygame.image.load("assets/white.png")
    color = (255, 255, 255)
    position = (0, 0)

    n = 9
    game = Game(n)
    now_move = [20, 20]
    # Bot
    if (may != None):
        # print(BOT)
        if (BOT == 1):
            agent = RandomAgent(game, may)
        elif BOT == 2:
            agent = AlphaBetaPruningAgent(game, may, 1)
        elif BOT == 3:
            agent = AlphaBetaPruningAgent(game, may, 3)
        elif BOT == 4:
            agent = DropAgent(game, may, 4, 10)

    exit = False
    num_pass = 0
    bo_luot_text = ""
    while not exit:
        if num_pass == 2:
            end_game(game, SCREEN)
            break
        # Luot cua Bot
        if (may != None and game.get_active_player() == may):
            turn_may = agent.next_move(time_mode=False)
            if turn_may is not None:
                bo_luot_text = ""
                now_move = [turn_may.get_x(), turn_may.get_y()]
                num_pass = 0
            else:
                num_pass += 1
            game.play(turn_may)
            if turn_may is None:
                if game.get_active_player() == stone.BLACK:
                    txt = "W"
                else:
                    txt = "B"
                bo_luot_text = f'{txt} bo luot'

        SCREEN.fill(color)
        SCREEN.blit(image, dest=position)

        bo_luot_component = get_font(18).render(
            bo_luot_text, False, (255, 0, 0))
        SCREEN.blit(bo_luot_component, (470, 340))
        # Hien thi con chuot la quan co khi di chuyen
        mx, my = pygame.mouse.get_pos()
        if (game.get_active_player() == stone.BLACK):
            image_virtual = black_image_chessman
        elif (game.get_active_player() == stone.WHITE):
            image_virtual = white_image_chessman
        SCREEN.blit(image_virtual, (mx-16, my-16))

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

        # hien thi diem
        diem_text = "W" + \
            str(game.score()[stone.WHITE]) + ":" + \
            "B" + str(game.score()[stone.BLACK])
        Diem = get_font(20).render('Diem', False, (0, 0, 0))
        SCREEN.blit(Diem, (500, 240))
        diem_component = get_font(18).render(diem_text, False, (0, 0, 0))
        SCREEN.blit(diem_component, (465, 280))
        for i in range(n):
            for j in range(n):
                if (game.get_board()[i, j] == sente.stone.BLACK):
                    SCREEN.blit(black_image_chessman, ((i)*49+15, (j)*49+15))
                elif (game.get_board()[i, j] == sente.stone.WHITE):
                    SCREEN.blit(white_image_chessman, ((i)*49+15, (j)*49+15))
        if (now_move[0] != 20):
            pygame.draw.circle(SCREEN, (0, 100, 100), ((
                now_move[0]+1)*49-18, (now_move[1]+1)*49-18), 18, 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                exit = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                place_x = mx - 16
                place_y = my - 16
                if place_x % 49 >= 1 and place_x % 49 <= 29 and place_y % 49 >= 1 and place_y % 49 <= 29:
                    if (game.is_legal(int(place_x/49)+1, int(place_y/49)+1)):
                        now_move = [int(place_x/49), int(place_y/49)]
                        game.play(int(place_x/49)+1, int(place_y/49)+1)
                        num_pass = 0
                if BO_LUOT.checkForInput((mx, my)):
                    if game.get_active_player() == stone.BLACK:
                        txt = "B"
                    else:
                        txt = "W"
                    bo_luot_text = f'{txt} bo luot'
                    Bo_Luot(game)
                    num_pass += 1
                if PLAY_BACK.checkForInput((mx, my)):
                    main_menu()
                if BO_CUOC.checkForInput((mx, my)):
                    surrender(SCREEN, game.get_active_player())
                print(game.score())

        pygame.display.update()


def options():
    pygame.display.set_caption("Go-Game")
    global BOT
    while True:
        SCREEN.fill((255, 255, 255))
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        BOT_1 = Button(image=None, pos=(330, 100),
                       text_input="RandomAgent", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        BOT_2 = Button(image=None, pos=(330, 220),
                       text_input="AlphaBetaPruningAgentLevel1", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        BOT_3 = Button(image=None, pos=(330, 340),
                       text_input="AlphaBetaPruningAgentLevel2", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        BOT_1.update(SCREEN)
        BOT_2.update(SCREEN)
        BOT_3.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BOT_1.checkForInput(MENU_MOUSE_POS):
                    BOT = 1
                    timer_option()
                if BOT_2.checkForInput(MENU_MOUSE_POS):
                    BOT = 2
                    timer_option()
                if BOT_3.checkForInput(MENU_MOUSE_POS):
                    BOT = 3
                    timer_option()
        pygame.display.update()


def timer_option():
    pygame.display.set_caption("Go-Game")
    global TIME
    while True:
        SCREEN.fill((255, 255, 255))
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        TIME_30p = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(330, 100),
                          text_input="30 Mininutes", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        TIME_60p = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(330, 220),
                          text_input="60 Mininutes", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        TIME_00p = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(330, 340),
                          text_input="unlimit Mininutes", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        TIME_30p.update(SCREEN)
        TIME_60p.update(SCREEN)
        TIME_00p.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TIME_30p.checkForInput(MENU_MOUSE_POS):
                    TIME = 30
                    main_menu()

                if TIME_60p.checkForInput(MENU_MOUSE_POS):
                    TIME = 60
                    main_menu()
                if TIME_00p.checkForInput(MENU_MOUSE_POS):
                    TIME = 0
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
