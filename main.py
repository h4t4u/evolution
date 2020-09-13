import cell
import pygame 
import sys

pygame.init()

width = 1000
height =1000
dT = 20
sc = pygame.display.set_mode((width, height))
RED = (225, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127, 127)

cells = [cell.Cell(0,10,30,30,30, 0, 600, 200)]

while 1:
	sc.fill(WHITE)
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	m = 0
	v = 0
	interaction = 0
	n = 0
	for cell in cells:
		if cell.interaction > 0:
			v+=abs(cell.v)
			interaction+=cell.interaction
			n+=1
		m+=cell.m
		child = cell.step(dT/100)
		for cell2 in cells:
			if cell2 != cell:
				cell.interact(cell2)
		if child == -1:
			cells.remove(cell)
			continue
		if child != None:
			cells.append(child)
			if cell.m<=1:
				cells.remove(cell)
		COLOUR = GREEN
		if cell.interaction > 0:
			COLOUR = RED
		#if m>=2000:
		#	dT = 1000
		pygame.draw.circle(sc, COLOUR, (cell.x+int(width/2), cell.y+int(height/2)), cell.r)
		pygame.draw.line(sc, GRAY,[cell.x+int(width/2)-int(cell.m/2), cell.y+int(height/2)], [cell.x+int(width/2)+int(cell.m/2), cell.y+int(height/2)], 4 )
	if n ==0:
		n =1
	print(m, len(cells), v/n, interaction/n)
	pygame.display.update()

	pygame.time.delay(dT)