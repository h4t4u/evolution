import cell
import pygame 
import sys

pygame.init()

width = 1000
cell.width = width
height =1000
cell.height = height
scale = 1
dT = 20
sc = pygame.display.set_mode((int(width*scale), int(height)))
RED = (225, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127, 127)

cells = [cell.Cell(0, 0, 100, 20, 20, 0, 0, 0, 600, 200)]

while 1:
	sc.fill(WHITE)
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	n_c = 0
	n_p = 0
	feel_c_c = 0
	feel_c_p = 0
	feel_p_c = 0
	feel_p_p = 0
	for cell in cells:
		if cell.interaction > 0:
			n_p += 1
			feel_p_c += cell.feel_carni
			feel_p_p += cell.feel_pred
		else:
			n_c += 1
			feel_c_c += cell.feel_carni
			feel_c_p += cell.feel_pred
		child = cell.step(0.1)
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
		pygame.draw.circle(sc, COLOUR, (int((cell.x+int(width/2))*scale), int((cell.y+int(height/2))*scale)), int(cell.r*scale))
		pygame.draw.line(sc, GRAY,	[int((cell.x+int(width/2)-int(cell.m/2))*scale), int((cell.y+int(height/2))*scale)],
									[int((cell.x+int(width/2)+int(cell.m/2))*scale), int((cell.y+int(height/2))*scale)], 4 )
	if n_c == 0:
		n_c = 1
	if n_p == 0:
		n_p = 1
	print("carni: c", int(feel_c_c/n_c), "p", int(feel_c_c/n_c))
	print("preda: c", int(feel_p_c/n_p), "p", int(feel_p_p/n_p))
	pygame.display.update()

	pygame.time.delay(dT)