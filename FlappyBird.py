"""

WELCOME TO FLAPPY BIRD!!

JUMP THROUGH THE GAPS IN THE PIPES AND DONT CRASH

TRY AND GET THE HIGHEST SCORE POSSIBLE

TOGGLE DIFFERENT GAME MODES ON/OFF IN THE SETTINGS SECTION

"""

#Imports/initiation
import pygame
import random as ran
import tkinter as tk
pygame.font.init()
pygame.init()


#COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 225, 50)
RED = (255, 0, 0)
DARK_GREEN = (0, 175, 0)
GREY = (128, 128, 128)

#GAME SETTINGS----------------
FPS = 60 

SPEED = False	#speed up game at n pipes
RATE_ACCEL = 10

PRECISION = False	#shrink pipe gaps by n pixels
RATE_SHRINK = 5

LOW_GRAV = False

DONT_ROTATE = False

PIPE_GAP = 175	#starting pipe gap
VEL = 7	#starting velocity

JUMP_HEIGHT = 80 	#max addition to height on single jump
FRAMES_JUMP = int(FPS*0.5) 	#number of frames it takes to return back to initial height

GAMEOVER_DELAY = 1500
HIGH_SCORE = 0
##-----------------------------------

VEL = (60/FPS) * VEL

if LOW_GRAV:
	PIPE_GAP = 250
	JUMP_HEIGHT = 150
	FRAMES_JUMP = int(FPS)

#formula to determine gravitational acceleration based on jump height and frames per jump
ACCEL = -JUMP_HEIGHT/((1-FRAMES_JUMP)-(1-(FRAMES_JUMP/2))**2) #(JUMP_HEIGHT)/(((FPS)**2)/4)
		#JUMP_EQN--> ACCEL * x * (x-FRAMES_JUMP) -ACCEL * (x-FPS//2)**2 + JUMP_HEIGHT

#COLLISION WITH PIPE EVENT
HIT_PIPE = pygame.USEREVENT + 1

#FONT INITIALISING
GAMEOVER_FONT = pygame.font.SysFont('comicsans', 100)
FINAL_SCORE_FONT = pygame.font.SysFont('comicsans', 70)
SCORE_FONT = pygame.font.SysFont('comicsans', 40)
SETTINGS_FONT = pygame.font.SysFont('comicsans', 50)
OPTIONS_FONT = pygame.font.SysFont('comicsans', 30)
#	RESTART_FONT = pygame.font.SysFont('comicsans', 50)

#WINDOW DIMENSIONS
WIDTH, HEIGHT = 900, 500

#GRASS HEIGHT
GRASS_HEIGHT = 30

#BIRD DIMENSIONS/STARTING POSITION
BIRD_WIDTH, BIRD_HEIGHT = 50, 40
BIRDX, BIRDY = WIDTH//4, HEIGHT//2

#PIPE WIDTH/MINIMUM HEIGHT/
#	SPACING BETWEEN PIPES(FACTOR OF PIPE WIDTH)--WILL BREAK LOWER THAN 3
PIPE_WIDTH = 75
PIPE_MIN = 50
SPACE_BW_PIPES = PIPE_WIDTH * 3

#TOP/BOTTOM PIPE STARTING POSITIONS
TOP_PIPE_START_X = WIDTH
TOP_PIPE_START_Y = 0
BOTTOM_PIPE_START_X = WIDTH
BOTTOM_PIPE_END_Y = HEIGHT

#CREATE WINDOW, SET WINDOW CAPTION
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

#CREATE GRASS RECTANGLE
GRASS = pygame.Rect(0, HEIGHT-GRASS_HEIGHT, WIDTH, HEIGHT)

#For Mac
"""
#IMPORT BIRD PNG, SCALE IT, CREATE COPIES WHERE IT TILTS UP AND TILTS DOWN, BY 30 DEGREES
BIRD = pygame.transform.scale(pygame.image.load('/Users/robertmcpherson/Documents/Coding/Python/Pygame/FlappyBird/Bird.png'), (BIRD_WIDTH, BIRD_HEIGHT))
BIRD_UP = pygame.transform.rotate(BIRD, 30)
BIRD_DOWN = pygame.transform.rotate(BIRD, 360-30)
BIRD_HALF_UP = pygame.transform.rotate(BIRD, 15)
BIRD_HALF_DOWN = pygame.transform.rotate(BIRD, 360-15)

#IMPORT SKY JPEG AND SCALE TO SIZE OF WINDOW
SKY = pygame.transform.scale(pygame.image.load('/Users/robertmcpherson/Documents/Coding/Python/Pygame/FlappyBird/Sky.jpeg'), (WIDTH, HEIGHT))

#IMPORT GEAR ICON and scale
GEAR_SIDES = 40
GEAR_PADDING = 10
GEAR = pygame.transform.scale(pygame.image.load('/Users/robertmcpherson/Documents/Coding/Python/Pygame/FlappyBird/Gear.png'), (GEAR_SIDES, GEAR_SIDES))

"""
#For Windows
#IMPORT BIRD PNG, SCALE IT, CREATE COPIES WHERE IT TILTS UP AND TILTS DOWN, BY 30 DEGREES
BIRD = pygame.transform.scale(pygame.image.load(r"C:\Users\rober\OneDrive\STEM\VSCodeProjects\Python\Pygame\FlappyBird\Bird.png"), (BIRD_WIDTH, BIRD_HEIGHT))
BIRD_UP = pygame.transform.rotate(BIRD, 30)
BIRD_DOWN = pygame.transform.rotate(BIRD, 360-30)
BIRD_HALF_UP = pygame.transform.rotate(BIRD, 15)
BIRD_HALF_DOWN = pygame.transform.rotate(BIRD, 360-15)

#IMPORT SKY JPEG AND SCALE TO SIZE OF WINDOW
SKY = pygame.transform.scale(pygame.image.load(r'C:\Users\rober\OneDrive\STEM\VSCodeProjects\Python\Pygame\FlappyBird\Sky.jpeg'), (WIDTH, HEIGHT))

#IMPORT GEAR ICON and scale
GEAR_SIDES = 40
GEAR_PADDING = 10
GEAR = pygame.transform.scale(pygame.image.load(r'C:\Users\rober\OneDrive\STEM\VSCodeProjects\Python\Pygame\FlappyBird\Gear.png'), (GEAR_SIDES, GEAR_SIDES))


BUTTON_WIDTH, BUTTON_HEIGHT = 100, 60 

ACCEL_ONOFF_X, ACCEL_ONOFF_Y = int(WIDTH*0.25-(BUTTON_WIDTH/2)), int(HEIGHT*0.45 -(BUTTON_HEIGHT/2))
PRECISE_ONOFF_X, PRECISE_ONOFF_Y = int(WIDTH*0.75-(BUTTON_WIDTH/2)), int(HEIGHT*0.45 -(BUTTON_HEIGHT/2))
# GRAV_ONOFF_X, GRAV_ONOFF_Y = int(WIDTH*0.5-(BUTTON_WIDTH/2)), int(HEIGHT*0.45 -(BUTTON_HEIGHT/2))


def draw_settings(SETTINGS, title_text, gamemodes_text, speed_text, precise_text, \
	accel_onoff, precise_onoff, accel_onoff_text, precise_onoff_text, rate_accel_text, \
	rate_shrink_text, gap_text, vel_text):#, grav_text, grav_onoff, grav_onoff_text):

	SETTINGS.fill(GREY)
	SETTINGS.blit(GEAR, (WIDTH-GEAR_SIDES - GEAR_PADDING, GEAR_PADDING))

	
	SETTINGS.blit(title_text, ((WIDTH/2 - title_text.get_width()/2), 20))	
	SETTINGS.blit(gamemodes_text, ((WIDTH/2 - gamemodes_text.get_width()/2), 20 + title_text.get_height()*2.5))
	SETTINGS.blit(speed_text, ((int(WIDTH*0.25) - speed_text.get_width()/2), int(HEIGHT*0.3)))
	SETTINGS.blit(precise_text, ((int(WIDTH*0.75) - precise_text.get_width()/2), int(HEIGHT*0.3)))
	#SETTINGS.blit(grav_text, (int(WIDTH*0.5)-grav_text.get_width()/2, int(HEIGHT*0.3)))

	pygame.draw.rect(WIN, WHITE, accel_onoff)
	pygame.draw.rect(WIN, WHITE, precise_onoff)
	#pygame.draw.rect(WIN, WHITE, grav_onoff)

	SETTINGS.blit(accel_onoff_text, (int((ACCEL_ONOFF_X + BUTTON_WIDTH/2) - accel_onoff_text.get_width()/2), int((ACCEL_ONOFF_Y + BUTTON_HEIGHT/2) - accel_onoff_text.get_height()/2)))	
	SETTINGS.blit(precise_onoff_text, (int((PRECISE_ONOFF_X + BUTTON_WIDTH/2) - precise_onoff_text.get_width()/2), int((PRECISE_ONOFF_Y + BUTTON_HEIGHT/2) - precise_onoff_text.get_height()/2)))	
	#SETTINGS.blit(grav_onoff_text, (int((GRAV_ONOFF_X + BUTTON_WIDTH/2) - grav_onoff_text.get_width()/2), int((GRAV_ONOFF_Y + BUTTON_HEIGHT/2) - grav_onoff_text.get_height()/2)))	
		

	pygame.display.update()

def settings():
	clock = pygame.time.Clock()
	SETTINGS = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Settings")

	title_text = SETTINGS_FONT.render("SETTINGS", 1, BLACK)
	gamemodes_text = OPTIONS_FONT.render("GAME MODES", 1, BLACK)
	speed_text = OPTIONS_FONT.render("ACCELERATION MODE", 1, BLACK)
	precise_text = OPTIONS_FONT.render("PRECISION MODE", 1, BLACK)
	rate_accel_text = OPTIONS_FONT.render("Rate of Acceleration", 1, BLACK)
	rate_shrink_text = OPTIONS_FONT.render("Rate of Shrinking", 1, BLACK)
	gap_text = OPTIONS_FONT.render("Starting Gaps", 1, BLACK)
	vel_text = OPTIONS_FONT.render("Starting Velocity", 1, BLACK)
	#grav_text = OPTIONS_FONT.render("LOW GRAVITY", 1, BLACK)

	accel_onoff = pygame.Rect(ACCEL_ONOFF_X, ACCEL_ONOFF_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
	precise_onoff = pygame.Rect(PRECISE_ONOFF_X, ACCEL_ONOFF_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
	# grav_onoff = pygame.Rect(WIDTH/2-BUTTON_WIDTH/2, ACCEL_ONOFF_Y, BUTTON_WIDTH, BUTTON_HEIGHT)

	running = True
	while running:
	
		global SPEED
		global PRECISION
		global LOW_GRAV
		if SPEED:
			a_text = "ON"
		else:
			a_text = "OFF"
		if PRECISION:
			p_text = "ON"
		else:
			p_text = "OFF"
		# if LOW_GRAV:
		# 	g_text = "ON"
		# else:
		# 	g_text = "OFF"
		accel_onoff_text = SETTINGS_FONT.render(a_text, 1, BLACK)
		precise_onoff_text = SETTINGS_FONT.render(p_text, 1, BLACK)
		# grav_onoff_text = SETTINGS_FONT.render(g_text, 1, BLACK)

		for event in pygame.event.get():
			if event.type == pygame.QUIT: 	#needed in order to quit program
				running = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse = pygame.mouse.get_pos()
				if WIDTH-GEAR_PADDING >= mouse[0] >= WIDTH-GEAR_SIDES-GEAR_PADDING and GEAR_PADDING <= mouse[1] <= (GEAR_PADDING + GEAR_SIDES):
					running = False
				elif ACCEL_ONOFF_X <= mouse[0] <= (ACCEL_ONOFF_X + BUTTON_WIDTH)  and ACCEL_ONOFF_Y <= mouse[1] <= (ACCEL_ONOFF_Y + BUTTON_HEIGHT):
					#global SPEED
					if SPEED:
						SPEED = False
					else:
						SPEED = True
				elif PRECISE_ONOFF_X <= mouse[0] <= (PRECISE_ONOFF_X + BUTTON_WIDTH)  and PRECISE_ONOFF_Y <= mouse[1] <= (PRECISE_ONOFF_Y + BUTTON_HEIGHT):
					#global PRECISION
					if PRECISION:
						PRECISION = False
					else:
						PRECISION = True
				# elif GRAV_ONOFF_X <= mouse[0] <= (GRAV_ONOFF_X + BUTTON_WIDTH)  and GRAV_ONOFF_Y <= mouse[1] <= (GRAV_ONOFF_Y + BUTTON_HEIGHT):
				# 	#global PRECISION
				# 	if LOW_GRAV:
				# 		LOW_GRAV = False
				# 	else:
				# 		LOW_GRAV = True
		draw_settings(SETTINGS, title_text, gamemodes_text, speed_text, precise_text, \
			accel_onoff, precise_onoff, accel_onoff_text, precise_onoff_text, rate_accel_text, \
			rate_shrink_text, gap_text, vel_text)#, grav_text, grav_onoff, grav_onoff_text)


#DRAWS WINDOW
def draw_window(bird, IMAGE, top_pipes, bottom_pipes, points):
	WIN.blit(SKY, (0, 0))
	
	for pipe in top_pipes:
		pygame.draw.rect(WIN, GREEN, pipe)

	for pipe in bottom_pipes:
		pygame.draw.rect(WIN, GREEN, pipe)

	pygame.draw.rect(WIN, DARK_GREEN, GRASS)

	score_text = SCORE_FONT.render("SCORE: " + str(points), 1, BLACK)
	WIN.blit(score_text, (10, 10))

	highscore_text = SCORE_FONT.render("HIGHSCORE: " + str(HIGH_SCORE), 1, BLACK)
	WIN.blit(highscore_text, (50 + score_text.get_width(), 10))

	WIN.blit(IMAGE, (bird.x, bird.y))
	WIN.blit(GEAR, (WIDTH-GEAR_SIDES - GEAR_PADDING, GEAR_PADDING))

	pygame.display.update()

#HANDLES JUMPING PHYSICS 
def jump(bird, jump_start_y, x):
		bird.y = jump_start_y + (ACCEL * x * (x-FRAMES_JUMP))#((1/3) * x *(x - FPS//2))#ACCEL * (x-FPS//2)**2 - JUMP_HEIGHT#((1/3) * x *(x - FPS//2))#

#DISPLAYS GAMEOVER TEXT (EXTRA COMMENTS ARE POSSIBLE FUTURE ADDITIONS)
def draw_gameover(points):
	draw_text = GAMEOVER_FONT.render("GAME OVER", 1, RED)
		# draw_restart = RESTART_FONT.render("Press R to Restart", 1, BLACK)
	WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
	global HIGH_SCORE
	if points> HIGH_SCORE:
		HIGH_SCORE = points
		draw_highscore = FINAL_SCORE_FONT.render("NEW HIGH SCORE: " + str(points), 1, BLACK)
		WIN.blit(draw_highscore, (WIDTH/2-draw_highscore.get_width()/2, HEIGHT/2 + draw_highscore.get_height() - draw_highscore.get_height()/2+20))
	else:
		draw_score = FINAL_SCORE_FONT.render("SCORE: " + str(points), 1, BLACK)
		WIN.blit(draw_score, (WIDTH/2-draw_score.get_width()/2, HEIGHT/2 + draw_text.get_height() - draw_score.get_height()/2+20))
		# WIN.blit(draw_restart, (WIDTH/2-draw_restart.get_width()/2, HEIGHT//4 * 3)) 
	pygame.display.update()
	pygame.time.delay(GAMEOVER_DELAY)

#MOVES ALL PIPES TO THE LEFT, DETECTS COLLISION WITH BIRD, REMOVES PIPES OFF LEFT SIDE OF SCREEN
def handle_pipes(top_pipes, bottom_pipes, bird, vel, pipe_gap):
	for pipe in top_pipes:
		pipe.x -= vel
		if bird.colliderect(pipe):
			pygame.event.post(pygame.event.Event(HIT_PIPE))
		if (pipe.x + PIPE_WIDTH) < 0:
			top_pipes.remove(pipe)

	for pipe in bottom_pipes:
		pipe.x -= vel
		if bird.colliderect(pipe):
			pygame.event.post(pygame.event.Event(HIT_PIPE))
		if (pipe.x + PIPE_WIDTH) < 0:
			bottom_pipes.remove(pipe)

	if (top_pipes[-1].x + PIPE_WIDTH) < WIDTH - (SPACE_BW_PIPES):
		top_pipe_height = ran.randint(PIPE_MIN, (HEIGHT-PIPE_MIN-pipe_gap))

		top_pipes.append(pygame.Rect(\
			TOP_PIPE_START_X, TOP_PIPE_START_Y, PIPE_WIDTH, top_pipe_height))
		bottom_pipes.append(pygame.Rect(\
			BOTTOM_PIPE_START_X, top_pipe_height + pipe_gap, PIPE_WIDTH, BOTTOM_PIPE_END_Y))

#MAIN FUNCTION FOR GAMEPLAY
def main():
	#sets variable to PIPE_GAP constant
	pipe_gap = PIPE_GAP

	#create bird surface
	bird = pygame.Rect(BIRDX, BIRDY, BIRD_WIDTH, BIRD_HEIGHT)
	
	#created random pipe height
	top_pipe_height = ran.randint(PIPE_MIN, (HEIGHT-PIPE_MIN-pipe_gap))

	#create lists for top/bottom pipes, store first pipe in each
	top_pipes = [pygame.Rect(TOP_PIPE_START_X, TOP_PIPE_START_Y, PIPE_WIDTH, top_pipe_height)]
	bottom_pipes = [pygame.Rect(BOTTOM_PIPE_START_X, top_pipe_height + pipe_gap, PIPE_WIDTH, BOTTOM_PIPE_END_Y)]

	#create clock object
	clock = pygame.time.Clock()
	
	running = True	#sentinel for game loop
	start_game = False	#variable for when actual game starts

	x  = 0 	#keeps track of frames during jump
	points = 0 	#points variable
	vel = VEL	#sets variable to VEL constant
	jump_start_y = bird.y 	#sets variable to starting bird y
							#keeps track of where bird started its jump
	
	#main gameloop
	while running:
		#set frame per second
		clock.tick(FPS)

		#check for events, quit, space, hit pipe
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 	#needed in order to quit program
				running = False
				pygame.quit()
				exit()

			if event.type == pygame.KEYDOWN: 	#if the event is a keypress
				if event.key == pygame.K_SPACE or event.key == pygame.K_UP: 	#on spacebar press, start bird jump
					x = 1
					start_game = True
					jump_start_y = bird.y
					
				# if event.key == pygame.K_r:
				# 	main()

			if event.type == HIT_PIPE and start_game: 	#show gameover screen and exit loop on hit pipe
				#if points > 0:
				draw_gameover(points)#, points)#\n SCORE: " + str(points))
				running = False

			if event.type == pygame.MOUSEBUTTONDOWN and not(start_game):
				mouse = pygame.mouse.get_pos()
				if WIDTH-GEAR_PADDING >= mouse[0] >= WIDTH-GEAR_SIDES-GEAR_PADDING and GEAR_PADDING <= mouse[1] <= GEAR_PADDING + GEAR_SIDES:
					settings() 
			 		#print(SPEED)

		# if bird exits game area(too high/low), gameover screen and exit gameloop
		if(bird.y+BIRD_HEIGHT) > (HEIGHT - GRASS_HEIGHT) or (bird.y + BIRD_HEIGHT) < 0:
			draw_gameover(points)#, points)#\n SCORE: " + str(points))
			running = False

		#updates bird position if x > 0
		if x > 0:
			jump(bird, jump_start_y, x)
			x += 1

		#Handles what image to show for bird for different parts of motion
		parabola = ACCEL * x * (x-FRAMES_JUMP)#((1/3) * x *(x - FPS//2))#ACCEL * (x-FPS//2)**2 - JUMP_HEIGHT#((1/2) * x *(x - FPS//2))
			#NOTE Y VALUES ARE REVERSED(FURTHER UP == LOWER VALUE)
		if DONT_ROTATE:
			IMAGE = BIRD
		elif parabola == 0: 	#standard image for added height equals zero
			IMAGE = BIRD 
		elif parabola < 0 and (x < FRAMES_JUMP * 0.5): 	#facing up image for any added height 
			IMAGE = BIRD_UP
		elif parabola < 0 and (x < FRAMES_JUMP * 0.75):
			IMAGE = BIRD_HALF_UP
		elif parabola > 20: 	#facing down image for any negative height below 40
			IMAGE = BIRD_HALF_DOWN
		elif parabola > 40:
			IMAGE = BIRD_DOWN
		else:
			IMAGE = BIRD 	#standard image for anything else(0 to -40)

		#if len(top_pipes)>1:
		#if the bird enters a section just after a pipe the points increases
		if bird.x > (top_pipes[0].x + PIPE_WIDTH) and bird.x <= (top_pipes[0].x + PIPE_WIDTH + vel):
			points += 1

				#if Speed mode is on and the number of points is a multiple of rate accel, velocity increases
			if SPEED and (points % RATE_ACCEL == 0): 
				vel += 1
				#if precision mode is on and pipe gap is greater than 100, the pipe gap shrinks
			if PRECISION and PIPE_GAP > 100: 	#
				pipe_gap -= RATE_SHRINK
	
			#if the start_game variable is true, the pipes will start moving
		if start_game:
			handle_pipes(top_pipes, bottom_pipes, bird, vel, pipe_gap)
	
			#call draw_window function
		draw_window(bird, IMAGE, top_pipes, bottom_pipes, points)


	main()#restarts main function if gameloop is exited

#random stuff to include at end that i dont understand
if __name__ == "__main__":
	main()