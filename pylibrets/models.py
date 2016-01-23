"""
Model classes - contains the primary objects that power pylibRETS.
"""


class RetsResource(object):
	def __init__(self):
		self.resource_id = None
		self.standard_name = None
		self.key_field = None

class RetsClass(object):
	def __init__(self):
		self.class_name = None
		self.standard_name = None
		self.description = None

class RetsField(object):
	def __init__(self):
		self.system_name = None
		self.standard_name = None
		self.long_name = None
		self.db_name = None
		self.max_length = None
		self.data_type = None
		self.precision = None
		self.is_searchable = None
		self.required = None
		self.interpretation = None
		self.units = None
		self.is_unique = None
		self.lookup_name = None

class RetsLookup(object):
	def __init__(self):
		self.lookup_name = None
		self.visible_name = None

class RetsLookupType(object):
	def __init__(self):
		self.value = None
		self.long_value = None
		self.short_value = None

class RetsObject(object):
	def __init__(self):
		self.object_id = None
		self.mime_type = None
		self.visible_name = None
		self.description = None
