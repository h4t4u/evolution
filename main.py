import cell
import pygame 
import sys

pygame.init()

width = 4000
height =4000
cell.width = width
cell.height = height
scale = 0.25
dT = 20
sc = pygame.display.set_mode((int(width*scale), int(height*scale)))

RED = (225, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127, 127)

cells = [cell.Cell(0, 0, 100, 0, 60, 0, 0, 0, 2000, 300, 0.5)]

while 1:
	sc.fill(WHITE)
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	part = 0
	n_h = 0
	n_p = 0
	feel_h_h = 0
	feel_h_p = 0
	feel_p_h = 0
	feel_p_p = 0
	for cell in cells:
		part += cell.part
		if cell.interaction > 0:
			n_p += 1
			feel_p_h += cell.feel_herb
			feel_p_p += cell.feel_pred
		else:
			n_h += 1
			feel_h_h += cell.feel_herb
			feel_h_p += cell.feel_pred
		child = cell.step(0.1)
		for cell2 in cells:
			if cell2 != cell:
				cell.interact(cell2)
		if child == -1:
			cells.remove(cell)
			continue
		if child != None:
			cells.append(child)
			if cell.m <= 1:
				cells.remove(cell)
		COLOUR = GREEN
		if cell.interaction > 0:
			COLOUR = RED
		pygame.draw.circle(sc, COLOUR, (int((cell.x + int(width/2)) * scale), int((cell.y + int(height1.5*/2)) * scale)), int(cell.r * scale))
		pygame.draw.line(sc, GRAY,	[int((cell.x + int(width/2) - int(cell.m/2)) * scale), int((cell.y + int(height/2)) * scale)],
									[int((cell.x + int(width/2) + int(cell.m/2)) * scale), int((cell.y + int(height/2)) * scale)], 2 )
	if n_h == 0:
		n_h = 1
	if n_p == 0:
		n_p = 1
	print("herb: h", int(feel_h_h/n_h), "p", int(feel_h_p/n_h))
	print("pred: h", int(feel_p_h/n_p), "p", int(feel_p_p/n_p))
	pygame.display.update()
	if len(cells) == 0:
		break
	pygame.time.delay(dT)