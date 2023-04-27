import sente
import pygame
import pyautogui

color = (255,255,255)
position = (0,0)

# CREATING CANVAS
canvas = pygame.display.set_mode((600,450))

# TITLE OF CANVAS
pygame.display.set_caption("Go-Game")

image = pygame.image.load("/home/bieenr/Downloads/go_game/go-game_test/go_game_9x9.png")

black_image_chessman = pygame.image.load("/home/bieenr/Downloads/go_game/go-game_test/black.png")
white_image_chessman = pygame.image.load("/home/bieenr/Downloads/go_game/go-game_test/white.png")
exit = False

pygame.init()

#Button
font = pygame.font.SysFont('Arial', 20)
objects = []
class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#999999',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

        objects.append(self)

    def process(self):

        mousePos = pygame.mouse.get_pos()
        
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        canvas.blit(self.buttonSurface, self.buttonRect)





n = 9
game = sente.Game(n)


def myFunction():
    print('Button Pressed')

def Bo_Luot():
    game.pss()
    print('Bo Luoted')
# print(game.__dir__())
# print(game.get_board().__dir__())
# print(dir(game.get_board().get_stone(1,1)))
    
customButton = Button(470, 30 , 120, 80, 'Bo luot', Bo_Luot)
customButton = Button(470, 130 , 120, 80, 'Bo cuoc', myFunction)
# customButton = Button(30, 140, 400, 100, 'Button Two (multiPress)', myFunction, True)
Diem = font.render('Some Text', False, (0, 0, 0))

print("-1")
while not exit:
	if (game.is_over() == True) :
		print(game.score())
		print(game.get_result())
		print(game.get_winner())
		break
	mx,my=pygame.mouse.get_pos()
	if(game.get_active_player() == sente.stone.BLACK) :
		image_virtual = black_image_chessman
	elif (game.get_active_player() == sente.stone.WHITE) :
		image_virtual = white_image_chessman

	canvas.fill(color)
	canvas.blit(image,dest = position)
	canvas.blit(image_virtual,(mx-16,my-16))

	#hien thi button
	for object in objects:
		object.process()

	#hien thi diem
	canvas.blit(Diem,(480,240))
	for i in range(n):
		for j in range(n):
			if(game.get_board().get_stone(i+1,j+1) == sente.stone.BLACK):
				canvas.blit(black_image_chessman,((i)*49+15,(j)*49+15))
			elif(game.get_board().get_stone(i+1,j+1) == sente.stone.WHITE):
				canvas.blit(white_image_chessman,((i)*49+15,(j)*49+15))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit = True
		elif event.type == pygame.MOUSEBUTTONUP :
			exit = False
		elif event.type == pygame.MOUSEBUTTONDOWN :
			place_x = mx - 16
			place_y = my - 16
			# print(place_x,place_y)
			if place_x%49 >=1 and place_x%49 <= 29  and place_y %49 >= 1 and place_y%49 <=29:
				if(game.is_legal(int(place_x/49)+1,int(place_y/49)+1)):					
					game.play(int(place_x/49)+1,int(place_y/49)+1)
					

	pygame.display.update()




