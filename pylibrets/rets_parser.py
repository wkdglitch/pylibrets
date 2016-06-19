"""RETS search response parser classes."""

from xml.etree import ElementTree
from .exceptions import RetsException


class SearchResultSet(object):

    def GetReplyCode(self):
        pass

    def GetReplyText(self):
        pass

    def GetCount(self):
        pass

    def GetColumns(self):
        pass

    def GetData(self):
        pass


class CompactResultSetParser(SearchResultSet):

    def __init__(self, xml_str):
        self.xml_str = xml_str
        self.result_xml = ElementTree.fromstring(xml_str)
        self.delimiter = self._get_delimiter()


    def _get_delimiter(self):
        delimiter_node = self.result_xml.find('DELIMITER')
        return int(delimiter_node.attrib['value'])


    def _fix_compact_array(self, data_list):
        if len(data_list) < 2:
            raise RetsException('Unknown COMPACT format: ')

        if not len(data_list[0]) == 0:
            raise RetsException('nvalid COMPACT format, missing initial tab: ')
        else:
            del data_list[0]

        if not len(data_list[-1]) == 0:
            raise RetsException('Invalid COMPACT format, missing final tab: ')
        else:
            del data_list[-1]

        return data_list


    def GetReplyCode(self):
        replyCode = self.result_xml.find('RETS').get('ReplyCode')
        return int(replyCode)


    def GetReplyText(self):
        replyText = self.result_xml.find('RETS').get('ReplyText')
        return replyText


    def GetCount(self):
        count = self.result_xml.find('COUNT').get('Records')
        return int(count)


    def GetColumns(self):
        column_xml_list = self.result_xml.find('COLUMNS')
        column_list = self._fix_compact_array(column_xml_list.text.split(chr(self.delimiter)))
        return column_list


    def GetData(self):
        data_rows = []
        column_list = self.GetColumns()
        data_xml_list = self.result_xml.findall('DATA')
        for item in data_xml_list:
            row = dict(zip(column_list, self._fix_compact_array(item.text.split(chr(self.delimiter)))))
            data_rows.append(row)
        return data_rows
