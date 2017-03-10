class MockContainer:
	def __init__(self):
		self.count_updates = 0
		self.count_setups = 0
		self.name = "Mock"

	def setup(self):
		self.count_setups += 1

	def update(self):
		self.count_updates += 1
