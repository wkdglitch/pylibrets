"""Metadata Parser classes."""

from xml.etree import ElementTree

from .models import (
    MetadataResource, MetadataClass, MetadataTable, MetadataLookup,
    MetadataLookupType, MetadataObject, MetadataSystem
)
from .exceptions import (
    RetsException, GetMetadataException, GetObjectException
)

class MetadataParser(object):
    def GetSystem(self):
        pass

    def GetAllResources(self):
        pass

    def GetResource(self, resource_id):
        pass

    def GetAllClasses(self, resource_id):
        pass

    def GetClass(self, resource_id, class_name):
        pass

    def GetAllTables(self, resource_id, class_name):
        pass

    def GetTable(self, resource_id, class_name, field_system_name):
        pass

    def GetAllLookups(self, resource_id, class_name, field_system_name):
        pass

    def GetLookup(self, resource_id, class_name, field_system_name, lookup_name):
        pass

    def GetAllLookupTypes(self, resource_id, lookup_name):
        pass

    def GetAllObjects(self, resource_id):
        pass

    def GetSearchHelp(self, resourceName, searchHelpID):
        pass


class StandardXmlMetadataParser(MetadataParser):
    def __init__(self, xml_str):
        self.meta_xml = ElementTree.fromstring(xml_str)

    def _getElementText(self, rootElement, elementName):
        validElement = rootElement.find(elementName)
        return validElement.text if validElement != None else None

    def _xml_get_system(self):
        system_xml = self.meta_xml.find('METADATA').find('METADATA-SYSTEM').find('System')
        return system_xml

    def _xml_get_resource(self, resource_id):
        resource_xml_list = self._xml_get_resource_all()
        for resource_xml in resource_xml_list:
            if resource_id == self._getElementText(resource_xml, 'ResourceID'):
                return resource_xml

    def _xml_get_resource_all(self):
        resource_xml_list = self.meta_xml.find('METADATA').find('METADATA-SYSTEM').find('System').find('METADATA-RESOURCE').findall('Resource')
        return resource_xml_list

    def _xml_get_class_all(self, resource_id):
        resource_xml = self._xml_get_resource(resource_id)
        return resource_xml.find('METADATA-CLASS').findall('Class')

    def _xml_get_class(self, resource_id, class_name):
        class_xml_list = self._xml_get_class_all(resource_id)
        for class_xml in class_xml_list:
            if class_name == class_xml.find('ClassName').text:
                return class_xml

    def _xml_get_table_all(self, resource_id, class_name):
        class_xml = self._xml_get_class(resource_id, class_name)
        return class_xml.find('METADATA-TABLE').findall('Field')

    def _xml_get_table(self, resource_id, class_name, field_system_name):
        field_xml_list = self._xml_get_table_all(resource_id, class_name)
        for field_xml in field_xml_list:
            if field_system_name == field_xml.find('SystemName').text:
                return field_xml

    def _xml_get_lookup_all(self, resource_id):
        resource_xml = self._xml_get_resource(resource_id)
        try:
            return resource_xml.find('METADATA-LOOKUP').findall('LookupType')
        except:
            return None

    def _xml_get_lookup(self, resource_id, lookup_name):
        lookup_xml_list = self._xml_get_lookup_all(resource_id)
        for lookup_xml in lookup_xml_list:
            if lookup_name == lookup_xml.find('LookupName').text:
                return lookup_xml

    def _xml_get_lookup_type_all(self, resource_id, lookup_name):
        lookup_xml = self._xml_get_lookup(resource_id, lookup_name)
        return lookup_xml.find('METADATA-LOOKUP_TYPE').findall('Lookup')

    def _xml_get_object_all(self, resource_id):
        resource_xml = self._xml_get_resource(resource_id)
        try:
            return resource_xml.find('METADATA-OBJECT').findall('Object')
        except:
            return None

    def GetSystem(self):
        system_xml = self._xml_get_system()
        system = MetadataSystem()
        system.GetSystemID = self._getElementText(system_xml, 'SystemID')
        system.GetSystemDescription = self._getElementText(system_xml, 'SystemDescription')
        system.GetComments = self._getElementText(system_xml, 'Comments')
        system.GetTimeZoneOffset = self._getElementText(system_xml, 'TimeZoneOffset')
        system.GetMetadataID = self._getElementText(system_xml, 'MetadataID')
        system.GetResourceVersion = self._getElementText(system_xml, 'ResourceVersion')
        system.GetResourceDate = self._getElementText(system_xml, 'ResourceDate')
        system.GetForeignKeyVersion = self._getElementText(system_xml, 'ForeignKeyVersion')
        system.GetForeignKeyDate = self._getElementText(system_xml, 'ForeignKeyDate')
        system.GetFilterVersion = self._getElementText(system_xml, 'FilterVersion')
        system.GetFilterDate = self._getElementText(system_xml, 'FilterDate')
        return system

    def GetAllResources(self):
        resource_list = []
        resource_xml_list = self._xml_get_resource_all()
        for resource_xml in resource_xml_list:
            resource = MetadataResource()
            resource.ResourceID = self._getElementText(resource_xml, 'ResourceID')
            resource.StandardName = self._getElementText(resource_xml, 'StandardName')
            resource.KeyField = self._getElementText(resource_xml, 'KeyField')
            resource_list.append(resource)
        return resource_list

    def GetResource(self, resource_id):
        resource_list = self.GetAllResources()
        for resource in resource_list:
            if resource.ResourceID == resource_id:
                return resource

    def GetAllClasses(self, resource_id):
        class_list = []
        class_xml_list = self._xml_get_class_all(resource_id)
        for class_xml in class_xml_list:
            rets_class = MetadataClass()
            rets_class.ClassName = class_xml.find('ClassName').text
            rets_class.StandardName = class_xml.find('StandardName').text
            rets_class.Description = class_xml.find('Description').text
            class_list.append(rets_class)
        return class_list

    def GetClass(self, resource_id, class_name):
        rets_class_list = self.GetAllClasses(resource_id)
        for rets_class in rets_class_list:
            if rets_class.ClassName == class_name:
                return rets_class

    def GetAllTables(self, resource_id, class_name):
        field_list = []
        field_xml_list = self._xml_get_table_all(resource_id, class_name)
        for field_xml in field_xml_list:
            rets_field = MetadataTable()
            rets_field.SystemName = field_xml.find('SystemName').text
            rets_field.StandardName = field_xml.find('StandardName').text
            rets_field.LongName = field_xml.find('LongName').text
            rets_field.DBName = field_xml.find('DBName').text
            rets_field.MaximumLength = field_xml.find('MaximumLength').text
            rets_field.DataType = field_xml.find('DataType').text
            rets_field.Precision = field_xml.find('Precision').text
            rets_field.Searchable = field_xml.find('Searchable').text
            rets_field.Required = field_xml.find('Required').text
            rets_field.Interpretation = field_xml.find('Interpretation').text
            rets_field.Units = field_xml.find('Units').text
            rets_field.Unique = field_xml.find('Unique').text
            rets_field.LookupName = field_xml.find('LookupName').text
            field_list.append(rets_field)
        return field_list

    def GetTable(self, resource_id, class_name, field_system_name):
        field_list = self.GetAllTables(resource_id, class_name)
        for field in field_list:
            if field.system_name == field_system_name:
                return field

    def GetAllLookups(self, resource_id):
        lookup_list = []
        lookup_xml_list = self._xml_get_lookup_all(resource_id)
        if lookup_xml_list is not None:
            for lookup_xml in lookup_xml_list:
                lookup = MetadataLookup()
                lookup.LookupName = lookup_xml.find('LookupName').text
                lookup.VisibleName = lookup_xml.find('VisibleName').text
                lookup_list.append(lookup)
        return lookup_list

    def GetLookup(self, resource_id, lookup_name):
        lookup_list = self.GetAllLookups(resource_id)
        for lookup in lookup_list:
            if lookup.LookupName == lookup_name:
                return lookup

    def GetAllLookupTypes(self, resource_id, lookup_name):
        lookup_list = []
        lookup_type_xml_list = self._xml_get_lookup_type_all(resource_id, lookup_name)
        for lookup_type_xml in lookup_type_xml_list:
            lookup_type = MetadataLookupType()
            lookup_type.Value = lookup_type_xml.find('Value').text
            lookup_type.LongValue = lookup_type_xml.find('LongValue').text
            lookup_type.ShortValue = lookup_type_xml.find('ShortValue').text
            lookup_list.append(lookup_type)
        return lookup_list

    def GetAllObjects(self, resource_id):
        object_list = []
        object_xml_list = self._xml_get_object_all(resource_id)
        if object_xml_list is not None:
            for object_xml in object_xml_list:
                obj = MetadataObject()
                obj.ObjectType = object_xml.find('ObjectType').text
                obj.StandardName = object_xml.find('StandardName').text
                obj.MIMEType = object_xml.find('MimeType').text
                obj.Description = object_xml.find('Description').text
                object_list.append(obj)
        return object_list

    def GetSearchHelp(self, resourceName, searchHelpID):
        pass
