__title__ = 'pylibRETS'
__version__ = '0.1.0'

Version = __version__  # for backware compatibility

import requests
from xml.etree import ElementTree
#from urllib import urlparse, urljoin
from urlparse import urlparse, urljoin
import socket
import hashlib
import time
import urllib

from .models import (
	RetsResource, RetsClass, RetsField, RetsLookup,
	RetsLookupType, RetsObject
)
from .exceptions import (
	LoginException, GetObjectException, SearchException,
	GetMetadataException, NoLoginException
)


def enum(**enums):
	return type('Enum', (), enums)


RetsVersion = enum(
	RETS_1_0   = "RETS/1.0", \
	RETS_1_5   = "RETS/1.5", \
	RETS_1_7   = "RETS/1.7", \
	RETS_1_7_2 = "RETS/1.7.2", \
	RETS_1_8   = "RETS/1.8", \
	RETS_1_8_0 = "RETS/1.8.0"
)


class RetsSession(object):
	RETS_SERVER_HEADER = 'RETS-Server'
	RETS_VERSION_HEADER = 'RETS-Version'
	RETS_UA_AUTH_HEADER = 'RETS-UA-Authorization'
	RETS_REQUEST_ID_HEADER = 'RETS-Request-ID'
	RETS_SESSION_ID_HEADER = 'RETS-Session-ID'
	RETS_USER_AGENT_HEADER = 'User-Agent'
	DEFAULT_USER_AGENT = "pylibrets/1.0"
	DEFAULT_RETS_VERSION = RetsVersion.RETS_1_5

	def __init__(self, login_url, user, passwd, user_agent = None, user_agent_passwd = None, rets_version = ''):
		self.rets_ua_authorization = None
		self.user = user
		self.passwd = passwd
		self.user_agent = self.DEFAULT_USER_AGENT if len(user_agent) == 0 else user_agent
		self.user_agent_passwd = user_agent_passwd
		self.rets_version = self.DEFAULT_RETS_VERSION if len(rets_version) == 0 else rets_version
		self.base_url = self._get_base_url(login_url)
		self.login_url = login_url
		self._session = None
		self.logged_in = False
		self.rets_error = None
		self.server_info = None
		self.detected_rets_version = None
		self.debug = self.DEFAULT_USER_AGENT

	def __del__(self):
		self._session = None
		self.logout()

	def login(self):
		try:
			self._session = requests.session()

			headers = {'Accept':"*/*",
				self.RETS_USER_AGENT_HEADER:self.user_agent,
				self.RETS_VERSION_HEADER:self.rets_version}

			if self.user_agent_passwd:
				headers[self.RETS_UA_AUTH_HEADER] = self._calculate_rets_ua_authorization(''
													, self.user_agent
													, self.user_agent_passwd
													, self.rets_version)

			auth = requests.auth.HTTPDigestAuth(self.user, self.passwd)

			self._session.headers = headers
			self._session.auth = auth

			response = self._session.get(self.login_url)
			response.raise_for_status()

			self.server_info = self._parse_login_response(response.text)
			self.server_info[self.RETS_SERVER_HEADER] = response.headers[self.RETS_SERVER_HEADER]
			self.server_info[self.RETS_VERSION_HEADER] = response.headers[self.RETS_VERSION_HEADER]

			if self.user_agent_passwd:
				self.rets_ua_authorization = self._calculate_rets_ua_authorization(response.cookies[self.RETS_SESSION_ID_HEADER]
													, self.user_agent
													, self.user_agent_passwd
													, self.rets_version)
			self.logged_in = True

		except Exception, e:
			self.rets_error = e.message

		return self.logged_in

	def logout(self):
		try:
			if not self.logged_in:
				raise NoLoginException("You are not logged in")

			logout_url = urljoin(self.base_url, self.server_info['Logout'])
			if self.user_agent_passwd:
				self._set_rets_ua_authorization()
			logout_response = self._session.get(logout_url)
			logout_response.raise_for_status()
		except Exception, e:
			self.rets_error = e.message

	def is_logged_in(self):
		if not self.logged_in:
			self.login()
		return self.logged_in

	def test(self):
		if self.login():
			self.logout()
			return True
		else:
			return False

	def get_object(self, obj_type, resource , obj_id):
		if not self.logged_in:
			raise NoLoginException("You need to call login before getobject")

		for i in range(3):
			try:
				return self._getobject(obj_type, resource , obj_id)
			except socket.timeout:
				if i < 3:
					print('timeout, try again')
					time.sleep(5)
				else:
					raise

	def get_metadata(self):
		if not self.logged_in:
			raise NoLoginException("You need to call login before getmetadata")

		get_meta_url = urljoin(self.base_url, self.server_info['GetMetadata'])
		if self.user_agent_passwd:
			self._set_rets_ua_authorization()
		response = self._session.get(get_meta_url + '?Type=METADATA-SYSTEM&ID=*&Format=STANDARD-XML')
		response.raise_for_status()
		self._parse_getmetadata_response(response.text)
		return StandardXmlMetaParser(response.text)

	def search(self, resource, search_class, query, limit, select):
		if not self.logged_in:
			raise NoLoginException("You need to call login before search")

		if limit:
			limit = 'NONE'

		params = {'SearchType': resource,
			'Class': search_class,
			'Query': query,
			'QueryType': 'DMQL2',
			'Count': '0',
			'Format': 'COMPACT-DECODED',
			'Limit': limit,
			'Select': select,
			'StandardNames': '0'}
		search_url = urljoin(self.base_url, self.server_info['Search'])
		if self.user_agent_passwd:
			self._set_rets_ua_authorization()
		search_response = self._session.post(search_url, params)
		search_response.raise_for_status()
		self._parse_search_response(search_response.text)
		return search_response.text

	def _get_base_url(self, url_str):
		url_parts = urlparse(url_str)
		resURL = url_parts.scheme + "://" + url_parts.netloc
		return resURL

	def _getobject(self, obj_type, resource , obj_id):
		getobject_url = urljoin(self.base_url, self.server_info['GetObject'])
		if self.user_agent_passwd:
			self._set_rets_ua_authorization()
		getobject_response = self._session.get(getobject_url + "?Type=%s&Resource=%s&ID=%s" % (obj_type, resource, obj_id))
		getobject_response.raise_for_status()
		if getobject_response.headers['content-type'] == 'text/plain':
			self._parse_getobject_response(getobject_response.text)
		return getobject_response.content

	def _parse_login_response(self, login_resp):
		reply_code, reply_text = self._get_code_text(login_resp)
		if reply_code != '0':
			raise LoginException(reply_code + "," + reply_text)

		login_xml = ElementTree.fromstring(login_resp)
		if len(login_xml) > 0:
			rets_info = login_xml[0].text.split('\n')
		else:
			# for servers which don't have RETS-RESPONSE node
			rets_info = login_xml.text.split('\n')
		rets_info_dict = {}
		for info_item in rets_info:
			if info_item.strip():
				key_value_pair = info_item.split('=')
				rets_info_dict[key_value_pair[0].strip()] = key_value_pair[1].strip()
		return rets_info_dict

	def _parse_getobject_response(self, response):
		reply_code, reply_text = self._get_code_text(response)
		if reply_code != '0':
			raise GetObjectException(reply_code + "," + reply_text)

	def _parse_search_response(self, response):
		if not response:
			raise SearchException('Empty response')
		reply_code, reply_text = self._get_code_text(response)
		if reply_code not in ['0']:
			raise SearchException(reply_code + "," + reply_text)

	def _parse_getmetadata_response(self, response):
		reply_code, reply_text = self._get_code_text(response)
		if reply_code != '0':
			raise GetMetadataException(reply_code + "," + reply_text)

	def _get_code_text(self, response_xml):
		xml_obj = ElementTree.fromstring(response_xml)
		reply_code = xml_obj.attrib['ReplyCode']
		reply_text = xml_obj.attrib['ReplyText']
		return reply_code, reply_text

	def _set_rets_ua_authorization(self):
		self._session.headers[self.RETS_UA_AUTH_HEADER] = self.rets_ua_authorization;

	def _calculate_rets_ua_authorization(self, sid, user_agent, user_agent_passwd, rets_version):
		product = user_agent
		#a1hashed = hashlib.md5(bytes(product + ':' + user_agent_passwd, 'utf-8')).hexdigest()
		a1hashed = hashlib.md5(bytes(product + ':' + user_agent_passwd)).hexdigest()
		retsrequestid = ''
		retssessionid = sid
		#digestHash = hashlib.md5(bytes(a1hashed + ':' + retsrequestid + ':' + retssessionid + ':' + rets_version, 'utf-8')).hexdigest()
		digestHash = hashlib.md5(bytes(a1hashed + ':' + retsrequestid + ':' + retssessionid + ':' + rets_version)).hexdigest()
		return 'Digest ' + digestHash
