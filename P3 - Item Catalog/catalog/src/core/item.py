class Item:
	def __init__(self, name):
		self.name = name

	# ToDo fix this using a loop
	def set_dict(self, dict):
		self.dict = {}
		self.dict['name'] = dict['name']
		self.dict['id'] = dict['id']
		self.dict['description'] = dict['description']
		self.dict['category_id'] = dict['category_id']
		self.dict['category_name'] = dict['category_name']
		self.dict['creator_id'] = dict['creator_id']

	def set_name(self, name):
		self.name = name

	def set_creator_id(self, creator):
		self.creator_id = creator

	def set_description(self, desc):
		self.description = desc

	def set_id(self, ids):
		self.id = ids

	def set_category_id(self, ids):
		self.category_id = ids

	def set_category_name(self, name):
		self.category_name = name