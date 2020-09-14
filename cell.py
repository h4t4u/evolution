import random
import math
width = 10
height = 10

class Cell:
	def __init__(self, x, y, v, angle, r, interaction, feel_carni, feel_pred, m, limit):
		self.x = x
		self.y = y
		self.v = v
		self.angle = angle
		if r < 5:
			r = 5
		self.r = r
		self.interaction = interaction
		self.m = m
		self.limit = limit
		self.feel_carni = feel_carni
		self.feel_pred = feel_pred
		self.sr=0

	def create(self, part):
		angle = random.randint(0,360)
		r = int(abs(self.r+random.gauss(0,2)))
		return Cell(int(self.x+(self.r+r)*1.5*math.cos(angle*3.14/180)), int(self.y+(self.r+r)*1.5*math.sin(angle*3.14/180)), self.v+random.gauss(0,5),
					self.angle+random.gauss(0,5), r, self.interaction+random.gauss(0,10),
					self.feel_carni+random.gauss(0,10), self.feel_pred+random.gauss(0,5), int(self.m*part), self.limit+random.gauss(0,10))

	def step(self, dt):
		#+(self.v_x*self.v_x+self.v_y*self.v_y)/70000
		self.sr = 0
		if self.m <=1:
			return -1
		self.angle += random.uniform(-3,3)
		self.x+=int(self.v*math.cos(self.angle*3.14/180)*dt)
		self.y+=int(self.v*math.sin(self.angle*3.14/180)*dt)
		self.correct_coords()
		self.get_mass()
		self.lose_mass()
		a = 3
		if self.m>=self.limit :
			self.m*=0.95
			part = 0.5
			child = self.create(part)
			self.m = int(self.m*0.5)
			return child

	def interact(self, other):
		r = self.radius(other)
		self.sr += r
		if r < (self.r + other.r):
			if self.interaction > 0 and other.m>0:
				if other.m<self.interaction*5:
					self.m += other.m
					other.m = 0
				else:
					other.m -= self.interaction*5
					self.m += self.interaction*5
		dx = other.x-self.x
		if abs(dx) > width-abs(dx):
			dx = dx-width

		dy = other.y-self.y
		if abs(dy)>height-abs(dy):
			dy = dy-height
		mult = self.v*math.cos(self.angle*3.14/180)*(dy)-self.v*math.sin(self.angle*3.14/180)*(dx)
		if other.interaction < 0:
			if mult < 0:
				self.angle-=200*self.feel_carni/((r+1)*(r+1))
			else:
				self.angle+=200*self.feel_carni/((r+1)*(r+1))

		if other.interaction > 0:
			if mult < 0:
				self.angle-=200*self.feel_pred/((r+1)*(r+1))
			else:
				self.angle+=200*self.feel_pred/((r+1)*(r+1))

		if self.interaction < 0:	
			self.m -= 0.06*self.r * other.r/(2*r+1)
			

	def radius(self, other):
		dx = abs(other.x-self.x)
		if dx > width-dx:
			dx = width-dx

		dy = abs(other.y-self.y)
		if dy>height-dy:
			dy = height-dy
		return math.sqrt((dx)*(dx)+(dy)*(dy))

	def correct_coords(self):
		if self.x > width/2:
			self.x = -width/2
		if self.x < -width/2:
			self.x = width/2
		 #*random.uniform(-1,1)
		if self.y > width/2:
			self.y = -width/2
		if self.y < -width/2:
			self.y = width/2

	def get_mass(self):
		if self.interaction<0:
			self.m+=0.09*(self.r+3)

	def lose_mass(self):
		self.m -= 0.08*(0.015*self.r+1 + abs(self.v*0.08))