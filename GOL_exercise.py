#!/usr/bin/env python

    # # # # # # # # # # # # # # # # # # # # # # # 
    #   Conway's Game of Life                   #
    #                                           #
    #   Simulation of a two-dimensional         #
    #   Cellular Automaton. Several             #
    #   properties like window size             #
    #   and world variation can be changed      #
    #   in the config.txt file.                 #
    #                                           #
    #   For more information read the           #
    #   readme.txt!                             #
    #                                           #
    #   Author: Bruno Vermeulen                 #
    #   bruno_vermeulen2001@yahoo.com           #
    # # # # # # # # # # # # # # # # # # # # # # #

import re
import sys, os
import pygame
from pygame.locals import *

# definition of Boardmember
class Boardmember():

	def __init__(self, alive, column, row):
        	self.alive = alive
        	self.pos = (column, row)

	def getneighbours(self):
        	self.neighbours = 0
        	for j in (-1, 0, 1):
            		for i in (-1, 0, 1):
                		if cell[(self.pos[0]+i)%cells_x][(self.pos[1]+j)%cells_y].alive and (not (i == 0 and j == 0)):
                    			self.neighbours += 1

	def updatelife(self, prop):
        	if (str(self.neighbours) in prop[1]) and (self.alive == False):
            		self.alive = True
        	elif str(self.neighbours) not in prop[0]:
            		self.alive = False

	def plot_cell(self):
		if self.alive:
			color = yellow
		else:
			color = black
		pos_x = int(a_w_o[0] + (self.pos[0]+0.5)*cell_dim_x)
		pos_y = int(a_w_o[1] + (self.pos[1]+0.5)*cell_dim_y)
		pygame.draw.circle(screen,color,(pos_x,pos_y),radius,0)

# calculate the number of neighbours, then use properties to decide whether cell is alive or not  
def nextcycle(prop):
	for j in range(cells_y):
		for i in range(cells_x):
			cell[i][j].getneighbours()
			
	for j in range(cells_y):
		for i in range(cells_x):
			cell[i][j].updatelife(prop)
			cell[i][j].plot_cell()
def plot_grid():
	# draw vertical grid lines
	for x in range(a_tl[0]+cell_dim_x,a_tr[0],cell_dim_x):
		pygame.draw.lines(screen,grey,False,((x,a_tl[1]+1),(x,a_bl[1]-1)),lwidth)

	# draw horizontal grid lines
	for y in range(a_tl[1]+cell_dim_y,a_bl[1],cell_dim_y):
		pygame.draw.lines(screen,grey,False,((a_tl[0]+1,y),(a_tr[0]-1,y)),lwidth)

	# draw action window border - there are two color (blue and organge)
	pygame.draw.rect(screen, bcolor, pygame.Rect(r_action_window), 2*lwidth)

# if mounse is pressed in the action window then create cell is not alive and vice versa
def mouse_pressed(grid):
	if grid[0] < cells_x and grid[0] >= 0 and grid[1] < cells_y and grid[1] >= 0:
		cell[grid[0]][grid[1]].alive = not cell[grid[0]][grid[1]].alive
 		cell[grid[0]][grid[1]].plot_cell()
	grid = (99999,99999)
	return grid

# display number of life iterations and time in seconds in status window left	
def display_text(n, t):
	
	# display text only once a second
	if t%1000 < 100:
		
		tpos = (a_bl[0], int(a_bl[1] + text_y*0.25))

		text ='Game of Life. Life cylce is: ' + str(int(n)) + ' and elapsed time is ' + str(int(t/1000)) + ' seconds.'
		text_display = myfont.render(text, False, yellow)
		
		#clear the text surface
		pygame.draw.rect(screen, black, pygame.Rect(r_text_window), 0)

		#display text on surface
		screen.blit(text_display,tpos)

# save and load pattern file
def save_pattern():
	pfile = open(pattern_file,"w")
	for i in range(cells_x):
		for j in range(cells_y):
			if cell[i][j].alive:
				pfile.write(str(i)+" "+str(j) + "\n")
	pfile.close()

def load_pattern():
	pfile = open(pattern_file)
	for line in pfile:
		pos = line.split()
		pos[0] = int(pos[0])
		pos[1] = int(pos[1])
		if (pos[0] >= 0 and pos[0] < cells_x) and (pos[1] >= 0 and pos[1] < cells_y):
			cell[pos[0]][pos[1]].alive = True
			cell[pos[0]][pos[1]].plot_cell()
	pfile.close()

# read config file in 1st argument (otherwise default is data/config.txt). Optionally 2nd argument is 
# pattern file otherwise defined in config file
def read_config():
	global pattern_file, fps, cells_x, cells_y, cell_dim_x, cell_dim_y, survival, birth	
	if len(sys.argv) == 2:
		config_file = sys.argv[1]
	else:
		config_file = os.path.join("data","config.txt")

	cfile = open(config_file)

	pattern_file= cfile.readline()[17:]
	fps         = int(cfile.readline()[17:])
	cells_x     = int(cfile.readline()[17:])
	cells_y     = int(cfile.readline()[17:])
	cell_dim_x  = int(cfile.readline()[17:])
	cell_dim_y  = int(cfile.readline()[17:])
	survival    = cfile.readline()[17:].split()
	birth       = cfile.readline()[17:].split()

	if len(sys.argv) == 3:
		pattern_file= sys.argv[2]

	# remove return /r, new line /n or spaces /s from pattern_file
	pattern_file = re.sub(r'[\r\n\s]','',pattern_file)
	print pattern_file, fps, cells_x, cells_y, cell_dim_x, cell_dim_y, survival, birth

	cfile.close()

# main program
def main():

	# initialize and set parameters
	global myfont
	pygame.init()
	fpsClock = pygame.time.Clock()
	myfont = pygame.font.Font(None,22)

	read_config()
	
	# set some variables not defined in config file
	global black, blue, orange, yellow, grey, padding, lwidth, radius
	black	    = (0,0,0)
	blue        = (0,128,255)
	orange      = (255,100,0)
	yellow      = (255,255,0)
	grey        = (128,128,128)
	padding     = 5
	lwidth      = 1
	radius      = int(cell_dim_x/2)

	# set window boundaries
	global a_w_o, a_w_x, a_w_y, a_tl, a_tr, a_br, a_bl, r_action_window, r_text_window, text_x, text_y
	a_w_o = (padding , padding )
	a_w_x = cells_x*cell_dim_x 
	a_w_y = cells_y*cell_dim_y 

	a_tl = a_w_o
	a_tr = (a_w_o[0]+a_w_x,a_w_o[1])
	a_br = (a_w_o[0]+a_w_x,a_w_o[1]+a_w_y)
	a_bl = (a_w_o[0],a_w_o[1] + a_w_y)

	status_x    = 50
	status_y    = 38
	text_x      = a_w_x - status_x
	text_y      = status_x

#	action_window = (a_tl,a_tr,a_br,a_bl)
	r_action_window = (a_tl,(a_w_x,a_w_y))
	r_status_window = ((a_br[0]-status_x,a_br[1]+padding),(status_x,status_y))
	r_text_window   = ((a_bl[0], a_bl[1]+padding),(text_x, text_y))
	status_pos      = (int(a_br[0]-status_x),int(a_br[1]+padding-10))
	main_x          = padding*2 + a_w_x
	main_y          = padding + a_w_y + status_y

	# create 2D matrix containing boardmembers as cells
	global cell
	cell = [[Boardmember(False, x, y) for y in range(cells_y)] for x in range(cells_x)]

	global bcolor, total_time
	bcolor           = blue
	run              = True
	pause            = True
	dummy            = 0
	m                = (9999,9999)
	world_properties = (survival, birth)
	lifecycle        = 0
	time_counter     = 0
	print world_properties

	# set the screen, set caption of the main window and load icons for pause and run
	global screen
	screen = pygame.display.set_mode((main_x, main_y))
	pygame.display.set_caption('Game of Life')
	pause_SMB = pygame.image.load('data/Pause.png').convert_alpha()
	run_SMB   = pygame.image.load('data/Triangle.png').convert_alpha()

	# run indefinetaly while run is true
	display_text(0, 0)
	while run:
		if pause:
			# update status symbol to pause
			pygame.draw.rect(screen, black, pygame.Rect(r_status_window), 0)
			screen.blit(pause_SMB, status_pos)
			
			# if mouse is pressed inside action window update cell
			m = mouse_pressed(m)

			#plot grid
			plot_grid()
		else:
			#update status symbol to run
			pygame.draw.rect(screen, black, pygame.Rect(r_status_window), 0)
			screen.blit(run_SMB, status_pos)		
			
			#next cycle in Game of Life
			nextcycle(world_properties)
			lifecycle += 1

			# plot grid
			plot_grid()
	
			# if mouse is pressed inside action window update cell
			m = mouse_pressed(m)
 
		for event in pygame.event.get():
			if event.type == QUIT:                # stop running when Quit event type is triggered
				run = False
		
			if event.type == KEYDOWN:
				if event.key == K_b:          # b - change border to blue
					bcolor = blue
				elif event.key == K_o:        # o - change border to orange
					bcolor = orange
				elif event.key == K_ESCAPE:   # Escape - leave program
					run = False
				elif event.key == K_SPACE:    # Space - pause no actions possible
					pause = not pause
					m = (999,999)
				elif event.key == K_l:        # l - load pattern
					load_pattern()
				elif event.key == K_s:        # s - save pattern
					save_pattern()
				elif event.key == K_c:        # c - clear screen and pause
					pause = True
                    			for i in range(cells_x) :
                        			for j in range(cells_y) :
                        	    			cell[i][j].alive = False
							cell[i][j].plot_cell()
					plot_grid()
					lifecycle = 0
								
			elif event.type == MOUSEBUTTONUP:     # if mouse if pressed calculated the cell indices
              			m = pygame.mouse.get_pos()
				m = [int((m[0]-a_w_o[0])/cell_dim_x),int((m[1]-a_w_o[1])/cell_dim_y)]

		pygame.display.flip()
		fpsClock.tick(fps)
	        
		time = pygame.time.get_ticks()
		display_text(lifecycle, time)

	pygame.quit()
	sys.exit

if __name__ == "__main__" :
    main()


