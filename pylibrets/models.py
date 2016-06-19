"""
Model classes - contains the primary objects that power pylibRETS.
"""

class MetadataSystem(object):
    def __init__(self):
		self.GetSystemID = None
		self.GetSystemDescription = None
		self.GetComments = None
		self.GetTimeZoneOffset = None
		self.GetMetadataID = None
		self.GetResourceVersion = None
		self.GetResourceDate = None
		self.GetForeignKeyVersion = None
		self.GetForeignKeyDate = None
		self.GetFilterVersion = None
		self.GetFilterDate = None

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

class LoginResponse(object):
	def __init__(self):
		self.GetMemberName = None
		self.GetUserInfo = None
		self.GetBroker = None
		self.GetMetadataVersion = None
		self.GetMetadataTimestamp = None
		self.GetMinMetadataTimestamp = None
		self.GetOfficeList = None
		self.GetBalance = None
		self.GetTimeout = None
		self.GetPasswordExpire = None
		self.GetActionUrl = None
		self.GetChangePasswordUrl = None
		self.GetGetObjectUrl = None
		self.GetLoginUrl = None
		self.GetLoginCompleteUrl = None
		self.GetLogoutUrl = None
		self.GetSearchUrl = None
		self.GetGetMetadataUrl = None
		self.GetServerInformationUrl = None
		self.GetUpdateUrl = None
		self.GetPayloadListUrl = None
		self.GetUserID = None
		self.GetUserClass = None
		self.GetUserLevel = None
		self.GetAgentCode = None
		self.GetBrokerCode = None
		self.GetBrokerBranch = None
		self.GetMetadataID = None
		self.GetWarnPasswordExpirationDays = None
		self.GetStandardNamesVersion = None
		self.GetVendorName = None
		self.GetServerProductName = None
		self.GetServerProductVersion = None
		self.GetOperatorName = None
		self.GetRoleName = None
		self.GetSupportContactInformation = None
		self.GetSessionInformationTokens = None

	def CreateCapabilityUrls(baseUrl):
		pass
