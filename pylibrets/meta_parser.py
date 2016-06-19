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
            if class_name == self._getElementText(class_xml, 'ClassName'):
                return class_xml

    def _xml_get_table_all(self, resource_id, class_name):
        class_xml = self._xml_get_class(resource_id, class_name)
        return class_xml.find('METADATA-TABLE').findall('Field')

    def _xml_get_table(self, resource_id, class_name, field_system_name):
        field_xml_list = self._xml_get_table_all(resource_id, class_name)
        for field_xml in field_xml_list:
            if field_system_name == self._getElementText(field_xml, 'SystemName'):
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
            if lookup_name == self._getElementText(lookup_xml, 'LookupName'):
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
        system                      = MetadataSystem()
        system.GetSystemID          = self._getElementText(system_xml, 'SystemID')
        system.GetSystemDescription = self._getElementText(system_xml, 'SystemDescription')
        system.GetComments          = self._getElementText(system_xml, 'Comments')
        system.GetTimeZoneOffset    = self._getElementText(system_xml, 'TimeZoneOffset')
        system.GetMetadataID        = self._getElementText(system_xml, 'MetadataID')
        system.GetResourceVersion   = self._getElementText(system_xml, 'ResourceVersion')
        system.GetResourceDate      = self._getElementText(system_xml, 'ResourceDate')
        system.GetForeignKeyVersion = self._getElementText(system_xml, 'ForeignKeyVersion')
        system.GetForeignKeyDate    = self._getElementText(system_xml, 'ForeignKeyDate')
        system.GetFilterVersion     = self._getElementText(system_xml, 'FilterVersion')
        system.GetFilterDate        = self._getElementText(system_xml, 'FilterDate')
        return system

    def GetAllResources(self):
        resource_list = []
        resource_xml_list = self._xml_get_resource_all()
        for resource_xml in resource_xml_list:
            resource              = MetadataResource()
            resource.ResourceID   = self._getElementText(resource_xml, 'ResourceID')
            resource.StandardName = self._getElementText(resource_xml, 'StandardName')
            resource.KeyField     = self._getElementText(resource_xml, 'KeyField')
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
            rets_class              = MetadataClass()
            rets_class.ClassName    = self._getElementText(class_xml, 'ClassName')
            rets_class.StandardName = self._getElementText(class_xml, 'StandardName')
            rets_class.Description  = self._getElementText(class_xml, 'Description')
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
            rets_field                = MetadataTable()
            rets_field.SystemName     = self._getElementText(field_xml, 'SystemName')
            rets_field.StandardName   = self._getElementText(field_xml, 'StandardName')
            rets_field.LongName       = self._getElementText(field_xml, 'LongName')
            rets_field.DBName         = self._getElementText(field_xml, 'DBName')
            rets_field.MaximumLength  = self._getElementText(field_xml, 'MaximumLength')
            rets_field.DataType       = self._getElementText(field_xml, 'DataType')
            rets_field.Precision      = self._getElementText(field_xml, 'Precision')
            rets_field.Searchable     = self._getElementText(field_xml, 'Searchable')
            rets_field.Required       = self._getElementText(field_xml, 'Required')
            rets_field.Interpretation = self._getElementText(field_xml, 'Interpretation')
            rets_field.Units          = self._getElementText(field_xml, 'Units')
            rets_field.Unique         = self._getElementText(field_xml, 'Unique')
            rets_field.LookupName     = self._getElementText(field_xml, 'LookupName')
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
                lookup             = MetadataLookup()
                lookup.LookupName  = self._getElementText(lookup_xml, 'LookupName')
                lookup.VisibleName = self._getElementText(lookup_xml, 'VisibleName')
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
            lookup_type            = MetadataLookupType()
            lookup_type.Value      = self._getElementText(lookup_type_xml, 'Value')
            lookup_type.LongValue  = self._getElementText(lookup_type_xml, 'LongValue')
            lookup_type.ShortValue = self._getElementText(lookup_type_xml, 'ShortValue')
            lookup_list.append(lookup_type)
        return lookup_list

    def GetAllObjects(self, resource_id):
        object_list = []
        object_xml_list = self._xml_get_object_all(resource_id)
        if object_xml_list is not None:
            for object_xml in object_xml_list:
                obj              = MetadataObject()
                obj.ObjectType   = self._getElementText(object_xml, 'ObjectType')
                obj.StandardName = self._getElementText(object_xml, 'StandardName')
                obj.MIMEType     = self._getElementText(object_xml, 'MimeType')
                obj.Description  = self._getElementText(object_xml, 'Description')
                object_list.append(obj)
        return object_list

    def GetSearchHelp(self, resourceName, searchHelpID):
        pass
