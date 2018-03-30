

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
	def __init__(self, world, message):
		self.world = world
		self.WORLD = self.world.WORLD
		self.message   = message
		self.equipment = Equipment_Handling(self.world, message)

	def update(self, message):
		self.movement(message)
		self.pick_up(message)
		self.drop(message)
		self.equip(message)
		self.unequip(message)
	def pick_up(self, message):
		if message["type"] == "pick_up":
			item_target = message['data']["entity_id"]
			action_user = message['data']["action_user"]
			self.world.move_to_inventory(item_target, action_user)

	def equip(self, message):
		if message["type"] == "equip":
			item_target    = message['data']["entity_id"]
			action_user    = message['data']["action_user"]
			requested_slot = message['data']["slot"]
			self.equipment.equip(action_user, item_target, requested_slot)

	def unequip(self, message):
		if message["type"] == "unequip":
			item_target    = message['data']["entity_id"]
			self.equipment.unequip(item_target)

	def movement(self, message):
		if message["type"] == "move":
			room_target = message['data']["room_target"]
			action_user = message['data']["action_user"]
			self.world.move_to_inventory(action_user, room_target)

	def drop(self, message):
		if message["type"] == "drop":
			item_target = message['data']["entity_id"]
			action_user = message['data']["action_user"]
			self.world.move_to_inventory(item_target, self.world.get_location(action_user))

	def notified(self, message):
		self.update(message)


class Equipment_Handling:
	def __init__(self, world, message):
		self.world = world
		self.WORLD = self.world.WORLD
		self.message = message

	def _equip(self, ent_id, item_id, slot):
		self.WORLD['inventory'][ent_id]['items'].remove(item_id)
		self.WORLD['equipment'][ent_id][slot] = item_id
		self.WORLD['equippable'][item_id]['equipped_by']   = ent_id
		self.WORLD['equippable'][item_id]['equipped_slot'] = slot
		message = {
			"type" : "notification",
			"data"  : {
				"action" 	 : "equip",
				"action_user": ent_id,
				"item_id"	 : item_id
			}
		}
		self.message.add_to_queue(message)

	def _unequip(self, ent_id, slot):
		if self.WORLD['equipment'][ent_id][slot] != None:
			item_id = self.WORLD['equipment'][ent_id][slot]
			self.WORLD['equipment'][ent_id][slot] = None
			self.WORLD['inventory'][ent_id]['items'].append(item_id)
			message = {
				"type" : "notification",
				"data"  : {
					"action" 	 : "unequip",
					"action_user": ent_id,
					"item_id"	 : item_id
				}
			}
			self.message.add_to_queue(message)

	def unequip(self, item):
		slot = self.WORLD['equippable'][item]['equipped_slot']
		by   = self.WORLD['equippable'][item]['equipped_by']
		self._unequip(by, slot)

	def equip(self, ent_id, item_id, slot):
		entity_equipment = self.WORLD['equipment'][ent_id]

		if slot == "dual_wield":
			if entity_equipment['left_hand'] == None and entity_equipment['right_hand'] == None:
				self._equip(ent_id, item_id, slot)

			else: 
				self._unequip(ent_id, 'left_hand')
				self._unequip(ent_id, 'right_hand')
				self._equip(ent_id, item_id, slot)

		elif slot == "left_hand":
			if entity_equipment['left_hand'] == None:
				self._equip(ent_id, item_id, slot)
			else:
				self._unequip(ent_id, 'left_hand')
				self._equip(ent_id, item_id, slot)
		elif slot == "right_hand":
			if entity_equipment['right_hand'] == None:
				self._equip(ent_id, item_id, slot)
			else:
				self._unequip(ent_id, 'right_hand')
				self._equip(ent_id, item_id, slot)
