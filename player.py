import my_net
import random
import pygame
import config


class Player:
	def __init__(self):
		# Bird
		self.x, self.y = 50, 200
		self.rect = pygame.Rect(self.x, self.y, 20, 20)
		self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
		self.vel = 0
		self.flap = False
		self.alive = True
		self.score = 0
		self.lifespan = 0
		self.yfit = 0
		self.fitness = 0
		# AI
		self.decision = None
		self.vision = [0.5, 1, 0.5]
		self.brain = my_net.Network()

	# Game related functions
	def draw(self, window):
		pygame.draw.rect(window, self.color, self.rect)

	def ground_collision(self, ground):
		return pygame.Rect.colliderect(self.rect, ground)

	def sky_collision(self):
		return bool(self.rect.y < 30)

	def pipe_collision(self):
		for p in config.pipes:
			return pygame.Rect.colliderect(self.rect, p.top_rect) or pygame.Rect.colliderect(self.rect, p.bottom_rect)

	def update(self, ground):
		if not (self.ground_collision(ground) or self.pipe_collision()):
			# Gravity
			self.vel += 0.25
			self.rect.y += self.vel
			if self.vel > 5:
				self.vel = 5
			# increment lifespan
			self.lifespan += 1
			# update y distance to pipe center
			if config.pipes:
				self.yfit = abs(self.rect.center[1] - (self.closest_pipe().bottom_rect.midtop[1] + self.closest_pipe().opening/2))
			self.fitness = self.lifespan - self.yfit/10
		else:
			self.alive = False
			self.flap = False
			self.vel = 0

	def bird_flap(self):
		if self.vel >=1:
			self.flap = False
		if not self.flap and not self.sky_collision():
			self.flap = True
			self.vel = -5

	@staticmethod
	def closest_pipe():
		for p in config.pipes:
			if not p.passed:
				return p

	# AI related functions
	def look(self):
		if config.pipes:
			# Line to top pipe
			self.vision[0] = max(0, self.rect.center[1] - self.closest_pipe().top_rect.bottom)/500
			pygame.draw.line(config.window, self.color, self.rect.center, (self.rect.center[0], config.pipes[0].top_rect.bottom))

			# Line to mid pipe
			self.vision[1] = max(0, self.closest_pipe().x - self.rect.center[0])/5000
			pygame.draw.line(config.window, self.color, self.rect.center, (self.closest_pipe().x, self.rect.center[1]))
			
			# Line to top pipe
			self.vision[2] = max(0, self.closest_pipe().bottom_rect.top - self.rect.center[1])/500
			pygame.draw.line(config.window, self.color, self.rect.center, (self.rect.center[0], config.pipes[0].bottom_rect.top))


	def think(self):
		self.decision = self.brain.feed_forward(self.vision)
		if self.decision > 0.5:
			self.bird_flap()

	def clone(self):
		clone = Player()
		clone.brain = self.brain.clone()
		return clone

	def mutate_player(self):
		mutant = self.clone()
		for i in range(3):
			mutant.brain.weights[i] += random.gauss(0,1)/10
		mutant.brain.bias += random.gauss(0,1)/10
		return mutant

	def calc_fitness(self):
		fit = self.lifespan + self.yfit/100
		return fit
