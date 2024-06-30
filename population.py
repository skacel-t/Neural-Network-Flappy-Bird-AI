import player
import config
import math
import operator
import random


class Population:
	def __init__(self, size):
		self.players = []
		self.generation = 1
		self.size = size
		self.generate_players()


	def generate_players(self):
		for i in range(self.size):
			self.players.append(player.Player())


	def update_live_players(self):
		for p in self.players:	
			if p.alive:
				p.look()
				p.think()
				p.draw(config.window)
				p.update(config.ground)


	def natural_selection(self):

		print("SORT BY FITNESS")
		# get 5 best from the previous generation, first randomize to handle ties
		random.shuffle(self.players)
		self.players.sort(key=operator.attrgetter("fitness"), reverse=True)

		champions = []
		for i in range(5):
			champions.append(self.players[i])
		for p in champions:
			print("--------------------")
			print(p.brain.weights)
			print(p.brain.bias)
			print(p.fitness)

		print("\nNEXT GEN")
		children = []

		for champ in champions:
			children.append(champ.clone())

		# fill open player slots with mutated children
		for champ in champions:	
			for _ in range(6):
				children.append(champ.mutate_player())

		# get new gen into players list
		self.players = []
		for child in children:
			self.players.append(child)
		self.generation += 1
		print(self.generation)


	# Return true if all players are dead
	def extinct(self):
		extinct = True
		for p in self.players:
			if p.alive:
				extinct = False
		return extinct
