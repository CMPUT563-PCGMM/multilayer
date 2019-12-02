import numpy as np

class tile_values():
	"""docstring for tile_values"""
	def __init__(self, tile):
		self.tiles = {}
		self.tiles[tile] = 1
	

	def add_tile(self, tile):
		if tile in self.tiles:
			self.tiles[tile] = self.tiles[tile] + 1
		else:
			self.tiles[tile] = 1


	def print_object(self):
		print(self.tiles)
		print(self.CPD)
		
		#for key in self.tiles:
		#	print(key, self.tiles[key])


	def calculate_CPD(self):
		self.tile_set = []
		self.CPD = []
		for i in self.tiles:
			self.CPD.append(self.tiles[i])
			self.tile_set.append(i)
		self.CPD = np.asarray(self.CPD)
		self.CPD = self.CPD.reshape(1, self.CPD.shape[0])
		self.CPD = self.CPD / np.sum(self.CPD)
		#print(self.tile_set)
		#print(self.CPD)
		#print(self.generat_new_tile())
		#print(self.CPD.ravel())
		#print(np.random.choice(self.CPD.shape[1],5,p = self.CPD.ravel()))

	def generate_new_tile(self):
		index = np.random.choice(self.CPD.shape[1], 1, p=self.CPD.ravel())
		return self.tile_set[int(index)]
