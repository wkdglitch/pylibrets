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
    MetadataResource, MetadataClass, MetadataTable, MetadataLookup,
    MetadataLookupType, MetadataObject, LoginResponse
)
from .exceptions import (
    LoginException, GetObjectException, SearchException,
    GetMetadataException, NoLoginException, RetsException
)
from .meta_parser import MetadataParser, StandardXmlMetadataParser
from .rets_parser import SearchResultSet, CompactResultSetParser


RETS_1_0   = "RETS/1.0"
RETS_1_5   = "RETS/1.5"
RETS_1_7   = "RETS/1.7"
RETS_1_7_2 = "RETS/1.7.2"
RETS_1_8   = "RETS/1.8"
RETS_1_8_0 = "RETS/1.8.0"

COMPACT = "COMPACT"
COMPACT_DECODED = "COMPACT-DECODED"
STANDARD_XML = "STANDARD-XML"

NO_COUNT = 0
INCLUDE_COUNT = 1
COUNT_ONLY = 2

HTTP_EXPECT_HEADER = "Expect"
RETS_REQUEST_ID_HEADER = "RETS-Request-ID"
RETS_SESSION_ID_HEADER = "RETS-Session-ID"
RETS_SERVER_HEADER = "RETS-Server"
RETS_VERSION_HEADER = "RETS-Version"
RETS_UA_AUTH_HEADER = "RETS-UA-Authorization"
RETS_REQUEST_ID_HEADER = "RETS-Request-ID"
RETS_SESSION_ID_HEADER = "RETS-Session-ID"
RETS_USER_AGENT_HEADER = "User-Agent"

RETS_XML_DEFAULT_ENCODING = "US-ASCII"
RETS_XML_ISO_ENCODING = "iso-8859-1"
RETS_XML_UTF8_ENCODING = "UTF-8"

DEFAULT_USER_AGENT = "%s/%s" % (__title__, __version__)
DEFAULT_RETS_VERSION = RETS_1_5

SEARCH_REQUEST_FORMAT_PARAMETER = "Format"
SEARCH_REQUEST_STANDARD_NAMES_PARAMETER = "StandardNames"
SEARCH_REQUEST_QUERY_TYPE_PARAMETER = "QueryType"
SEARCH_REQUEST_SEARCH_TYPE_PARAMETER = "SearchType"
SEARCH_REQUEST_CLASS_PARAMETER = "Class"
SEARCH_REQUEST_QUERY_PARAMETER = "Query"
SEARCH_REQUEST_SELECT_PARAMETER = "Select"
SEARCH_REQUEST_COUNT_PARAMETER = "Count"
SEARCH_REQUEST_LIMIT_PARAMETER = "Limit"
SEARCH_REQUEST_OFFSET_PARAMETER = "Offset"
SEARCH_REQUEST_RESTRICTED_PARAMETER = "RestrictedIndicator"
SEARCH_REQUEST_PAYLOAD_PARAMETER = "Payload"


class RetsSession(object):

    def __init__(self, login_url, user, passwd, user_agent = None, user_agent_passwd = None, rets_version = DEFAULT_RETS_VERSION):
        self.rets_ua_authorization = None
        self.user = user
        self.passwd = passwd
        self.user_agent = DEFAULT_USER_AGENT if len(user_agent) == 0 else user_agent
        self.user_agent_passwd = user_agent_passwd
        self.rets_version = rets_version
        self.base_url = self._get_base_url(login_url)
        self.login_url = login_url
        self._session = None
        self.logged_in = False
        self.rets_error = None
        self.server_info = None
        self.detected_rets_version = None
        self.result_format = COMPACT_DECODED
        self.result_count = INCLUDE_COUNT
        self.debug = DEFAULT_USER_AGENT

    def __del__(self):
        self.Logout()
        self._session = None

    def _set_rets_ua_authorization(self):
        self._session.headers[RETS_UA_AUTH_HEADER] = self.rets_ua_authorization;

    def _calculate_rets_ua_authorization(self, sid, user_agent, user_agent_passwd, rets_version):
        product = user_agent
        #a1hashed = hashlib.md5(bytes(product + ':' + user_agent_passwd, 'utf-8')).hexdigest()
        a1hashed = hashlib.md5(bytes(product + ':' + user_agent_passwd)).hexdigest()
        retsrequestid = ''
        retssessionid = sid
        #digestHash = hashlib.md5(bytes(a1hashed + ':' + retsrequestid + ':' + retssessionid + ':' + rets_version, 'utf-8')).hexdigest()
        digestHash = hashlib.md5(bytes(a1hashed + ':' + retsrequestid + ':' + retssessionid + ':' + rets_version)).hexdigest()
        return 'Digest ' + digestHash

    def _get_code_text(self, response_xml):
        xml_obj = ElementTree.fromstring(response_xml)
        reply_code = xml_obj.attrib['ReplyCode']
        reply_text = xml_obj.attrib['ReplyText']
        return reply_code, reply_text

    def _get_base_url(self, url_str):
        url_parts = urlparse(url_str)
        resURL = url_parts.scheme + "://" + url_parts.netloc
        return resURL

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

    def _get_object(self, obj_type, resource , obj_id):
        if self.user_agent_passwd:
            self._set_rets_ua_authorization()

        getobject_url = urljoin(self.base_url, self.server_info['GetObject'])
        getobject_response = self._session.get(getobject_url + "?Type=%s&Resource=%s&ID=%s" % (obj_type, resource, obj_id))
        getobject_response.raise_for_status()
        if getobject_response.headers['content-type'] == 'text/plain':
            self._parse_getobject_response(getobject_response.text)

        return getobject_response.content

    def GetLoginUrl(self):
        return self.login_url

    def Login(self):
        try:
            self._session = requests.session()

            headers = {'Accept': "*/*",
                RETS_USER_AGENT_HEADER: self.user_agent,
                RETS_VERSION_HEADER: self.rets_version}

            if self.user_agent_passwd:
                headers[RETS_UA_AUTH_HEADER] = self._calculate_rets_ua_authorization(
                                                    ''
                                                    , self.user_agent
                                                    , self.user_agent_passwd
                                                    , self.rets_version)

            self._session.headers = headers
            self._session.auth = requests.auth.HTTPDigestAuth(self.user, self.passwd)

            response = self._session.get(self.login_url)
            response.raise_for_status()

            self.server_info = self._parse_login_response(response.text)
            self.server_info[RETS_SERVER_HEADER] = response.headers[RETS_SERVER_HEADER]
            self.server_info[RETS_VERSION_HEADER] = response.headers[RETS_VERSION_HEADER]

            if self.user_agent_passwd:
                self.rets_ua_authorization = self._calculate_rets_ua_authorization(
                                                    response.cookies[RETS_SESSION_ID_HEADER]
                                                    , self.user_agent
                                                    , self.user_agent_passwd
                                                    , self.rets_version)
            self.logged_in = True

        except Exception, e:
            self.rets_error = e.message

        return self.logged_in

    def GetLoginResponse(self):
        pass

    def GetCapabilityUrls(self):
        pass

    def GetAction(self):
        pass

    def CreateSearchRequest(self):
        pass

    def Logout(self):
        try:
            if not self.logged_in:
                raise NoLoginException("You are not logged in")

            if self.user_agent_passwd:
                self._set_rets_ua_authorization()

            logout_url = urljoin(self.base_url, self.server_info['Logout'])
            logout_response = self._session.get(logout_url)
            logout_response.raise_for_status()
        except Exception, e:
            self.rets_error = e.message

    def IsLoggedIn(self):
        if not self.logged_in:
            self.Login()
        return self.logged_in

    def Test(self):
        if self.Login():
            self.Logout()
            return True
        else:
            return False

    def GetObject(self, obj_type, resource , obj_id):
        if not self.logged_in:
            raise NoLoginException("You need to call login before getobject")

        for i in range(3):
            try:
                return self._get_object(obj_type, resource , obj_id)
            except socket.timeout:
                if i < 3:
                    print('timeout, try again')
                    time.sleep(5)
                else:
                    raise

    def GetMetadata(self):
        if not self.logged_in:
            raise NoLoginException("You need to call login before getmetadata")

        if self.user_agent_passwd:
            self._set_rets_ua_authorization()

        get_meta_url = urljoin(self.base_url, self.server_info['GetMetadata'])
        response = self._session.get(get_meta_url + '?Type=METADATA-SYSTEM&ID=*&Format=STANDARD-XML')
        response.raise_for_status()
        self._parse_getmetadata_response(response.text)
        return StandardXmlMetadataParser(response.text)

    def Search(self, resource, search_class, query, select = None, limit = None, offset = None):
        if not self.logged_in:
            raise NoLoginException("You need to call login before search")

        if self.user_agent_passwd:
            self._set_rets_ua_authorization()

        if limit:
            limit = 'NONE'

        params = {}
        params.setdefault(SEARCH_REQUEST_SEARCH_TYPE_PARAMETER, resource)
        params.setdefault(SEARCH_REQUEST_CLASS_PARAMETER, search_class)
        params.setdefault(SEARCH_REQUEST_QUERY_PARAMETER, query)
        params.setdefault(SEARCH_REQUEST_QUERY_TYPE_PARAMETER, 'DMQL2')
        params.setdefault(SEARCH_REQUEST_STANDARD_NAMES_PARAMETER, '0')
        params.setdefault(SEARCH_REQUEST_COUNT_PARAMETER, self.result_count)
        params.setdefault(SEARCH_REQUEST_FORMAT_PARAMETER, self.result_format)
        params.setdefault(SEARCH_REQUEST_LIMIT_PARAMETER, limit)

        if offset is not None:
            params.setdefault(SEARCH_REQUEST_OFFSET_PARAMETER, offset)

        if select is not None:
            params.setdefault(SEARCH_REQUEST_SELECT_PARAMETER, select)

        search_url = urljoin(self.base_url, self.server_info['Search'])
        search_response = self._session.post(search_url, params)
        search_response.raise_for_status()
        self._parse_search_response(search_response.text)
        return CompactResultSetParser(search_response.text)
