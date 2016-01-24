"""
Model classes - contains the primary objects that power pylibRETS.
"""


class MetadataResource(object):
	def __init__(self):
		self.ResourceID = None
		self.StandardName = None
		self.KeyField = None

class MetadataClass(object):
	def __init__(self):
		self.ClassName = None
		self.StandardName = None
		self.Description = None
		self.VisibleName = None
		self.TableVersion = None
		self.TableDate = None
		self.UpdateVersion = None
		self.UpdateDate = None
		self.ClassTimeStamp = None
		self.DeletedFlagField = None
		self.DeletedFlagValue = None
		self.HasKeyIndex = None
		self.OffsetSupport = None

class MetadataTable(object):
	def __init__(self):
		self.SystemName = None
		self.StandardName = None
		self.LongName = None
		self.DBName = None
		self.ShortName = None
		self.MaximumLength = None
		self.DataType = None
		self.Precision = None
		self.Searchable = None
		self.Interpretation = None
		self.Alignment = None
		self.UseSeparator = None
		self.EditMaskID = None
		self.LookupName = None
		self.MaxSelect = None
		self.Units = None
		self.Index = None
		self.Minimum = None
		self.Maximum = None
		self.Default = None
		self.Required = None
		self.SearchHelpID = None
		self.Unique = None
		self.UpdatesModTimeStamp = None
		self.ForeignKey = None
		self.ForeignField = None
		self.KeyRetrievalQuery = None
		self.KeyRetrievalSelect = None
		self.InKeyIndex = None
		self.FilterParentField = None
		self.DefaultSearchOrder = None
		self.Case = None

class MetadataLookup(object):
	def __init__(self):
		self.LookupName = None
		self.VisibleName = None
		self.Version = None
		self.Date = None
		self.FilterID = None
		self.NotShownByDefault = None

class MetadataLookupType(object):
	def __init__(self):
		self.Value = None
		self.LongValue = None
		self.ShortValue = None

class MetadataObject(object):
	def __init__(self):
		self.ObjectType = None
		self.MIMEType = None
		self.VisibleName = None
		self.Description = None
		self.ObjectTimeStamp = None
		self.ObjectCount = None
		self.LocationAvailability = None
		self.ObjectData = None
		self.MaxFileSize = None
