"""
RETS search response parser classes - .
"""
from xml.etree import ElementTree

from .exceptions import RetsException


class SearchResultSet(object):

	def get_columns(self):
		pass

	def get_data(self):
		pass


class CompactResultSetParser(SearchResultSet):

	def __init__(self, xml_str):
		self.xml_str = xml_str
		self.result_xml = ElementTree.fromstring(xml_str)
		self.delimiter = self._get_delimiter()

	def _get_delimiter(self):
		delimiter_node = self.result_xml.find('DELIMITER')
		return int(delimiter_node.attrib['value'])

	def get_columns(self):
		column_xml_list = self._get_all_column_xml()
		column_list = self._fix_compact_array(column_xml_list.text.split(chr(self.delimiter)))
		return column_list

	def get_data(self):
		data_rows = []
		data_xml_list = self._get_all_data_rows_xml()
		for item in data_xml_list:
			row = self._fix_compact_array(item.text.split(chr(self.delimiter)))
			data_rows.append(row)
		return data_rows

	def _get_all_column_xml(self):
		column_xml = self.result_xml.find('COLUMNS')
		return column_xml

	def _get_all_data_rows_xml(self):
		data_xml_list = self.result_xml.findall('DATA')
		return data_xml_list

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
