import random
import math
width = 10
height = 10

class Cell:
	def __init__(self, x, y, v, angle, r, interaction, feel_herb, feel_pred, m, limit, part):
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
		self.feel_herb = feel_herb
		self.feel_pred = feel_pred
		self.sr = 0
		self.part = part

	def create(self, part):
		angle = random.randint(0, 360)
		r = int(abs(self.r + random.gauss(0, 2)))
		return Cell(int(self.x + 1.5*(self.r + r)*math.cos(angle * 3.14/180)), int(self.y + 1.5*(self.r + r)*math.sin(angle * 3.14/180)),
						self.v + random.gauss(0, 5), self.angle + random.gauss(0, 5), r, self.interaction + random.gauss(0, 10),
						self.feel_herb + random.gauss(0, 10), self.feel_pred + random.gauss(0, 5), 
						int(self.m * part), self.limit + random.gauss(0, 10), abs((self.part + random.gauss(0, 0.1))%1))

	def step(self, dt):
		self.sr = 0
		if self.m <= 1:
			return - 1
		self.angle += random.uniform(-3, 3)
		self.x += int(self.v * math.cos(self.angle * 3.14/180)*dt)
		self.y += int(self.v * math.sin(self.angle * 3.14/180)*dt)
		self.correct_coords()
		self.get_mass()
		self.lose_mass()
		if self.m >= self.limit :
			self.m *= 0.95
			part = self.part
			child = self.create(part)
			self.m = int((1 - part) * self.m)
			return child

	def interact(self, other):
		r = self.radius(other)
		self.sr += r
		if r < (self.r + other.r):
			if self.interaction > 0 and other.m > 0:
				mtp = 5
				if other.m < self.interaction*mtp:
					self.m += other.m
					other.m = 0
				else:
					other.m -= self.interaction*mtp
					self.m += self.interaction*mtp
		dx = other.x - self.x
		if abs(dx) > width - abs(dx):
			if dx > 0:
				dx = dx - width
			else:
				dx = width + dx

		dy = other.y - self.y
		if abs(dy) > height - abs(dy):
			if dy > 0:
				dy = dy - height
			else:
				dy = height + dy

		mult = self.v * math.cos(self.angle * 3.14/180)*dy - self.v * math.sin(self.angle * 3.14/180)*dx

		k = 1000
		if other.interaction < 0:
			if mult < 0:
				self.angle -= k * self.feel_herb/((r+2) * (r+2))
			else:
				self.angle += k * self.feel_herb/((r+2) * (r+2))

		if other.interaction > 0:
			if mult < 0:
				self.angle -= k * self.feel_pred/((r+2) * (r+2))
			else:
				self.angle += k * self.feel_pred/((r+2) * (r+2))

		if self.interaction < 0:	
			self.m -= 0.06 * self.r * other.r/(2*r + 1)
			

	def radius(self, other):
		dx = abs(other.x - self.x)
		if dx > width - dx:
			dx = width - dx

		dy = abs(other.y - self.y)
		if dy > height - dy:
			dy = height - dy
		return math.sqrt( dx * dx + dy * dy)

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
		if self.interaction < 0:
			self.m += 0.09 * (self.r+3)

	def lose_mass(self):
		self.m -= 0.08 * (0.015 * self.r + abs(self.v*0.08) + 1)