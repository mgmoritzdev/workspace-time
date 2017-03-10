from threading import Timer


class Engine:
	"""A framework to control other bits of code.

	An engine in a framework that controls the execution of other bits of code.
	It calls in a convinient way the setup and updates of container objects. 
	That objects could have an implementation for setup() and update() methods.
	"""

	def __init__(self, interval):
		"""Create an empty engine but don't start it. Set the update interval in seconds."""

		self.containers = []
		self.update_interval = interval
		self.is_running = False
		self.timer = None

	def start(self):
		for c in self.containers:
			c.setup()
			
		self.is_running = True
		self.update()

	def stop(self):
		self.timer.cancel()
		self.is_running = False		

	def update(self):
		self.timer = Timer(self.update_interval, self.update_all)
		self.timer.start()
		
	def update_all(self):
		for c in self.containers:
			c.update()

		if self.is_running:
			self.update()
			
	def append_container(self, container):
		self.containers.append(container)

	def remove_container(self, container):
		self.containers.remove(container)
		
		
