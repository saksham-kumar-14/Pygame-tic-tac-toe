import pygame, sys, time

pygame.init()
pygame.font.init()
pygame.display.set_caption("Tic Tac Toe")

WIDTH, HEIGHT = 1000,800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

FONT = pygame.font.SysFont('Comic Sans MS', 100)
BNT_FONT = pygame.font.SysFont('Comic Sans MS', 40)

WINNING_PLAYER = None
FPS = 60
CLOCK = pygame.time.Clock()

def draw_grid(grid):
	start_coordinate = [WIDTH//3,0]
	end_coordinate = [WIDTH//3, HEIGHT]
	
	# vertical display
	for i in range(2):
		pygame.draw.line(SCREEN, (255,255,255), start_coordinate, end_coordinate, 2)
		start_coordinate[0] += WIDTH//3
		end_coordinate[0] += WIDTH//3

	start_coordinate = [0,HEIGHT//3]
	end_coordinate = [WIDTH, HEIGHT//3]
	
	# horizontal display
	for i in range(2):
		pygame.draw.line(SCREEN, (255,255,255), start_coordinate, end_coordinate, 2)
		start_coordinate[1] += HEIGHT//3
		end_coordinate[1] += HEIGHT//3

	current_coordinate = [0,0]
	for i in grid:
		for j in i:
			item = FONT.render(j, True, (255,255,255))
			x = current_coordinate[0] + (WIDTH//3 - item.get_width())//2
			y = current_coordinate[1] + (HEIGHT//3 - item.get_height())//2
			SCREEN.blit(item, [ x, y] )
			current_coordinate[0] += WIDTH//3
		current_coordinate[0] = 0
		current_coordinate[1] +=  HEIGHT//3

def progress_game(Xchance, grid):
	pos = pygame.mouse.get_pos()
	clicked = pygame.mouse.get_pressed()

	start = [0,0]
	end = [WIDTH//3, HEIGHT//3]
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if end[0]>pos[0]>start[0] and end[1]>pos[1]>start[1] and True in clicked and grid[i][j]=="":
				if Xchance:
					grid[i][j] = "X"
				else:
					grid[i][j] = "O"
				Xchance = not Xchance
			start[0] = end[0]
			end[0] += WIDTH//3
		start[0] = 0
		start[1] += HEIGHT//3
		end[0] = WIDTH//3
		end[1] += HEIGHT//3

	return [grid, Xchance]


def check_draw(grid):
	for i in grid:
		for j in i:
			if j == "":
				return [False, None]

	return [True, "draw"]


def check_result(grid):
	if grid[0][0] == grid[0][1] == grid[0][2] and grid[0][0]!="":
		return [True, grid[0][0]]
	if grid[1][0] == grid[1][1] == grid[1][2] and grid[1][0]!="":
		return [True, grid[1][0]]
	if grid[2][0] == grid[2][1] == grid[2][2] and grid[2][0]!="":
		return [True, grid[2][0]]
	if grid[0][0] == grid[1][0] == grid[2][0] and grid[0][0]!="":
		return [True, grid[0][0]]
	if grid[0][1] == grid[1][1] == grid[2][1] and grid[0][1]!="":
		return [True, grid[0][1]]
	if grid[0][2] == grid[1][2] == grid[2][2] and grid[0][2]!="":
		return [True, grid[0][2]]
	if grid[0][0] == grid[1][1] == grid[2][2] and grid[0][0]!="":
		return [True, grid[0][0]]
	if grid[0][2] == grid[1][1]== grid[2][0] and grid[0][2]!="":
		return [True, grid[0][2]]

	return check_draw(grid)


def run():
	global WINNING_PLAYER
	grid = [ ["","",""], ["","",""], ["","",""] ]
	Xchance = True
	game_over = False
	
	while not game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
				pygame.quit()
				sys.exit()


		temp = progress_game(Xchance, grid)
		grid = temp[0]
		Xchance = temp[1]
		result = check_result(grid)
		game_over = result[0]
		WINNING_PLAYER = result[1]


		SCREEN.fill((0,0,0))
		draw_grid(grid)

		
		CLOCK.tick(FPS)
		pygame.display.update()


def game_over_screen():

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
				pygame.quit()
				sys.exit()

		if WINNING_PLAYER == "draw":
			game_over_text = FONT.render("Draw!!", True, (255, 165, 0))
		else:
			game_over_text = FONT.render(f"Player {WINNING_PLAYER} has won!", True, (255,165,0))

		btn_width, btn_height = 200,100
		restart_btn_x, end_btn_x = (WIDTH//4)-(btn_width//2) , ((3*WIDTH)//4)-(btn_width//2)
		btn_y = (HEIGHT//2)+100
		restart_btn = pygame.Rect(restart_btn_x, btn_y, btn_width, btn_height)
		end_btn = pygame.Rect(end_btn_x, btn_y, btn_width, btn_height)

		restart_btn_color = (0,255,0)
		end_btn_color = (255,0,0)

		pos = pygame.mouse.get_pos()
		clicked = pygame.mouse.get_pressed()

		if restart_btn_x+btn_width>pos[0]>restart_btn_x and btn_y+btn_height>pos[1]>btn_y:
			restart_btn_color = (0,155,0)
			if True in clicked:
				break
		elif end_btn_x+btn_width>pos[0]>end_btn_x and btn_y+btn_height>pos[1]>btn_y:
			end_btn_color = (155,0,0)
			if True in clicked:
				pygame.quit()
				sys.exit()

		SCREEN.fill((0,0,0))
		game_over_text_x = (WIDTH - game_over_text.get_width())//2
		SCREEN.blit(game_over_text, (game_over_text_x ,HEIGHT//3))
		pygame.draw.rect(SCREEN, restart_btn_color, restart_btn)
		pygame.draw.rect(SCREEN, end_btn_color, end_btn)

		restart_btn_text = BNT_FONT.render("Restart",True,(255,255,255))
		end_btn_text = BNT_FONT.render("Exit",True,(255,255,255))

		restart_btn_text_x= restart_btn_x + (btn_width-restart_btn_text.get_width())//2
		restart_btn_text_y = btn_y + (btn_height-restart_btn_text.get_height())//2
		end_btn_text_x= end_btn_x + (btn_width-end_btn_text.get_width())//2
		end_btn_text_y = btn_y + (btn_height-end_btn_text.get_height())//2

		SCREEN.blit(restart_btn_text, (restart_btn_text_x, restart_btn_text_y))
		SCREEN.blit(end_btn_text, (end_btn_text_x, end_btn_text_y))


		CLOCK.tick(FPS)
		pygame.display.update()



if __name__ == '__main__':
	while True:
		run()
		time.sleep(1)
		game_over_screen()
		time.sleep(1)