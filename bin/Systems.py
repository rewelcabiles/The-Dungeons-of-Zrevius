

class MessageBoard():
	def __init__(self):
		self.message_queue = []
		self.observers = []
		
	def add_to_queue(self, message):
		self.message_queue.append(message)
		self.notify_observers(message)

	def register(self, observer):
		self.observers.append(observer)
		return observer 

	def notify_observers(self, message):
		for observer in self.observers:
			observer(message)


class Systems:
	def __init__(self, world):
		self.world = world
		self.WORLD = self.world.WORLD

	def update(self, message):
		self.movement(message)

	def movement(self, message):
		if message["type"] == "move":
			room_target = message['pointer']["room_target"]
			action_user = message['pointer']["action_user"]
			self.world.move_to_inventory(action_user, room_target)

	def pickup(self, message):
		if message["type"] == "pick_up":
			item_target = message['pointer']["item_target"]
			action_user = message['pointer']["action_user"]
			self.world.move_to_inventory(item_target, action_user)

	def drop(self, message):
		if message == "drop":
			item_target = message['pointer']["item_target"]
			action_user = message['pointer']["action_user"]
			self.world.move_to_inventory(item_target, self.world.get_location(action_user))

	def notified(self, message):
		self.update(message)