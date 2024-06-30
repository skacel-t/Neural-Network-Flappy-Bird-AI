import random
import numpy
import copy
import math


def sigmoid(z):
	return 1/(1+math.exp(-z))


class Network:
	def __init__(self):
		self.inputs = 3
		self.bias = random.uniform(-1,1)
		self.weights = [random.uniform(-1,1) for _ in range(3)]

	def feed_forward(self, vision):
		weighted_sum = self.bias
		for i in range(self.inputs):
			weighted_sum += self.weights[i] * vision[i]
		return sigmoid(weighted_sum)

	def clone(self):
		clone = Network()
		clone.bias = copy.deepcopy(self.bias)
		clone.weights = copy.deepcopy(self.weights)
		return clone
